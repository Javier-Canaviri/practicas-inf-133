import requests

url= "http://localhost:8000/"
nuevo_paciente={
        "ci":2,
        "nombre":"Luciano",
        "apellido":"Ursino",
        "genero":"Masculino",
        "edad":30,
        "diagnostico":"Gripe",
        "doctor":"Pedro Pérez",
}

ruta_post=url+"pacientes"
post_response=requests.request(method="POST", url=ruta_post,json=nuevo_paciente)
print(post_response.text)

print("-----------------------todos-----------------------------")
ruta_get= url+"pacientes"
get_response=requests.request(method="GET", url=ruta_get)
print(get_response.text)

print("-----------------------ci-----------------------------")
ruta_get_por_ci=url+"pacientes/2"
get_response=requests.request(method="GET",url=ruta_get_por_ci)
print(get_response.text)
print("--------------------------POR diagnostico--------------------------")
ruta_get= url+"pacientes?diagnostico=Diabetes"
get_response=requests.request(method="GET", url=ruta_get)
print(get_response.text)
print("---------------------------POR doctor-------------------------")
ruta_get= url+"pacientes?doctor=Pedro Pérez"
get_response=requests.request(method="GET", url=ruta_get)
print(get_response.text)

print("---------------------------ACTUALIZANDO-------------------------")
paciente_actualizado={
        "nombre":"Michael",
        "apellido":"Ortega",
        "diagnostico":"Gripe",
        "doctor":"Javier Canaviri",
}

ruta_put=url+"pacientes/2"
put_response=requests.request(method="PUT", url=ruta_put, json=paciente_actualizado)
print(put_response.text)

print("---------------------------eliminando-------------------------")

ruta_delete=url+"pacientes/1"
delete_response=requests.request(method="DELETE", url=ruta_delete)

print(delete_response.text)