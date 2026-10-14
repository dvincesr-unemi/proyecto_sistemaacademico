from datetime import date
from typing import Dict, Any


# CLASE BASE: lo que los modelos comparten
class ModeloBase:
    """Padre de todos los modelos. Guarda el id y define el comportamiento comun."""

    def __init__(self, id_registro: int) -> None:
        """
        Inicializa la entidad base con su identificador unico.

        Args:
            id_registro (int): Identificador numerico unico para el registro.

        Returns:
            None
        """
        self.id = int(id_registro)

    # UNICO METODO DE CLASE DEL PROYECTO
    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> "ModeloBase":
        """
        Diccionario -> objeto. Escrito UNA vez y usado por todos los modelos.
        cls es la clase que llamo (Estudiante, Profesor, Materia, etc.).

        Args:
            datos (Dict[str, Any]): Diccionario con los datos leidos del JSON.

        Returns:
            ModeloBase: Instancia de la clase que hizo la llamada.
        """
        datos_copia = dict(datos)                  # copia, para no tocar el original
        id_registro = datos_copia.pop("id")        # saco el id
        return cls(id_registro, **datos_copia)     # el resto son los campos del modelo

    # METODOS DE INSTANCIA
    def a_diccionario(self) -> Dict[str, Any]:
        """
        Objeto -> diccionario. Cada hijo agrega sus campos.

        Args:
            Ninguno

        Returns:
            Dict[str, Any]: Diccionario base conteniendo solo el id.
        """
        return {"id": self.id}

    def etiqueta(self) -> str:
        """
        POLIMORFISMO: cada hijo la reescribe a su manera para listados.

        Args:
            Ninguno

        Returns:
            str: Texto generico con el numero de registro.
        """
        return f"registro {self.id}"

    def __str__(self) -> str:
        """
        Lo que se ve al hacer print(objeto). Llama a etiqueta(),
        asi que cada modelo se imprime distinto sin cambiar esta linea.

        Args:
            Ninguno

        Returns:
            str: Representacion final formateada para la consola.
        """
        return f"[{self.id}] {self.etiqueta()}"


# HERENCIA: Persona es la base de Estudiantes y Profesores
class Persona(ModeloBase):
    """Todo lo que tiene una persona del sistema."""

    def __init__(self, id_registro: int, nombre: str, apellido: str, email: str) -> None:
        """
        Inicializa una Persona con sus datos civiles basicos.

        Args:
            id_registro (int): Identificador unico numerico.
            nombre (str): Nombre de la persona.
            apellido (str): Apellido de la persona.
            email (str): Correo electronico de contacto.

        Returns:
            None
        """
        super().__init__(id_registro)      # el padre guarda el id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email

    def nombre_completo(self) -> str:
        """
        Concatena de forma limpia el nombre y el apellido.

        Args:
            Ninguno

        Returns:
            str: Nombre y apellido unidos por un espacio.
        """
        return f"{self.nombre} {self.apellido}"

    def a_diccionario(self) -> Dict[str, Any]:
        """
        Agrega los atributos de Persona al diccionario del padre.

        Args:
            Ninguno

        Returns:
            Dict[str, Any]: Diccionario con id, nombre, apellido y email.
        """
        datos = super().a_diccionario()    # {"id": ...} que arma el padre
        datos["nombre"] = self.nombre
        datos["apellido"] = self.apellido
        datos["email"] = self.email
        return datos

    def etiqueta(self) -> str:
        """
        Sobrescribe la representacion base para devolver el nombre completo.

        Args:
            Ninguno

        Returns:
            str: Nombre completo.
        """
        return self.nombre_completo()


class Estudiante(Persona):
    """Estudiante ES UNA Persona, con carnet y carrera."""

    def __init__(
        self, id_registro: int, nombre: str, apellido: str, email: str, 
        carnet: str = "", carrera: str = ""
    ) -> None:
        """
        Inicializa un Estudiante integrando sus datos academicos.

        Args:
            id_registro (int): Identificador unico numerico.
            nombre (str): Nombre del estudiante.
            apellido (str): Apellido del estudiante.
            email (str): Correo electronico de contacto.
            carnet (str, opcional): Codigo de identificacion. Por defecto "".
            carrera (str, opcional): Programa academico. Por defecto "".

        Returns:
            None
        """
        super().__init__(id_registro, nombre, apellido, email)
        self.carnet = carnet
        self.carrera = carrera

    def a_diccionario(self) -> Dict[str, Any]:
        """
        Extiende el diccionario de Persona agregando carnet y carrera.

        Args:
            Ninguno

        Returns:
            Dict[str, Any]: Diccionario completo del Estudiante.
        """
        datos = super().a_diccionario()    # reutiliza lo de Persona
        datos["carnet"] = self.carnet
        datos["carrera"] = self.carrera
        return datos

    def etiqueta(self) -> str:
        """
        Sobrescribe y EXTIENDE la etiqueta del padre (Persona).

        Args:
            Ninguno

        Returns:
            str: Representacion con nombre, carnet y carrera.
        """
        return f"{super().etiqueta()} · {self.carnet or 'sin carnet'} · {self.carrera}"


