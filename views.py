from abc import ABC, abstractmethod

from models import Estudiante, Profesor, Materia, Matricula
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido


# CLASE BASE (ABSTRACTA)
# Solo define la interfaz que debe implementar todo controlador.
class CrudBase(ABC):

    @abstractmethod
    def leer(self):
        """
        Retorna la lista completa de registros.
        
        Args:
            Ninguno
            
        Returns:
            list: Lista de objetos del modelo.
        """
        pass

    @abstractmethod
    def obtener(self, id_registro):
        """
        Busca un registro por su identificador unico.
        
        Args:
            id_registro (int): Identificador a buscar.
            
        Returns:
            object o None: El objeto encontrado o None si no existe.
        """
        pass

    @abstractmethod
    def buscar(self, texto):
        """
        Filtra registros que coincidan con el texto proporcionado.
        
        Args:
            texto (str): Cadena de busqueda.
            
        Returns:
            list: Lista de objetos que coinciden con el criterio.
        """
        pass

    @abstractmethod
    def siguiente(self):
        """
        Calcula el proximo identificador disponible.
        
        Args:
            Ninguno
            
        Returns:
            int: Siguiente ID numerico.
        """
        pass

    @abstractmethod
    def crear(self, datos):
        """
        Crea un nuevo registro a partir de un diccionario de datos.
        
        Args:
            datos (dict): Diccionario con la informacion del registro.
            
        Returns:
            tuple: (bool: exito, object o str: instancia creada o mensaje de error).
        """
        pass

    @abstractmethod
    def actualizar(self, id_registro, datos):
        """
        Modifica un registro existente.
        
        Args:
            id_registro (int): Identificador del registro a modificar.
            datos (dict): Diccionario con los campos a actualizar.
            
        Returns:
            tuple: (bool: exito, object o str: instancia actualizada o mensaje de error).
        """
        pass

    @abstractmethod
    def eliminar(self, id_registro):
        """
        Elimina un registro del sistema.
        
        Args:
            id_registro (int): Identificador del registro a eliminar.
            
        Returns:
            tuple: (bool: exito, str: confirmacion o motivo de fallo).
        """
        pass


