import requests
# Definir la URL del servidor GraphQL
url = 'http://localhost:8000/graphql'

# Definir la consulta GraphQL simple
query = """
    {
        plantas{
            id 
            nombre 
            especie
            edad
            altura
            frutos
            
        }
    }
"""
# Solicitud POST al servidor GraphQL
response = requests.post(url, json={'query': query})
print(response.text)


# Definir la consulta GraphQL con parametros
query = """
    {
        planta_por_id(id: 1){
            id 
            nombre 
            especie
            edad
            altura
            frutos
        }
    }
"""

response = requests.post(url, json={'query': query})
print(response.text)

# Solicitud POST al servidor GraphQL
response = requests.post(url, json={'query': query})
print(response.text)

# Definir la consulta GraphQL para crear nuevo estudiante
query_crear = """
mutation {
        crearPlanta( nombre = "Rosa2",especie = "Rosa Rugosa",edad = 2,altura=50,frutos=True) {
            planta {
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
"""

response_mutation = requests.post(url, json={'query': query_crear})
print(response_mutation.text)

# Lista de todos los estudiantes
response = requests.post(url, json={'query': query})
print(response.text)

# Definir la consulta GraphQL para eliminar un estudiante
query_eliminar = """
mutation {
        deletePlanta(id: 1) {
            planta {
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
"""

response_mutation = requests.post(url, json={'query': query_eliminar})
print(response_mutation.text)

# Lista de todos los estudiantes
response = requests.post(url, json={'query': query})
print(response.text)