class Profesor(Persona):
    """Profesor ES UNA Persona, con titulo y especialidad academica."""

    def __init__(
        self, id_registro: int, nombre: str, apellido: str, email: str, 
        titulo: str = "", especialidad: str = ""
    ) -> None:
        """
        Inicializa un Profesor integrando sus datos profesionales.

        Args:
            id_registro (int): Identificador unico numerico.
            nombre (str): Nombre del profesor.
            apellido (str): Apellido del profesor.
            email (str): Correo electronico de contacto.
            titulo (str, opcional): Titulo academico (ej. Ing., PhD). Por defecto "".
            especialidad (str, opcional): Area de dominio academico. Por defecto "".

        Returns:
            None
        """
        super().__init__(id_registro, nombre, apellido, email)
        self.titulo = titulo
        self.especialidad = especialidad

    def a_diccionario(self) -> Dict[str, Any]:
        """
        Extiende el diccionario de Persona agregando titulo y especialidad.

        Args:
            Ninguno

        Returns:
            Dict[str, Any]: Diccionario completo del Profesor.
        """
        datos = super().a_diccionario()
        datos["titulo"] = self.titulo
        datos["especialidad"] = self.especialidad
        return datos

    def etiqueta(self) -> str:
        """
        Genera la presentacion del docente.

        Args:
            Ninguno

        Returns:
            str: Representacion con titulo, nombre y especialidad.
        """
        titulo_texto = f"{self.titulo} " if self.titulo else ""
        return f"{titulo_texto}{super().etiqueta()} · Especialidad: {self.especialidad or 'General'}"


# UNICA CLASE CON ATRIBUTOS Y METODOS ESTATICOS
class Materia(ModeloBase):
    """Materia ES UN ModeloBase. Contiene reglas de aula y asignacion docente."""

    # ATRIBUTOS ESTATICOS (de clase): existen una sola vez, no por objeto
    CUPOS_MAXIMOS = 30           # regla del negocio, igual para todas las materias
    NOTA_APROBACION = 14         # calificacion minima para aprobar
    total_creadas = 0            # contador compartido

    def __init__(
        self, id_registro: int, nombre: str, codigo: str, 
        creditos: int = 0, cupos: int = 30, profesor_id: int = 0
    ) -> None:
        """
        Inicializa una asignatura academica.

        Args:
            id_registro (int): Identificador unico numerico.
            nombre (str): Nombre de la asignatura.
            codigo (str): Codigo institucional de la asignatura.
            creditos (int, opcional): Valor en creditos academicos. Por defecto 0.
            cupos (int, opcional): Plazas disponibles. Por defecto 30.
            profesor_id (int, opcional): ID del docente asignado. Por defecto 0 (sin asignar).

        Returns:
            None
        """
        super().__init__(id_registro)
        self.nombre = nombre
        self.codigo = codigo
        self.creditos = int(creditos)
        self.cupos = int(cupos)
        self.profesor_id = int(profesor_id)
        Materia.total_creadas += 1

    # METODOS ESTATICOS: reglas que no necesitan ninguna materia concreta
    @staticmethod
    def es_nota_valida(valor: Any) -> bool:
        """
        Valida que un ingreso numerico este dentro del rango permitido (0 a 20).

        Args:
            valor (Any): Valor a evaluar, usualmente string o numerico.

        Returns:
            bool: True si es valido, False si hay error de tipo o rango.
        """
        try:
            nota = float(valor)
            return 0 <= nota <= 20
        except (TypeError, ValueError):
            return False

    # METODOS DE INSTANCIA: estado y reglas de la asignatura
    def hay_cupo(self) -> bool:
        """
        Verifica si la materia aun cuenta con plazas disponibles.

        Args:
            Ninguno

        Returns:
            bool: True si hay cupos restantes.
        """
        return self.cupos > 0

    def ocupar_cupo(self) -> None:
        """
        Resta 1 a la disponibilidad si es que todavia hay cupos.

        Args:
            Ninguno

        Returns:
            None
        """
        if self.hay_cupo():
            self.cupos -= 1

    def liberar_cupo(self) -> None:
        """
        Suma 1 a la disponibilidad, sin exceder el maximo configurado en la clase.

        Args:
            Ninguno

        Returns:
            None
        """
        if self.cupos < Materia.CUPOS_MAXIMOS:
            self.cupos += 1

    def desasignar_docente(self) -> None:
        """
        Restablece el profesor asignado a 0 (sin docente).

        Args:
            Ninguno

        Returns:
            None
        """
        self.profesor_id = 0

    def tiene_docente(self) -> bool:
        """
        Indica si la asignatura cuenta con un docente asignado.

        Args:
            Ninguno

        Returns:
            bool: True si profesor_id es mayor a 0.
        """
        return self.profesor_id > 0

    def a_diccionario(self) -> Dict[str, Any]:
        """
        Objeto -> diccionario agregando los datos de la asignatura.

        Args:
            Ninguno

        Returns:
            Dict[str, Any]: Datos para el JSON.
        """
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["codigo"] = self.codigo
        datos["creditos"] = self.creditos
        datos["cupos"] = self.cupos
        datos["profesor_id"] = self.profesor_id
        return datos

    def etiqueta(self) -> str:
        """
        Genera el formato de lectura para la asignatura sin mostrar identificadores crudos.

        Args:
            Ninguno

        Returns:
            str: Texto con codigo, nombre, estado de docente y cupos.
        """
        alerta = " ⚠ LLENA" if not self.hay_cupo() else ""
        docente_estado = "Con docente" if self.tiene_docente() else "Sin docente asignado"
        return f"[{self.codigo}] {self.nombre} ({self.creditos} Cr) · [{docente_estado}] · cupos {self.cupos}/{Materia.CUPOS_MAXIMOS}{alerta}"


