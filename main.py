from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import EstudianteController, ProfesorController, MateriaController, MatriculaController

# Se crea un solo controlador de cada tipo.
# Inyeccion de dependencias: materias recibe profesores; matriculas recibe estudiantes y materias.
estudiantes = EstudianteController()
profesores = ProfesorController()
materias = MateriaController(profesores)
matriculas = MatriculaController(estudiantes, materias)


# AYUDAS DE PANTALLA

def pausa() -> None:
    """
    Detiene la ejecucion hasta que el usuario presione Enter.

    Args:
        Ninguno

    Returns:
        None
    """
    input("\nPresione Enter para continuar...")


def pedir_entero(etiqueta: str) -> int:
    """
    Devuelve un entero o None si la entrada no es un numero valido.

    Args:
        etiqueta (str): Texto mostrado al solicitar la entrada.

    Returns:
        int o None: Numero entero validado o None si fallo.
    """
    try:
        return int(input(etiqueta))
    except ValueError:
        return None


def mostrar_lista(objetos: list, vacio: str = "No hay registros todavia.") -> None:
    """
    Recorre e imprime la coleccion de objetos mediante su metodo __str__.

    Args:
        objetos (list): Coleccion de instancias a imprimir.
        vacio (str, opcional): Mensaje si la lista esta vacia.

    Returns:
        None
    """
    if not objetos:
        imprimir_info(vacio)
        return
    for objeto in objetos:
        print(f"  {objeto}")
    imprimir_info(f"Total: {len(objetos)}")


def mostrar_detalle(objeto: object) -> None:
    """
    Imprime en pantalla los atributos de un objeto a partir de su diccionario.

    Args:
        objeto (object): Instancia del modelo a inspeccionar.

    Returns:
        None
    """
    for clave, valor in objeto.a_diccionario().items():
        print(f"  {str(clave).replace('_', ' ').capitalize():<16}: {valor}")


# MENU DE ESTUDIANTES

def crear_estudiante() -> None:
    """
    Solicita entradas por consola, llama al controlador y formatea la confirmacion.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("CREAR ESTUDIANTE")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "carnet": input("Carnet: "),
        "carrera": input("Carrera: "),
    }
    exito, resultado = estudiantes.crear(datos)
    if exito:
        imprimir_exito(f"Estudiante registrado: {resultado.nombre_completo()} ({resultado.carnet or 'Sin carnet'})")
    else:
        imprimir_error(resultado)
    pausa()


def listar_estudiantes() -> None:
    """
    Muestra la lista de estudiantes registrados.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("ESTUDIANTES")
    mostrar_lista(estudiantes.leer(), "Todavia no hay estudiantes registrados.")
    pausa()


def buscar_estudiante() -> None:
    """
    Busca estudiantes por termino de coincidencia y despliega los resultados.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, apellido, email, carnet o carrera: ")
    encontrados = estudiantes.buscar(termino)
    mostrar_lista(encontrados, f"Ningun estudiante coincide con '{termino}'.")
    pausa()


def ver_estudiante() -> None:
    """
    Busca y presenta el detalle completo de un estudiante por su clave primaria.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("VER ESTUDIANTE POR ID")
    id_estudiante = pedir_entero("Id: ")
    if id_estudiante is None:
        imprimir_error("Debe ingresar un identificador numerico valido.")
        return pausa()

    estudiante = estudiantes.obtener(id_estudiante)
    if estudiante is None:
        imprimir_error("Estudiante no encontrado.")
    else:
        mostrar_detalle(estudiante)
    pausa()


def actualizar_estudiante() -> None:
    """
    Permite modificar los atributos de un estudiante existente.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    id_estudiante = pedir_entero("Id: ")
    if id_estudiante is None:
        imprimir_error("Debe ingresar un identificador numerico valido.")
        return pausa()

    estudiante = estudiantes.obtener(id_estudiante)
    if estudiante is None:
        imprimir_error("Estudiante no encontrado.")
        return pausa()

    imprimir_info(f"Editando: {estudiante.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "apellido", "email", "carnet", "carrera"):
        actual = getattr(estudiante, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    exito, resultado = estudiantes.actualizar(id_estudiante, cambios)
    if exito:
        imprimir_exito(f"Estudiante {resultado.id} actualizado exitosamente.")
    else:
        imprimir_error(resultado)
    pausa()


def eliminar_estudiante() -> None:
    """
    Remueve un estudiante previa confirmacion en pantalla.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    id_estudiante = pedir_entero("Id: ")
    if id_estudiante is None:
        imprimir_error("Debe ingresar un identificador numerico valido.")
        return pausa()

    estudiante = estudiantes.obtener(id_estudiante)
    if estudiante is None:
        imprimir_error("Estudiante no encontrado.")
        return pausa()

    imprimir_info(f"Se eliminara: {estudiante.etiqueta()}")
    if confirmar("¿Confirma?"):
        exito, resultado = estudiantes.eliminar(id_estudiante)
        if exito:
            imprimir_exito(resultado)
        else:
            imprimir_error(resultado)
    else:
        imprimir_info("Operacion cancelada.")
    pausa()


