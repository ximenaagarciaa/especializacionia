#El nombre de la estudiante

#La calificación del curso

#El titulo de la segunda tarea

#Si la primera tarea está completada

estudiante = {

    "nombre": "Ana",

    "edad": 24,

    "curso": {

        "nombre": "Python",

        "calificacion": 92

    },

    "tareas": [

        {

            "titulo": "Variables",

            "completada": True

        },

        {

            "titulo": "Consumo de APIs",

            "completada": False

        }

    ]

}

print(f'Estudiante: {estudiante["nombre"]}, TITULO: {estudiante["curso"]["calificacion"]}')
print(f'Estudiante: {estudiante["tareas"][1]["titulo"]}')
print(f'Estudiante: {estudiante["tareas"][0]["completada"]}')
if estudiante["tareas"][0]["completada"]:
    print ("la primera esta completada ")
    