# CONTROLADOR DE ESTUDIANTES
class EstudianteController(CrudBase):

    def __init__(self, archivo="datos/estudiantes.json"):
        """
        Inicializa el controlador cargando estudiantes desde el gestor persistente.
        
        Args:
            archivo (str, opcional): Ruta del archivo JSON. Por defecto "datos/estudiantes.json".
            
        Returns:
            None
        """
        self.gestor = GestorJSON(archivo)
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Estudiante.desde_diccionario(datos))

    def guardar(self):
        """
        Persiste los estudiantes actuales serializandolos a diccionario.
        
        Args:
            Ninguno
            
        Returns:
            None
        """
        datos = []
        for estudiante in self.lista:
            datos.append(estudiante.a_diccionario())
        self.gestor.guardar(datos)

    def validar(self, datos, id_actual=None):
        """
        Aplica reglas de negocio e integridad sobre los datos del estudiante.
        
        Args:
            datos (dict): Atributos a validar.
            id_actual (int, opcional): ID del estudiante a omitir en chequeo de duplicados.
            
        Returns:
            str o None: Mensaje descriptivo si hay error, de lo contrario None.
        """
        campos_obligatorios = ("nombre", "apellido", "email", "carnet", "carrera")
        if id_actual is None:
            for campo in campos_obligatorios:
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo '{campo}' es obligatorio"
        else:
            for campo, valor in datos.items():
                if campo in campos_obligatorios and str(valor).strip() == "":
                    return f"El campo '{campo}' no puede quedar vacio"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email):
                return f"Email invalido: '{email}'"
            usados = {e.email for e in self.lista if e.id != id_actual}
            if email in usados:
                return "Ese email ya esta registrado en otro estudiante"

        if "carnet" in datos:
            carnet = str(datos["carnet"]).strip().upper()
            usados_carnet = {e.carnet for e in self.lista if e.id != id_actual}
            if carnet in usados_carnet:
                return f"El carnet '{carnet}' ya pertenece a otro estudiante"

        return None

    def leer(self):
        """
        Retorna la coleccion en memoria de estudiantes.
        
        Args:
            Ninguno
            
        Returns:
            list: Lista de instancias Estudiante.
        """
        return self.lista

    def obtener(self, id_estudiante):
        """
        Localiza un estudiante por su clave primaria.
        
        Args:
            id_estudiante (int): Identificador numerico.
            
        Returns:
            Estudiante o None: Objeto encontrado o None si no existe.
        """
        for estudiante in self.lista:
            if estudiante.id == id_estudiante:
                return estudiante
        return None

    def buscar(self, texto):
        """
        Filtra estudiantes por coincidencia en cualquiera de sus campos de texto.
        
        Args:
            texto (str): Cadena de busqueda.
            
        Returns:
            list: Estudiantes coincidentes.
        """
        texto = texto.strip().lower()
        encontrados = []
        if texto == "":
            return encontrados

        for estudiante in self.lista:
            if (texto in estudiante.nombre.lower()
                    or texto in estudiante.apellido.lower()
                    or texto in estudiante.email
                    or texto in estudiante.carnet.lower()
                    or texto in estudiante.carrera.lower()):
                encontrados.append(estudiante)
        return encontrados

    def siguiente(self):
        """
        Calcula el identificador autoincremental para estudiantes.
        
        Args:
            Ninguno
            
        Returns:
            int: Proximo ID.
        """
        mayor = 0
        for estudiante in self.lista:
            if estudiante.id > mayor:
                mayor = estudiante.id
        return mayor + 1

    def crear(self, datos):
        """
        Instancia, registra y persiste un nuevo Estudiante.
        
        Args:
            datos (dict): Atributos del nuevo estudiante.
            
        Returns:
            tuple: (exito (bool), estudiante (Estudiante) o error (str)).
        """
        error = self.validar(datos)
        if error:
            return False, error

        estudiante = Estudiante(self.siguiente(),
                                str(datos["nombre"]).strip().title(),
                                str(datos["apellido"]).strip().title(),
                                str(datos["email"]).strip().lower(),
                                str(datos["carnet"]).strip().upper(),
                                str(datos["carrera"]).strip().title())
        self.lista.append(estudiante)
        self.guardar()
        return True, estudiante

    def actualizar(self, id_estudiante, datos):
        """
        Modifica los campos indicados de un Estudiante existente.
        
        Args:
            id_estudiante (int): ID del estudiante a modificar.
            datos (dict): Diccionario con los campos a cambiar.
            
        Returns:
            tuple: (exito (bool), estudiante (Estudiante) o error (str)).
        """
        estudiante = self.obtener(id_estudiante)
        if estudiante is None:
            return False, f"No existe un estudiante con id {id_estudiante}"
        if not datos:
            return False, "No se indico ningun cambio"

        permitidos = {"nombre", "apellido", "email", "carnet", "carrera"}
        desconocidos = set(datos) - permitidos
        if desconocidos:
            return False, f"Campos no validos: {', '.join(sorted(desconocidos))}"

        error = self.validar(datos, id_estudiante)
        if error:
            return False, error

        for campo, valor in datos.items():
            valor = str(valor).strip()
            if campo in ("nombre", "apellido", "carrera"):
                valor = valor.title()
            elif campo == "email":
                valor = valor.lower()
            elif campo == "carnet":
                valor = valor.upper()
            setattr(estudiante, campo, valor)

        self.guardar()
        return True, estudiante

    def eliminar(self, id_estudiante):
        """
        Remueve un estudiante del registro si existe.
        
        Args:
            id_estudiante (int): ID del estudiante a eliminar.
            
        Returns:
            tuple: (exito (bool), mensaje (str)).
        """
        estudiante = self.obtener(id_estudiante)
        if estudiante is None:
            return False, f"No existe un estudiante con id {id_estudiante}"

        self.lista.remove(estudiante)
        self.guardar()
        return True, f"Estudiante {id_estudiante} eliminado"

    def carreras_registradas(self):
        """
        Obtiene el conjunto ordenado de carreras sin duplicados.
        
        Args:
            Ninguno
            
        Returns:
            list: Lista de carreras unicas.
        """
        return sorted({e.carrera for e in self.lista if e.carrera != ""})