# MENU DE PROFESORES

def crear_profesor() -> None:
    """
    Solicita entradas por consola, crea el docente y presenta el resultado.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("CREAR PROFESOR")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "titulo": input("Titulo (ej. Ing., PhD): "),
        "especialidad": input("Especialidad: "),
    }
    exito, resultado = profesores.crear(datos)
    if exito:
        imprimir_exito(f"Profesor registrado: {resultado.etiqueta()}")
    else:
        imprimir_error(resultado)
    pausa()


def listar_profesores() -> None:
    """
    Muestra todos los docentes registrados.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("PROFESORES")
    mostrar_lista(profesores.leer(), "Todavia no hay profesores registrados.")
    pausa()


def buscar_profesor() -> None:
    """
    Busca docentes por palabra clave.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("BUSCAR PROFESOR")
    termino = input("Nombre, apellido, email, titulo o especialidad: ")
    mostrar_lista(profesores.buscar(termino), f"Ningun profesor coincide con '{termino}'.")
    pausa()


def ver_profesor() -> None:
    """
    Presenta la ficha del docente y las materias asignadas bajo su cargo.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("VER PROFESOR POR ID")
    id_profesor = pedir_entero("Id: ")
    if id_profesor is None:
        imprimir_error("Debe ingresar un identificador numerico valido.")
        return pausa()

    profesor = profesores.obtener(id_profesor)
    if profesor is None:
        imprimir_error("Profesor no encontrado.")
        return pausa()

    mostrar_detalle(profesor)

    asignadas = materias.materias_por_docente(profesor.id)
    print("\n  Materias que imparte:")
    if asignadas:
        for m in asignadas:
            print(f"    - [{m.codigo}] {m.nombre} ({m.creditos} Cr)")
    else:
        print("    (Ninguna materia asignada actualmente)")

    pausa()


def actualizar_profesor() -> None:
    """
    Permite modificar los atributos de un docente existente.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("ACTUALIZAR PROFESOR")
    id_profesor = pedir_entero("Id: ")
    if id_profesor is None:
        imprimir_error("Debe ingresar un identificador numerico valido.")
        return pausa()

    profesor = profesores.obtener(id_profesor)
    if profesor is None:
        imprimir_error("Profesor no encontrado.")
        return pausa()

    imprimir_info(f"Editando: {profesor.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "apellido", "email", "titulo", "especialidad"):
        actual = getattr(profesor, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    exito, resultado = profesores.actualizar(id_profesor, cambios)
    if exito:
        imprimir_exito(f"Profesor {resultado.id} actualizado exitosamente.")
    else:
        imprimir_error(resultado)
    pausa()


def eliminar_profesor() -> None:
    """
    Remueve un profesor previa confirmacion y desasigna sus materias.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("ELIMINAR PROFESOR")
    id_profesor = pedir_entero("Id: ")
    if id_profesor is None:
        imprimir_error("Debe ingresar un identificador numerico valido.")
        return pausa()

    profesor = profesores.obtener(id_profesor)
    if profesor is None:
        imprimir_error("Profesor no encontrado.")
        return pausa()

    imprimir_info(f"Se eliminara: {profesor.etiqueta()}")
    if confirmar("¿Confirma? (Las materias a su cargo quedaran sin docente asignado)"):
        exito, resultado = profesores.eliminar(id_profesor)
        if exito:
            imprimir_exito(resultado)
        else:
            imprimir_error(resultado)
    else:
        imprimir_info("Operacion cancelada.")
    pausa()


# MENU DE MATERIAS

def crear_materia() -> None:
    """
    Solicita datos por consola para registrar una nueva asignatura.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("CREAR MATERIA")
    datos = {
        "nombre": input("Nombre: "),
        "codigo": input("Codigo: "),
        "creditos": input("Creditos: "),
        "cupos": input("Cupos iniciales [Enter = 30]: "),
    }
    exito, resultado = materias.crear(datos)
    if exito:
        imprimir_exito(f"Materia registrada: [{resultado.codigo}] {resultado.nombre} ({resultado.cupos} cupos)")
    else:
        imprimir_error(resultado)
    pausa()


def listar_materias() -> None:
    """
    Muestra el listado de materias del catalogo.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("MATERIAS")
    mostrar_lista(materias.leer(), "Todavia no hay materias creadas.")
    pausa()


