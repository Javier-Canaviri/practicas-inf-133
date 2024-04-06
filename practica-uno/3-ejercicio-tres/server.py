from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

pacientes = [
    {
        "ci":1,
        "nombre":"Carlos",
        "apellido":"Canaviri",
        "edad":21,
        "genero":"masculino",
        "diagnostico":"fractura",
        "doctor":"Javier Huaranca",
    },
    {
        "ci":2,
        "nombre":"Luciano",
        "apellido":"Ursino",
        "edad":23,
        "genero":"masculino",
        "diagnostico":"Diabetes",
        "doctor":"Pedro Pérez",
    },
] 

class PacientesService:
    @staticmethod
    def add_patient(data):
        pacientes.append(data)
        return pacientes
    
    @staticmethod
    def buscar_por_nombre(nombre):
        return [paciente for paciente in pacientes if paciente["nombre"]== nombre]
    
    @staticmethod
    def buscar_por_ci(ci):
        return next((paciente for paciente in pacientes if paciente["ci"]== ci),
        None,)
    
    @staticmethod
    def buscar_por_enfermedad(diagnostico):
        return ([paciente for paciente in pacientes if paciente["diagnostico"]== diagnostico])
    
    @staticmethod
    def buscar_por_doctor(doctor):
        return [paciente for paciente in pacientes if paciente["doctor"]== doctor]
    
    @staticmethod
    def update_patient(ci, data):
        paciente=PacientesService.buscar_por_ci(ci)
        if paciente:
            paciente.update(data)
            return pacientes
        else:
            return None
    
    @staticmethod
    def delete_patient(ci):
        global pacientes
        new_pacientes=[paciente for paciente in pacientes if int(paciente["ci"])!= ci]
        return new_pacientes


class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type","application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
        
        

class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path= urlparse(self.path)
        query_params=parse_qs(parsed_path.query)
        
        if parsed_path.path == "/pacientes":
            if "nombre" in query_params:
                nombre= query_params['nombre'][0]
                pacientes_filtrados = PacientesService.buscar_por_nombre(nombre)
                if pacientes_filtrados != []:
                    HTTPResponseHandler.handle_response(
                        self,200, pacientes_filtrados
                    )
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            elif "diagnostico" in query_params:
                diagnostico = query_params['diagnostico'][0]
                pacientes_filtrados1=PacientesService.buscar_por_enfermedad(diagnostico)
                if pacientes_filtrados1:
                    HTTPResponseHandler.handle_response(self, 200, pacientes_filtrados1)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            elif "doctor" in query_params:
                doctor = query_params['doctor'][0]
                pacientes_filtrados2=PacientesService.buscar_por_doctor(doctor)
                if pacientes_filtrados2:
                    HTTPResponseHandler.handle_response(self, 200, pacientes_filtrados2)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
                
            else:
                HTTPResponseHandler.handle_response(self, 200, pacientes)

        elif self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            paciente=PacientesService.buscar_por_ci(ci)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, [paciente])
            else:
                HTTPResponseHandler.handle_response(self,204, [])
    
    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data= self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data
    
    def do_POST(self):
        if self.path== "/pacientes":
            data = self.read_data()
            pacientes = PacientesService.add_patient(data)
            HTTPResponseHandler.handle_response(self, 201, data)
        else :
            HTTPResponseHandler.handle_response(self, 404, {"Error":"Ruta no Existente"})
            
    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            id =int(self.path.split("/")[-1])
            data=self.read_data()
            pacientes=PacientesService.update_patient(id, data)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error":"Paciente no Encontrado"})
    
    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci =int(self.path.split("/")[-1])
            pacientes= PacientesService.delete_patient(ci)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error":"Ruta no Encontrada"})
                
def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd= HTTPServer(server_address,RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apangando servidor web")
        httpd.socket.close()
        
if __name__=="__main__":
    run_server()