# CONTROLADOR DE PROFESORES
class ProfesorController(CrudBase):

    def __init__(self, archivo="datos/profesores.json"):
        """
        Inicializa el controlador cargando profesores desde el almacenamiento JSON.
        
        Args:
            archivo (str, opcional): Ruta del archivo JSON. Por defecto "datos/profesores.json".
            
        Returns:
            None
        """
        self.materias = None
        self.gestor = GestorJSON(archivo)
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Profesor.desde_diccionario(datos))

    def vincular_materias(self, materias_controller):
        """
        Asocia el controlador de materias para resolver desasignaciones en cascada.
        
        Args:
            materias_controller (MateriaController): Instancia del catalogo de materias.
            
        Returns:
            None
        """
        self.materias = materias_controller

    def guardar(self):
        """
        Serializa y persiste la coleccion de profesores en JSON.
        
        Args:
            Ninguno
            
        Returns:
            None
        """
        datos = []
        for profesor in self.lista:
            datos.append(profesor.a_diccionario())
        self.gestor.guardar(datos)

    def validar(self, datos, id_actual=None):
        """
        Valida integridad de campos obligatorios y formato/unicidad de correo.
        
        Args:
            datos (dict): Atributos a comprobar.
            id_actual (int, opcional): ID a ignorar al verificar correo repetido.
            
        Returns:
            str o None: Error identificado o None si es valido.
        """
        campos_obligatorios = ("nombre", "apellido", "email", "especialidad")
        if id_actual is None:
            for campo in campos_obligatorios:
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo '{campo}' es obligatorio"
        else:
            for campo, valor in datos.items():
                if campo in campos_obligatorios and str(valor).strip() == "":
                    return f"El campo '{campo}' no puede quedar vacio"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email):
                return f"Email invalido: '{email}'"
            usados = {p.email for p in self.lista if p.id != id_actual}
            if email in usados:
                return "Ese email ya esta registrado en otro profesor"

        return None

    def leer(self):
        """
        Devuelve la lista completa de docentes.
        
        Args:
            Ninguno
            
        Returns:
            list: Instancias de Profesor.
        """
        return self.lista

    def obtener(self, id_profesor):
        """
        Busca un docente por su identificador unico.
        
        Args:
            id_profesor (int): Clave primaria.
            
        Returns:
            Profesor o None: Docente encontrado o None.
        """
        for profesor in self.lista:
            if profesor.id == id_profesor:
                return profesor
        return None

    def buscar(self, texto):
        """
        Filtra profesores por nombre, apellido, correo, titulo o especialidad.
        
        Args:
            texto (str): Cadena de busqueda.
            
        Returns:
            list: Profesores coincidentes.
        """
        texto = texto.strip().lower()
        encontrados = []
        if texto == "":
            return encontrados

        for profesor in self.lista:
            if (texto in profesor.nombre.lower()
                    or texto in profesor.apellido.lower()
                    or texto in profesor.email
                    or texto in profesor.titulo.lower()
                    or texto in profesor.especialidad.lower()):
                encontrados.append(profesor)
        return encontrados

    def siguiente(self):
        """
        Calcula el identificador siguiente disponible para profesores.
        
        Args:
            Ninguno
            
        Returns:
            int: Proximo ID.
        """
        mayor = 0
        for profesor in self.lista:
            if profesor.id > mayor:
                mayor = profesor.id
        return mayor + 1

    def crear(self, datos):
        """
        Construye, registra y persiste un nuevo Profesor.
        
        Args:
            datos (dict): Datos del docente.
            
        Returns:
            tuple: (exito (bool), profesor (Profesor) o error (str)).
        """
        error = self.validar(datos)
        if error:
            return False, error

        profesor = Profesor(self.siguiente(),
                            str(datos["nombre"]).strip().title(),
                            str(datos["apellido"]).strip().title(),
                            str(datos["email"]).strip().lower(),
                            str(datos.get("titulo", "")).strip().title(),
                            str(datos["especialidad"]).strip().title())
        self.lista.append(profesor)
        self.guardar()
        return True, profesor

    def actualizar(self, id_profesor, datos):
        """
        Aplica modificaciones sobre los campos de un docente existente.
        
        Args:
            id_profesor (int): ID del docente a actualizar.
            datos (dict): Diccionario con los campos a alterar.
            
        Returns:
            tuple: (exito (bool), profesor (Profesor) o error (str)).
        """
        profesor = self.obtener(id_profesor)
        if profesor is None:
            return False, f"No existe un profesor con id {id_profesor}"
        if not datos:
            return False, "No se indico ningun cambio"

        permitidos = {"nombre", "apellido", "email", "titulo", "especialidad"}
        desconocidos = set(datos) - permitidos
        if desconocidos:
            return False, f"Campos no validos: {', '.join(sorted(desconocidos))}"

        error = self.validar(datos, id_profesor)
        if error:
            return False, error

        for campo, valor in datos.items():
            valor = str(valor).strip()
            if campo in ("nombre", "apellido", "titulo", "especialidad"):
                valor = valor.title()
            elif campo == "email":
                valor = valor.lower()
            setattr(profesor, campo, valor)

        self.guardar()
        return True, profesor

    def eliminar(self, id_profesor):
        """
        Elimina un docente del sistema y desvincula sus materias en cascada.
        
        Args:
            id_profesor (int): ID del profesor.
            
        Returns:
            tuple: (exito (bool), mensaje (str)).
        """
        profesor = self.obtener(id_profesor)
        if profesor is None:
            return False, f"No existe un profesor con id {id_profesor}"

        if self.materias is not None:
            for materia in self.materias.materias_por_docente(id_profesor):
                materia.desasignar_docente()
            self.materias.guardar()

        self.lista.remove(profesor)
        self.guardar()
        return True, f"Profesor {id_profesor} eliminado"