def buscar_materia() -> None:
    """
    Busca materias por nombre o codigo oficial.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("BUSCAR MATERIA")
    termino = input("Nombre o codigo: ")
    mostrar_lista(materias.buscar(termino), "Sin coincidencias.")
    pausa()


def ver_materia() -> None:
    """
    Muestra los detalles de la materia resolviendo el nombre del docente si lo tiene asignado.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("VER MATERIA POR ID")
    id_materia = pedir_entero("Id: ")
    if id_materia is None:
        imprimir_error("Debe ingresar un identificador numerico valido.")
        return pausa()

    materia = materias.obtener(id_materia)
    if materia is None:
        imprimir_error("Materia no encontrada.")
        return pausa()

    mostrar_detalle(materia)

    if materia.tiene_docente():
        docente = profesores.obtener(materia.profesor_id)
        nombre_doc = docente.nombre_completo() if docente else "Docente no localizado"
        print(f"  Profesor a cargo: {nombre_doc}")
    else:
        print("  Profesor a cargo: Sin docente asignado")

    pausa()


def actualizar_materia() -> None:
    """
    Modifica campos basicos de la materia.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("ACTUALIZAR MATERIA")
    id_materia = pedir_entero("Id: ")
    if id_materia is None:
        imprimir_error("Debe ingresar un identificador numerico valido.")
        return pausa()

    materia = materias.obtener(id_materia)
    if materia is None:
        imprimir_error("Materia no encontrada.")
        return pausa()

    imprimir_info(f"Editando: {materia.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "codigo", "creditos", "cupos"):
        actual = getattr(materia, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    exito, resultado = materias.actualizar(id_materia, cambios)
    if exito:
        imprimir_exito(f"Materia {resultado.codigo} actualizada exitosamente.")
    else:
        imprimir_error(resultado)
    pausa()


def eliminar_materia() -> None:
    """
    Elimina una materia del catalogo.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("ELIMINAR MATERIA")
    id_materia = pedir_entero("Id: ")
    if id_materia is None:
        imprimir_error("Debe ingresar un identificador numerico valido.")
        return pausa()

    materia = materias.obtener(id_materia)
    if materia is None:
        imprimir_error("Materia no encontrada.")
        return pausa()

    imprimir_info(f"Se eliminara: {materia.etiqueta()}")
    if confirmar("¿Confirma?"):
        exito, resultado = materias.eliminar(id_materia)
        if exito:
            imprimir_exito(resultado)
        else:
            imprimir_error(resultado)
    else:
        imprimir_info("Operacion cancelada.")
    pausa()


def asignar_docente_materia() -> None:
    """
    Asigna un docente a una asignatura y formatea el mensaje con los nombres reales.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("ASIGNAR DOCENTE A MATERIA")
    imprimir_info("Materias disponibles:")
    mostrar_lista(materias.leer())
    imprimir_info("Docentes disponibles:")
    mostrar_lista(profesores.leer())

    id_materia = pedir_entero("\nId de la materia: ")
    id_profesor = pedir_entero("Id del profesor: ")

    if id_materia is None or id_profesor is None:
        imprimir_error("Los IDs deben ser numeros enteros.")
        return pausa()

    exito, resultado = materias.asignar_docente(id_materia, id_profesor)
    if exito:
        materia_obj, profesor_obj = resultado
        imprimir_exito(f"El docente {profesor_obj.nombre_completo()} fue asignado a la materia {materia_obj.nombre} [{materia_obj.codigo}].")
    else:
        imprimir_error(resultado)
    pausa()


def desasignar_docente_materia() -> None:
    """
    Remueve la asignacion docente de una materia.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("QUITAR DOCENTE DE MATERIA")
    con_docente = [m for m in materias.leer() if m.tiene_docente()]
    if not con_docente:
        imprimir_info("No hay materias con docentes asignados actualmente.")
        return pausa()

    imprimir_info("Materias con docente asignado:")
    mostrar_lista(con_docente)

    id_materia = pedir_entero("\nId de la materia a desasignar: ")
    if id_materia is None:
        imprimir_error("Debe ingresar un numero entero.")
        return pausa()

    exito, resultado = materias.desasignar_docente(id_materia)
    if exito:
        imprimir_exito(f"Se removio la asignacion docente de la materia {resultado.codigo}.")
    else:
        imprimir_error(resultado)
    pausa()


