import requests

url= "http://localhost:8000/"
nuevo_animal={
        "nombre":"Ortega",
        "especie":"Gato",
        "genero":"Macho",
        "edad":10,
        "peso":20,
}

ruta_post=url+"animales"
post_response=requests.request(method="POST", url=ruta_post,json=nuevo_animal)
print(post_response.text)

print("-----------------------todos-----------------------------")
ruta_get= url+"animales"
get_response=requests.request(method="GET", url=ruta_get)
print(get_response.text)
print("--------------------------POR ESPECIE--------------------------")
ruta_get= url+"animales?especie=Burro"
get_response=requests.request(method="GET", url=ruta_get)
print(get_response.text)
print("---------------------------POR GENERO-------------------------")
ruta_get= url+"animales?genero=Macho"
get_response=requests.request(method="GET", url=ruta_get)
print(get_response.text)

print("---------------------------ACTUALIZANDO-------------------------")
animal_actualizado={
        "nombre":"Ortega",
        "especie":"Tigre",
        "genero":"Macho",
        "edad":30,
        "peso":50,
}

ruta_put=url+"animales/2"
put_response=requests.request(method="PUT", url=ruta_put, json=animal_actualizado)
print(put_response.text)

print("---------------------------eliminando-------------------------")

ruta_delete=url+"animales/1"
delete_response=requests.request(method="DELETE", url=ruta_delete)

print(delete_response.text)