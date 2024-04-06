import requests

url="http://localhost:8000/"
#CREAR UN PACIENTE
nuevo_paciente={
    "ci":6,
    "nombre":"Lautaro",
    "apellido":"Cobra",
    "edad":26,
    "genero":"masculino",
    "diagnostico":"Diabetes",
    "doctor":"Pedro Pérez",
},

ruta_post=url+"pacientes"
post_response=requests.request(method="POST", url=ruta_post, json=nuevo_paciente)
print(post_response.text)
print("----------------------------------------------------")

#LISTA DE TODOS LOS PACIENTES
ruta_get=url+"pacientes"
get_response =requests.request(method="GET", url=ruta_get)
print(get_response.text)
print("----------------------------------------------------")

#BUSCAR PACIENTE POR CI
ruta_get_por_ci= url+"pacientes/1"
get_response = requests.request(method="GET", url=ruta_get_por_ci)
print(get_response.text)
print("----------------------------------------------------")

#LISTAR A LOS PACIENTES CON DIAGNOSTICO DIABETES
ruta_get_diagnostico = url + "pacientes?diagnostico=Diabetes"
get_response = requests.request(method="GET", url=ruta_get_diagnostico)
print(get_response.text)
print("----------------------------------------------------")

#LISTAR A LOS PACIENTES QUE ATIENDE EL DOCTOR PEDRO PEREZ
ruta_get_doctor = url + "pacientes?doctor=Pedro Pérez"
get_response = requests.request(method="GET", url=ruta_get_doctor)
print(get_response.text)
print("----------------------------------------------------")

#ACTUALIZAR LA INFORMACION DE UN PACIENTE
paciente_actualizado={
    "nombre":"David",
    "apellido":"Martinez",
    "edad":23,
    "genero":"masculino",
    "diagnostico":"Diabetes",
    "doctor":"Pedro Pérez",
}
ruta_put_paciente= url+ "pacientes/6"
put_response=requests.request(method="PUT", url=ruta_put_paciente, json=paciente_actualizado)
print(put_response.text)
print("----------------------------------------------------")

#ELIMINAR UN PACIENTE
ruta_delete=url+"pacientes/6"
delete_response=requests.request(method="DELETE", url=ruta_delete)
print(delete_response.text)


print("----------------------------------------------------")
#LISTAR A LOS PACIENTES CON DIAGNOSTICO DIABETES
ruta_get_diagnostico = url + "pacientes?diagnostico=Diabetes"
get_response = requests.request(method="GET", url=ruta_get_diagnostico)
print(get_response.text)