# MENU DE MATRICULAS

def registrar_matricula() -> None:
    """
    Procesa la matricula y formatea el mensaje de exito resolviendo estudiante, materia y docente.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("REGISTRAR MATRICULA")
    imprimir_info("Estudiantes:")
    mostrar_lista(estudiantes.leer())
    imprimir_info("Materias:")
    mostrar_lista(materias.leer())

    datos = {
        "estudiante_id": pedir_entero("\nId del estudiante: "),
        "materia_id": pedir_entero("Id de la materia: "),
        "periodo": input("Periodo (ej. 2026-1): "),
    }

    if datos["estudiante_id"] is None or datos["materia_id"] is None:
        imprimir_error("Los IDs deben ser numeros enteros.")
        return pausa()

    exito, resultado = matriculas.crear(datos)
    if not exito:
        imprimir_error(resultado)
        return pausa()

    estudiante = estudiantes.obtener(resultado.estudiante_id)
    materia = materias.obtener(resultado.materia_id)
    docente = profesores.obtener(materia.profesor_id) if materia.tiene_docente() else None

    nombre_estudiante = estudiante.nombre_completo() if estudiante else "Estudiante Desconocido"
    nombre_materia = materia.nombre if materia else "Materia Desconocida"
    nombre_docente = docente.nombre_completo() if docente else "Sin docente asignado"

    imprimir_exito(
        f"El estudiante {nombre_estudiante} se inscribio en {nombre_materia} "
        f"con el docente {nombre_docente}."
    )
    imprimir_info(f"Cupos restantes en la materia: {materia.cupos}")
    pausa()


def listar_matriculas() -> None:
    """
    Muestra todas las matriculas activas.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("MATRICULAS ACTIVAS")
    mostrar_lista(matriculas.leer(), "Todavia no hay inscripciones.")
    pausa()


def asentar_calificacion() -> None:
    """
    Registra la nota de una matricula y muestra el estado academico resultante.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("ASENTAR CALIFICACION")
    id_matricula = pedir_entero("Id de la matricula: ")
    if id_matricula is None:
        imprimir_error("Debe ingresar un identificador numerico valido.")
        return pausa()

    matricula = matriculas.obtener(id_matricula)
    if matricula is None:
        imprimir_error(f"No existe la matricula con ID {id_matricula}.")
        return pausa()

    nota = input(f"Ingrese la nota (0 a 20) [Actual: {matricula.nota}]: ").strip()
    exito, resultado = matriculas.actualizar(id_matricula, {"nota": nota})
    if exito:
        imprimir_exito(f"Calificacion asentada: {resultado.nota} -> Estado: [{resultado.estado()}]")
    else:
        imprimir_error(resultado)
    pausa()


def ver_reporte() -> None:
    """
    Consume la estructura de datos pura del controlador y la formatea en pantalla.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("REPORTE ACADEMICO")
    id_estudiante = pedir_entero("Id del estudiante: ")
    if id_estudiante is None:
        imprimir_error("Debe ingresar un ID valido.")
        return pausa()

    reporte = matriculas.reporte_academico(id_estudiante)
    if reporte is None:
        imprimir_error("El estudiante no existe.")
        return pausa()

    est = reporte["estudiante"]
    inscripciones = reporte["inscripciones"]

    print(f"BOLETIN ACADEMICO - {est.nombre_completo()}")
    print(f"Carrera: {est.carrera or 'Sin carrera asignada'}")
    print("-" * 50)

    if not inscripciones:
        print("El estudiante no tiene materias registradas.")
    else:
        for item in inscripciones:
            print(f"{item['periodo']} | [{item['materia_codigo']}] {item['materia_nombre']} -> Nota: {item['nota']} [{item['estado']}]")

    print("-" * 50)
    pausa()