# CONTROLADOR DE MATERIAS
class MateriaController(CrudBase):

    def __init__(self, profesores, archivo="datos/materias.json"):
        """
        Inicializa el catalogo de asignaturas inyectando la referencia al controlador docente.
        
        Args:
            profesores (ProfesorController): Controlador de docentes para validar y resolver relaciones.
            archivo (str, opcional): Ruta del archivo JSON. Por defecto "datos/materias.json".
            
        Returns:
            None
        """
        self.profesores = profesores
        self.profesores.vincular_materias(self)
        self.gestor = GestorJSON(archivo)
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Materia.desde_diccionario(datos))

    def guardar(self):
        """
        Persiste el estado actual de las materias en JSON.
        
        Args:
            Ninguno
            
        Returns:
            None
        """
        datos = []
        for materia in self.lista:
            datos.append(materia.a_diccionario())
        self.gestor.guardar(datos)

    def validar(self, datos, id_actual=None):
        """
        Comprueba campos obligatorios, unicidad de codigo y valores de creditos y cupos.
        
        Args:
            datos (dict): Atributos a comprobar.
            id_actual (int, opcional): ID a ignorar al evaluar duplicidad de codigo.
            
        Returns:
            str o None: Error detectado o None si la informacion es valida.
        """
        campos_obligatorios = ("nombre", "codigo", "creditos")
        if id_actual is None:
            for campo in campos_obligatorios:
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo '{campo}' es obligatorio"
        else:
            for campo, valor in datos.items():
                if campo in campos_obligatorios and str(valor).strip() == "":
                    return f"El campo '{campo}' no puede quedar vacio"

        if "creditos" in datos:
            creditos_str = str(datos["creditos"]).strip()
            if not creditos_str.isdigit() or int(creditos_str) <= 0:
                return "Los creditos deben ser un numero entero mayor a 0"

        if "cupos" in datos:
            cupos_str = str(datos.get("cupos", "")).strip()
            if cupos_str != "" and (not cupos_str.isdigit() or int(cupos_str) < 0):
                return "Los cupos deben ser un numero entero mayor o igual a 0"

        if "codigo" in datos:
            codigo = str(datos["codigo"]).strip().upper()
            for otra in self.lista:
                if otra.codigo == codigo and otra.id != id_actual:
                    return f"Ya existe una materia con el codigo '{codigo}'"

        return None

    def leer(self):
        """
        Retorna la coleccion en memoria de materias.
        
        Args:
            Ninguno
            
        Returns:
            list: Lista de objetos Materia.
        """
        return self.lista

    def obtener(self, id_materia):
        """
        Recupera una materia mediante su clave primaria.
        
        Args:
            id_materia (int): ID de la asignatura.
            
        Returns:
            Materia o None: Instancia encontrada o None.
        """
        for materia in self.lista:
            if materia.id == id_materia:
                return materia
        return None

    def buscar(self, texto):
        """
        Filtra asignaturas por nombre o codigo oficial.
        
        Args:
            texto (str): Cadena de busqueda.
            
        Returns:
            list: Asignaturas coincidentes.
        """
        texto = texto.strip().lower()
        encontrados = []
        if texto == "":
            return encontrados

        for materia in self.lista:
            if texto in materia.nombre.lower() or texto in materia.codigo.lower():
                encontrados.append(materia)
        return encontrados

    def siguiente(self):
        """
        Genera el proximo identificador autoincremental para asignaturas.
        
        Args:
            Ninguno
            
        Returns:
            int: Proximo ID disponible.
        """
        mayor = 0
        for materia in self.lista:
            if materia.id > mayor:
                mayor = materia.id
        return mayor + 1

    def crear(self, datos):
        """
        Instancia y persiste una nueva Materia sin docente asignado inicialmente.
        
        Args:
            datos (dict): Datos para construir la asignatura.
            
        Returns:
            tuple: (exito (bool), materia (Materia) o error (str)).
        """
        error = self.validar(datos)
        if error:
            return False, error

        creditos = int(str(datos["creditos"]).strip())
        cupos_str = str(datos.get("cupos", "")).strip()
        cupos = int(cupos_str) if cupos_str != "" else Materia.CUPOS_MAXIMOS

        materia = Materia(self.siguiente(),
                          str(datos["nombre"]).strip().title(),
                          str(datos["codigo"]).strip().upper(),
                          creditos,
                          cupos)

        self.lista.append(materia)
        self.guardar()
        return True, materia

    def actualizar(self, id_materia, datos):
        """
        Modifica los atributos basicos de una asignatura existente.
        
        Args:
            id_materia (int): ID de la asignatura a modificar.
            datos (dict): Campos a actualizar.
            
        Returns:
            tuple: (exito (bool), materia (Materia) o error (str)).
        """
        materia = self.obtener(id_materia)
        if materia is None:
            return False, f"No existe una materia con id {id_materia}"
        if not datos:
            return False, "No se indico ningun cambio"

        desconocidos = set(datos) - {"nombre", "codigo", "creditos", "cupos"}
        if desconocidos:
            return False, f"Campos no validos: {', '.join(sorted(desconocidos))}"

        error = self.validar(datos, id_materia)
        if error:
            return False, error

        if "nombre" in datos:
            materia.nombre = str(datos["nombre"]).strip().title()
        if "codigo" in datos:
            materia.codigo = str(datos["codigo"]).strip().upper()
        if "creditos" in datos:
            materia.creditos = int(datos["creditos"])
        if "cupos" in datos:
            materia.cupos = int(datos["cupos"])

        self.guardar()
        return True, materia

    def eliminar(self, id_materia):
        """
        Remueve una asignatura del catalogo.
        
        Args:
            id_materia (int): ID de la materia a eliminar.
            
        Returns:
            tuple: (exito (bool), mensaje (str)).
        """
        materia = self.obtener(id_materia)
        if materia is None:
            return False, f"No existe una materia con id {id_materia}"

        self.lista.remove(materia)
        self.guardar()
        return True, f"Materia {id_materia} eliminada"

    def asignar_docente(self, id_materia, id_profesor):
        """
        Asocia una materia a un docente validado.
        
        Args:
            id_materia (int): ID de la asignatura.
            id_profesor (int): ID del docente a vincular.
            
        Returns:
            tuple: (exito (bool), tupla (materia, profesor) o mensaje de error (str)).
        """
        materia = self.obtener(id_materia)
        if materia is None:
            return False, f"No existe la materia con id {id_materia}"

        profesor = self.profesores.obtener(id_profesor)
        if profesor is None:
            return False, f"No existe un docente con id {id_profesor}"

        materia.profesor_id = profesor.id
        self.guardar()
        return True, (materia, profesor)

    def desasignar_docente(self, id_materia):
        """
        Disocia el docente a cargo de una materia restableciendo profesor_id a 0.
        
        Args:
            id_materia (int): ID de la asignatura a liberar.
            
        Returns:
            tuple: (exito (bool), materia (Materia) o mensaje de error (str)).
        """
        materia = self.obtener(id_materia)
        if materia is None:
            return False, f"No existe la materia con id {id_materia}"

        if not materia.tiene_docente():
            return False, f"La materia {materia.codigo} no tiene ningun docente asignado actualmente"

        materia.desasignar_docente()
        self.guardar()
        return True, materia

    def materias_por_docente(self, id_profesor):
        """
        Filtra y devuelve las materias asignadas a un docente especifico.
        
        Args:
            id_profesor (int): Identificador del docente.
            
        Returns:
            list: Asignaturas dictadas por el profesor.
        """
        return [m for m in self.lista if m.profesor_id == id_profesor]


