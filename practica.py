# def crear(self, datos):
#         """Matricula a un estudiante restando un cupo y devuelve un mensaje con nombres reales."""
#         error = self.validar_creacion(datos)
#         if error:
#             return False, error

#         # 1. Obtenemos los objetos reales de estudiante y materia
#         estudiante = self.estudiantes.obtener(int(datos["estudiante_id"]))
#         materia = self.materias.obtener(int(datos["materia_id"]))
        
#         matricula = Matricula(self.siguiente(),
#                               estudiante.id,
#                               materia.id,
#                               str(datos.get("periodo", "Actual")).strip().upper())

#         # 2. Restamos el cupo
#         materia.ocupar_cupo()
#         self.materias.guardar()                
        
#         self.lista.append(matricula)
#         self.guardar()                          
        
#         # 3. CONSTRUIMOS EL MENSAJE CON NOMBRES REALES
#         # Viajamos desde materias hacia profesores para obtener el nombre del docente
#         if materia.profesor_id > 0:
#             profesor = self.materias.profesores.obtener(materia.profesor_id)
#             nombre_docente = profesor.nombre_completo() if profesor else "Docente Eliminado"
#         else:
#             nombre_docente = "Sin docente asignado"
            
#         # Armamos el texto final
#         mensaje_exito = (f"El estudiante {estudiante.nombre_completo()} "
#                          f"se inscribio en {materia.nombre} "
#                          f"con el docente {nombre_docente}")
        
#         return True, mensaje_exito