from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String, Int, Boolean, List, Schema, Field, Mutation


class Planta(ObjectType):
    id = Int()
    nombre = String()
    especie = String()
    edad = Int()
    altura=Int()
    frutos=Boolean()


class Query(ObjectType):
    
    plantas = List(Planta)
    planta_por_id = Field(Planta, id=Int())

    def resolve_plantas(root, info):
        return plantas
        
    def resolve_planta_por_id(root, info, id):
        for planta in plantas:
            if planta.id == id:
                return planta
        return None

class CrearPlanta(Mutation):
    class Arguments:
        nombre = String()
        especie = String()
        edad = Int()
        altura=Int()
        frutos=Boolean()

    planta = Field(Planta)

    def mutate(root, info, nombre, especie, edad, altura, frutos):
        nueva_planta = Planta(
            id=len(plantas) + 1, 
            nombre = nombre,
            especie = especie,
            edad = edad,
            altura=altura,
            frutos=frutos,
        ),
        plantas.append(nueva_planta)

        return CrearPlanta(planta=nueva_planta)

class DeletePlanta(Mutation):
    class Arguments:
        id = Int()

    planta = Field(Planta)

    def mutate(root, info, id):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                plantas.pop(i)
                return DeletePlanta(planta=planta)
        return None

class Mutations(ObjectType):

    crear_planta = CrearPlanta.Field()
    delete_planta = DeletePlanta.Field()

plantas = [
    Planta(
        id=1, 
        nombre = "Rosa",
        especie = "Rosa Rugosa",
        edad = 2,
        altura=50,
        frutos=True
    ),
]

schema = Schema(query=Query, mutation=Mutations)


class GraphQLRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    
    def do_POST(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            print(data)
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GraphQLRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()
 