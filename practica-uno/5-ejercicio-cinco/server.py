from http.server import BaseHTTPRequestHandler,HTTPServer
import json
from urllib. parse import urlparse, parse_qs

animales=[
    {
        "id":1,
        "nombre":"Willy",
        "especie":"Burro",
        "genero":"Hembra",
        "edad":10,
        "peso":20,
    }
]

class AnimalesServices:
    @staticmethod
    def add_animal(data):
        data["id"]= len(animales)+1
        animales.append(data)
        return animales
    
    @staticmethod
    def buscar_por_id(id):
        return next(( animal for animal in animales if animal["id"]==id),None)
    
    
    @staticmethod
    def buscar_por_especie(especie):
        animales_especie= [ animal for animal in animales if animal["especie"]==especie]
        return animales_especie
    
    @staticmethod
    def buscar_por_genero(genero):
        animales_genero= [ animal for animal in animales if animal["genero"]==genero]
        return animales_genero
    
    @staticmethod
    def actualizar_animal(id,data):
        animal= AnimalesServices.buscar_por_id(id)
        if animal:
            animal.update(data)
            return animales
        else:
            None
        
    @staticmethod
    def eliminar_animal(id):
        animales_nuevo=[animal for animal in animales if animal["id"]!=id]
        return animales_nuevo
        
class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler,status,data):
        handler.send_response(status)
        handler.send_header("Content-Type","appliaction/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    
class RestRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        if parsed_path.path == "/animales":
            if "especie" in query_params:
                especie = query_params["especie"][0]
                animales_filtrados = AnimalesServices.buscar_por_especie(especie)
                if animales_filtrados:
                    HTTPResponseHandler.handle_response(self,200,animales_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            
            elif "genero" in query_params:
                genero=query_params["genero"][0]
                animales_fil=AnimalesServices.buscar_por_genero(genero)
                if animales_fil:
                    HTTPResponseHandler.handle_response(self, 200,animales_fil)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            
            else :
                HTTPResponseHandler.handle_response(self,200,animales)
        '''elif parsed_path.path == "/animales/":
            id=int()'''
    def do_POST(self):
        if  self.path== "/animales":
            data =self.read_data()
            animales=AnimalesServices.add_animal(data)
            HTTPResponseHandler.handle_response(self , 201 , animales)
        else:
            HTTPResponseHandler.handle_response(self , 404, {"Error":"Ruta no existente"})
    def do_PUT(self):
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            data = self.read_data()
            animales= AnimalesServices.actualizar_animal(id,data)
            if animales:
                HTTPResponseHandler.handle_response(self, 200, animales)
            else:
                HTTPResponseHandler.handle_response(self,404,{"Error":"Animal no encontrado"})
                
    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            animales= AnimalesServices.eliminar_animal(id)
            if animales :
                HTTPResponseHandler.handle_response(self, 200 , animales)
            else: HTTPResponseHandler.handle_response(self, 404,{"Error":"Ruta no encontrada"})
    
    def read_data(self):
        content_length=int(self.headers["Content-Length"])
        data=self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data
    
def run_server(port=8000):
    try:
        server_address=('',port)
        httpd=HTTPServer(server_address,RestRequestHandler)
        print(f"Iniciando servidor web en http://localhost/{port}/")
        httpd.serve_forever()
    
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__=="__main__":
    run_server()