# CONTROLADOR DE MATRICULAS (TRANSACCIONAL)
class MatriculaController(CrudBase):

    def __init__(self, estudiantes, materias, archivo="datos/matriculas.json"):
        """
        Inicializa el controlador transaccional inyectando dependencias de estudiantes y materias.
        
        Args:
            estudiantes (EstudianteController): Controlador de estudiantes.
            materias (MateriaController): Controlador de materias.
            archivo (str, opcional): Ruta del archivo JSON. Por defecto "datos/matriculas.json".
            
        Returns:
            None
        """
        self.estudiantes = estudiantes
        self.materias = materias
        self.gestor = GestorJSON(archivo)
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Matricula.desde_diccionario(datos))

    def guardar(self):
        """
        Persiste los registros transaccionales de matricula en JSON.
        
        Args:
            Ninguno
            
        Returns:
            None
        """
        datos = []
        for matricula in self.lista:
            datos.append(matricula.a_diccionario())
        self.gestor.guardar(datos)

    def validar_creacion(self, datos):
        """
        Verifica existencia de claves foraneas, periodo obligatorio, cupos y previene duplicados.
        
        Args:
            datos (dict): Diccionario con estudiante_id, materia_id y periodo.
            
        Returns:
            str o None: Motivo de rechazo o None si la operacion es valida.
        """
        try:
            estudiante_id = int(datos.get("estudiante_id", 0))
            materia_id = int(datos.get("materia_id", 0))
        except (TypeError, ValueError):
            return "estudiante_id y materia_id deben ser numeros enteros"

        periodo = str(datos.get("periodo", "")).strip().upper()
        if not periodo:
            return "El periodo academico es obligatorio (ej. '2026-1')"

        if self.estudiantes.obtener(estudiante_id) is None:
            return f"No existe un estudiante con id {estudiante_id}"

        materia = self.materias.obtener(materia_id)
        if materia is None:
            return f"No existe una materia con id {materia_id}"

        for mat in self.lista:
            if (mat.estudiante_id == estudiante_id and 
                mat.materia_id == materia_id and 
                mat.periodo.upper() == periodo):
                return f"El estudiante ya esta matriculado en {materia.codigo} para el periodo {periodo}"

        if not materia.hay_cupo():
            return f"La materia {materia.codigo} ya no tiene cupos disponibles"

        return None

    def leer(self):
        """
        Retorna la lista de matriculas registradas.
        
        Args:
            Ninguno
            
        Returns:
            list: Instancias Matricula.
        """
        return self.lista

    def obtener(self, id_matricula):
        """
        Recupera una inscripcion por su clave primaria.
        
        Args:
            id_matricula (int): ID de la matricula.
            
        Returns:
            Matricula o None: Registro encontrado o None.
        """
        for matricula in self.lista:
            if matricula.id == id_matricula:
                return matricula
        return None

    def buscar(self, texto):
        """
        Filtra inscripciones por periodo lectivo o fecha ISO.
        
        Args:
            texto (str): Cadena de busqueda.
            
        Returns:
            list: Matriculas que coinciden con el criterio.
        """
        texto = texto.strip().lower()
        encontradas = []
        if texto == "":
            return encontradas

        for matricula in self.lista:
            if texto in matricula.periodo.lower() or texto in matricula.fecha:
                encontradas.append(matricula)
        return encontradas

    def siguiente(self):
        """
        Calcula el identificador autoincremental para matriculas.
        
        Args:
            Ninguno
            
        Returns:
            int: Proximo ID.
        """
        mayor = 0
        for matricula in self.lista:
            if matricula.id > mayor:
                mayor = matricula.id
        return mayor + 1

    def crear(self, datos):
        """
        Ejecuta la transaccion academica: crea la matricula, decrementa cupo y persiste ambos estados.
        
        Args:
            datos (dict): Informacion requerida para la matricula.
            
        Returns:
            tuple: (exito (bool), matricula (Matricula) o error (str)).
        """
        error = self.validar_creacion(datos)
        if error:
            return False, error

        materia = self.materias.obtener(int(datos["materia_id"]))

        matricula = Matricula(self.siguiente(),
                              int(datos["estudiante_id"]),
                              materia.id,
                              str(datos["periodo"]).strip().upper())

        materia.ocupar_cupo()
        self.materias.guardar()

        self.lista.append(matricula)
        self.guardar()

        return True, matricula

    def actualizar(self, id_matricula, datos):
        """
        Actualiza exclusivamente la calificacion de la matricula evaluando su rango valido.
        
        Args:
            id_matricula (int): ID de la matricula a asentar nota.
            datos (dict): Diccionario con la clave 'nota'.
            
        Returns:
            tuple: (exito (bool), matricula (Matricula) o error (str)).
        """
        matricula = self.obtener(id_matricula)
        if matricula is None:
            return False, f"No existe la matricula {id_matricula}"

        if "nota" not in datos or str(datos["nota"]).strip() == "":
            return False, "Debe ingresar una calificacion valida"

        if not Materia.es_nota_valida(datos["nota"]):
            return False, "La nota no es valida. Debe ser un numero entre 0 y 20"

        matricula.nota = float(datos["nota"])
        self.guardar()

        return True, matricula

    def eliminar(self, id_matricula):
        """
        Anula la transaccion academica, reintegra el cupo al catalogo y persiste los cambios.
        
        Args:
            id_matricula (int): ID de la matricula a remover.
            
        Returns:
            tuple: (exito (bool), mensaje (str)).
        """
        matricula = self.obtener(id_matricula)
        if matricula is None:
            return False, f"No existe la matricula {id_matricula}"

        materia = self.materias.obtener(matricula.materia_id)
        if materia is not None:
            materia.liberar_cupo()
            self.materias.guardar()

        self.lista.remove(matricula)
        self.guardar()
        return True, f"Matricula {id_matricula} anulada y cupo liberado"

    def reporte_academico(self, id_estudiante):
        """
        Estructura el historial academico de un estudiante como modelo de datos transferible.
        
        Args:
            id_estudiante (int): ID del estudiante consultado.
            
        Returns:
            dict o None: Datos completos del estudiante y sus asignaturas inscritas, o None si no existe.
        """
        estudiante = self.estudiantes.obtener(id_estudiante)
        if estudiante is None:
            return None

        inscripciones = []
        for mat in self.lista:
            if mat.estudiante_id == id_estudiante:
                materia = self.materias.obtener(mat.materia_id)
                inscripciones.append({
                    "matricula_id": mat.id,
                    "periodo": mat.periodo,
                    "materia_nombre": materia.nombre if materia else "Materia eliminada",
                    "materia_codigo": materia.codigo if materia else "N/A",
                    "nota": mat.nota,
                    "estado": mat.estado()
                })

        return {
            "estudiante": estudiante,
            "inscripciones": inscripciones
        }