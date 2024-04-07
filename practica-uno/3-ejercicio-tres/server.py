from http.server import BaseHTTPRequestHandler,HTTPServer
import json
from urllib. parse import urlparse, parse_qs

pacientes=[
    {
        "ci":1,
        "nombre":"Willy",
        "apellido":"Burro",
        "genero":"Masculino",
        "edad":10,
        "diagnostico":"Diabetes",
        "doctor":"Pedro Pérez",
    }
]

class PacientesServices:
    @staticmethod
    def add_paciente(data):
        pacientes.append(data)
        return pacientes
    
    @staticmethod
    def buscar_por_ci(ci):
        return next(( paciente for paciente in pacientes if paciente["ci"]==ci),None)
    
    
    @staticmethod
    def buscar_por_diagnostico(diagnostico):
        pacientes_por_diagnostico= [ paciente for paciente in pacientes if paciente["diagnostico"]==diagnostico]
        return pacientes_por_diagnostico
    
    @staticmethod
    def buscar_por_doctor(doctor):
        pacientes_por_doctor= [ paciente for paciente in pacientes if paciente["doctor"]==doctor]
        return pacientes_por_doctor
    
    @staticmethod
    def actualizar_paciente(ci,data):
        paciente= PacientesServices.buscar_por_ci(ci)
        if paciente:
            paciente.update(data)
            return pacientes
        else:
            None
        
    @staticmethod
    def eliminar_paciente(ci):
        pacientes_nuevo=[paciente for paciente in pacientes if paciente["ci"]!=ci]
        return pacientes_nuevo
        
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
        
        if parsed_path.path == "/pacientes":
            if "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                pacientes_filtrados = PacientesServices.buscar_por_diagnostico(diagnostico)
                if pacientes_filtrados:
                    HTTPResponseHandler.handle_response(self,200,pacientes_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            
            elif "doctor" in query_params:
                doctor=query_params["doctor"][0]
                pacientes_fil=PacientesServices.buscar_por_doctor(doctor)
                if pacientes_fil:
                    HTTPResponseHandler.handle_response(self, 200,pacientes_fil)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            
            else :
                HTTPResponseHandler.handle_response(self,200,pacientes)
        elif self.path.startswith("/pacientes/"):
            id = int(self.path.split("/")[-1])
            paciente = PacientesServices.buscar_por_ci(id)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, [paciente])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )
            
    def do_POST(self):
        if  self.path== "/pacientes":
            data =self.read_data()
            pacientes=PacientesServices.add_paciente(data)
            HTTPResponseHandler.handle_response(self , 201 , pacientes)
        else:
            HTTPResponseHandler.handle_response(self , 404, {"Error":"Ruta no existente"})
    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            data = self.read_data()
            pacientes= PacientesServices.actualizar_paciente(ci,data)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(self,404,{"Error":"Paciente no encontrado"})
                
    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            pacientes= PacientesServices.eliminar_paciente(ci)
            if pacientes :
                HTTPResponseHandler.handle_response(self, 200 , pacientes)
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