class Matricula(ModeloBase):
    """Matricula simple: une a un estudiante con una materia en un periodo especifico."""

    def __init__(
        self, id_registro: int, estudiante_id: int, materia_id: int, 
        periodo: str, nota: float = 0.0, fecha: str = ""
    ) -> None:
        """
        Inicializa la relacion transaccional entre estudiante y materia.

        Args:
            id_registro (int): Identificador de la matricula.
            estudiante_id (int): ID de la entidad Estudiante.
            materia_id (int): ID de la entidad Materia.
            periodo (str): Ciclo lectivo o semestre.
            nota (float, opcional): Calificacion. Por defecto 0.0.
            fecha (str, opcional): Fecha de registro. Por defecto se usa la de hoy.

        Returns:
            None
        """
        super().__init__(id_registro)
        self.estudiante_id = int(estudiante_id)
        self.materia_id = int(materia_id)
        self.periodo = periodo
        self.nota = float(nota)
        self.fecha = fecha or date.today().isoformat()

    def esta_aprobada(self) -> bool:
        """
        Consulta la regla estatica de Materia para saber si la nota es aprobatoria.

        Args:
            Ninguno

        Returns:
            bool: True si es mayor o igual a la NOTA_APROBACION.
        """
        return self.nota >= Materia.NOTA_APROBACION

    def estado(self) -> str:
        """
        Convierte la validacion de aprobacion en un estado legible.

        Args:
            Ninguno

        Returns:
            str: 'Aprobada' o 'Reprobada'.
        """
        return "Aprobada" if self.esta_aprobada() else "Reprobada"

    def a_diccionario(self) -> Dict[str, Any]:
        """
        Devuelve el diccionario que se persistira en la transaccion.

        Args:
            Ninguno

        Returns:
            Dict[str, Any]: Diccionario con referencias y calificacion.
        """
        datos = super().a_diccionario()
        datos["estudiante_id"] = self.estudiante_id
        datos["materia_id"] = self.materia_id
        datos["periodo"] = self.periodo
        datos["nota"] = self.nota
        datos["fecha"] = self.fecha
        return datos

    def etiqueta(self) -> str:
        """
        Formato de lectura que resume la situacion academica de la inscripcion.

        Args:
            Ninguno

        Returns:
            str: Historial formateado.
        """
        return (f"{self.fecha} · estudiante {self.estudiante_id} · "
                f"materia {self.materia_id} ({self.periodo}) "
                f"-> Nota: {self.nota} [{self.estado()}]")