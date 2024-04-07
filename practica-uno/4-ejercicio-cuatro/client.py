import requests

url= "http://localhost:8000/"
headers={'Content-type':'application/json'}

nuevo_paciente={
        "ci":2,
        "nombre":"Luciano",
        "apellido":"Ursino",
        "genero":"Masculino",
        "edad":30,
        "diagnostico":"Gripe",
        "doctor":"Pedro Pérez",
}

# GET /tacos
response = requests.get(url)
print(response.json())


print("----------------------------POST-------------------------------")
# POST  
mi_paciente = {
        "ci":1,
        "nombre":"Luciano",
        "apellido":"Ursino",
        "genero":"Masculino",
        "edad":30,
        "diagnostico":"Diabetes",
        "doctor":"Pedro Pérez",
}
response = requests.post(url, json=mi_paciente, headers=headers)
mi_paciente = {
        "ci":2,
        "nombre":"Michael",
        "apellido":"Ortega",
        "genero":"Masculino",
        "edad":20,
        "diagnostico":"Gripe",
        "doctor":"Pedro Pérez",
}
response = requests.post(url, json=mi_paciente, headers=headers)
print(response.json())

print("----------------------------GET-------------------------------")
# GET 
response = requests.get(url)
print(response.json())

print("------------------------------PUT-----------------------------")
# PUT /tacos/1
edit_paciente = {
        "nombre":"Guillermo",
        "apellido":"Viscarra",
        "genero":"Masculino",
        "edad":20,
        "diagnostico":"Gripe",
        "doctor":"Pedro Pérez",
}
response = requests.put(url+ "/1", json=edit_paciente, headers=headers)
print(response.json())

print("----------------------------GET-------------------------------")
# GET /tacos
response = requests.get(url)
print(response.json())

print("------------------GET POR DIAGNOSTICO-------------------------")
# GET /pacientes/diagnostico/{diagnostico}
diagnostico = "Diabetes"
response = requests.get(url + f"pacientes/diagnostico/{diagnostico}")
print(response.json())

print("----------------------GET POR CI-----------------------------")
# GET /pacientes/ci/{ci}
ci = 2
response = requests.get(url + f"pacientes/ci/{ci}")
print(response.json())

print("------------------GET POR DOCTOR-------------------------------")
# GET /pacientes/doctor/{doctor}
doctor = "Pedro Pérez"
response = requests.get(url + f"pacientes/doctor/{doctor}")
print(response.json())
print("---------------------------DELETE--------------------------------")
# DELETE /tacos/1

response = requests.delete(url + "/1")
print(response.json())

print("------------------------------GET-----------------------------")
# GET /tacos
response = requests.get(url)
print(response.json())
print("-----------------------------------------------------------")