def anular_matricula() -> None:
    """
    Anula una matricula y confirma la liberacion del cupo.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("ANULAR MATRICULA")
    id_matricula = pedir_entero("Id de la matricula: ")
    if id_matricula is None:
        imprimir_error("Debe ingresar un identificador numerico valido.")
        return pausa()

    matricula = matriculas.obtener(id_matricula)
    if matricula is None:
        imprimir_error(f"No existe la matricula con ID {id_matricula}.")
        return pausa()

    imprimir_info(f"Se anulara: {matricula.etiqueta()}")
    if confirmar("Se liberara el cupo en la materia. ¿Confirma?"):
        exito, resultado = matriculas.eliminar(id_matricula)
        if exito:
            imprimir_exito(resultado)
        else:
            imprimir_error(resultado)
    else:
        imprimir_info("Operacion cancelada.")
    pausa()


def resumen() -> None:
    """
    Calcula y presenta metricas globales del sistema academico.

    Args:
        Ninguno

    Returns:
        None
    """
    imprimir_titulo("RESUMEN GENERAL")
    print(f"  Estudiantes : {len(estudiantes.leer())}")
    print(f"  Carreras    : {', '.join(estudiantes.carreras_registradas()) or '-'}")
    print(f"  Profesores  : {len(profesores.leer())}")
    print(f"  Materias    : {len(materias.leer())}")

    llenas = [m for m in materias.leer() if not m.hay_cupo()]
    print(f"  Sin cupos   : {', '.join(m.codigo for m in llenas) or 'ninguna'}")
    print(f"  Matriculas  : {len(matriculas.leer())}")
    pausa()


# MENUS: DICCIONARIOS tecla -> (texto, funcion)

MENU_ESTUDIANTES = {
    "1": ("Crear estudiante", crear_estudiante),
    "2": ("Ver todos", listar_estudiantes),
    "3": ("Buscar", buscar_estudiante),
    "4": ("Ver por id", ver_estudiante),
    "5": ("Actualizar", actualizar_estudiante),
    "6": ("Eliminar", eliminar_estudiante),
    "0": ("Volver", None),
}

MENU_PROFESORES = {
    "1": ("Registrar profesor", crear_profesor),
    "2": ("Ver todos", listar_profesores),
    "3": ("Buscar", buscar_profesor),
    "4": ("Ver por id", ver_profesor),
    "5": ("Actualizar", actualizar_profesor),
    "6": ("Eliminar", eliminar_profesor),
    "0": ("Volver", None),
}

MENU_MATERIAS = {
    "1": ("Crear materia", crear_materia),
    "2": ("Ver todas", listar_materias),
    "3": ("Buscar", buscar_materia),
    "4": ("Ver por id", ver_materia),
    "5": ("Actualizar", actualizar_materia),
    "6": ("Eliminar", eliminar_materia),
    "7": ("Asignar docente", asignar_docente_materia),
    "8": ("Quitar docente", desasignar_docente_materia),
    "0": ("Volver", None),
}

MENU_MATRICULAS = {
    "1": ("Inscribir estudiante", registrar_matricula),
    "2": ("Ver todas", listar_matriculas),
    "3": ("Asentar calificacion", asentar_calificacion),
    "4": ("Ver reporte academico", ver_reporte),
    "5": ("Anular matricula", anular_matricula),
    "0": ("Volver", None),
}


def ejecutar_menu(titulo: str, opciones: dict) -> None:
    """
    Bucle generico para renderizar y despachar los submenus dinamicamente.

    Args:
        titulo (str): Encabezado del submenu.
        opciones (dict): Mapeo de teclas a tuplas (texto, funcion).

    Returns:
        None
    """
    while True:
        imprimir_titulo(titulo)
        for tecla, (texto, _funcion) in opciones.items():
            print(f"  {tecla}. {texto}")
        print()

        tecla = input("Opcion: ").strip()
        if tecla not in opciones:
            imprimir_error("Opcion no valida.")
            pausa()
            continue

        _texto, funcion = opciones[tecla]
        if funcion is None:
            break
        funcion()


def main() -> None:
    """
    Punto de entrada principal del sistema academico.

    Args:
        Ninguno

    Returns:
        None
    """
    while True:
        imprimir_titulo("SISTEMA ACADEMICO")
        print("  1. Estudiantes")
        print("  2. Profesores")
        print("  3. Materias")
        print("  4. Matriculas")
        print("  5. Resumen")
        print("  0. Salir\n")

        tecla = input("Opcion: ").strip()
        if tecla == "1":
            ejecutar_menu("GESTION DE ESTUDIANTES", MENU_ESTUDIANTES)
        elif tecla == "2":
            ejecutar_menu("GESTION DE PROFESORES", MENU_PROFESORES)
        elif tecla == "3":
            ejecutar_menu("GESTION DE MATERIAS", MENU_MATERIAS)
        elif tecla == "4":
            ejecutar_menu("GESTION DE MATRICULAS", MENU_MATRICULAS)
        elif tecla == "5":
            resumen()
        elif tecla == "0":
            imprimir_info("¡Hasta luego! 👋")
            break
        else:
            imprimir_error("Opcion no valida.")
            pausa()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")