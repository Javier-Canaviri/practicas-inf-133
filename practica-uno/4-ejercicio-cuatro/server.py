from http.server import BaseHTTPRequestHandler,HTTPServer
import json


pacientes={}
class Paciente:
    def __init__(self):
        self.ci=None
        self.nombre=None
        self.edad=None
        self.edad=None
        self.edad=None
        self.diagnostico=None
        self.doctor=None
    def __str__(self) :
        return f"CI: {self.ci}, NOMBRE: {self.nombre}, , APELLIDO: {self.edad}, GENERO: {self.edad}, EDAD: {self.edad}, DIAGNOSTICO: {self.diagnostico}, DOCTOR: {self.doctor}"

class PacienteBuilder:
    def __init__(self) :
        self.paciente=Paciente()
    def set_ci(self, tamaño):
        self.paciente.tamaño = tamaño

    def set_nombre(self, nombre):
        self.paciente.nombre = nombre
    
    def set_apellido(self, apellido):
        self.paciente.edad = apellido
        
    def set_genero(self, edad):
        self.paciente.edad = edad
    
    def set_edad(self, edad):
        self.paciente.edad = edad
    def set_diagnostico(self, diagnostico):
        self.paciente.diagnostico = diagnostico
    def set_doctor(self, doctor):
        self.paciente.doctor = doctor

    def get_paciente(self):
        return self.paciente

class Enfermeria:
    def __init__(self, builder):
        self.builder=builder
    def create_paciente(self,ci,nombre,apellido,genero,edad,diagnostico,doctor):
        self.builder.set_ci(ci)
        self.builder.set_nombre(nombre)
        self.builder.set_apellido(apellido)
        self.builder.set_genero(genero)
        self.builder.set_edad(edad)
        self.builder.set_diagnostico(diagnostico)
        self.builder.set_doctor(doctor)
        
        
class PacientesServices:
    def __init__(self) :
        self.builder=PacienteBuilder()
        self.enfermeria=Enfermeria(self.builder)
    
    def buscar_por_ci(ci):
        return next(( paciente for paciente in pacientes if paciente["ci"]==ci),None)
    

    def buscar_por_diagnostico(diagnostico):
        pacientes_por_diagnostico= [ paciente for paciente in pacientes if paciente["diagnostico"]==diagnostico]
        return pacientes_por_diagnostico
    
    def buscar_por_doctor(doctor):
        pacientes_por_doctor= [ paciente for paciente in pacientes if paciente["doctor"]==doctor]
        return pacientes_por_doctor
    
    def create_paciente(self, post_data):
        ci = post_data.get("ci", None)
        nombre = post_data.get("nombre", None)
        apellido = post_data.get("apellido", [])
        genero = post_data.get("genero", None)
        edad = post_data.get("edad", None)
        diagnostico = post_data.get("diagnostico", None)
        doctor = post_data.get("doctor", None)

        paciente = self.enfermeria.create_paciente(ci, nombre, apellido, genero,edad, diagnostico, doctor)
        pacientes[len(paciente) + 1] = paciente
        
        return paciente
    
    def read_paciente(self):
        return {index: paciente.__dict__ for index, paciente in pacientes.items()}

    def update_paciente(self, index, post_data):
        if index in pacientes:
            paciente = pacientes[index]
            ci = post_data.get("ci", None)
            nombre = post_data.get("nombre", None)
            apellido = post_data.get("apellido", None)
            genero = post_data.get("genero", None)
            edad = post_data.get("edad", None)
            diagnostico = post_data.get("diagnostico", None)
            doctor = post_data.get("doctor", None)


            if ci:
                paciente.ci = ci
            if nombre:
                paciente.nombre = nombre
            if apellido:
                paciente.apellido = apellido
            if genero:
                paciente.genero = genero
            if edad:
                paciente.edad = edad
            if diagnostico:
                paciente.diagnostico = diagnostico
            if doctor:
                paciente.doctor = doctor
            
            return paciente
        else:
            return None

    def delete_paciente(self, index):
        if index in pacientes:
            return pacientes.pop(index)
        else:
            return None
        
class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))
    
class PacienteHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = PacientesServices()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/pacientes":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.create_paciente(data)
            HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_GET(self):
        if self.path == "/pacientes":
            response_data = self.controller.read_paciente()
            HTTPDataHandler.handle_response(self, 200, response_data)
        elif self.path.startswith("/pacientes/ci"):
            ci=int(self.path.split("/")[-1])
            response_data=self.controller.buscar_por_ci(ci)
            if response_data:
                HTTPDataHandler.handle_response(self,200, response_data)
            else:
                HTTPDataHandler.handle_response(self,404,{"Error":"Paciente no encontrado"})
        elif self.path.startswith("/pacientes/diagnostico"):
            diagnostico = self.path.split("/")[-1]
            response_data = self.controller.buscar_por_diagnostico(diagnostico)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
        elif self.path.startswith("/pacientes/doctor"):
            doctor = self.path.split("/")[-1]
            response_data = self.controller.buscar_por_doctor(doctor)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            index = int(self.path.split("/")[2])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.update_paciente(index, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "Índice de taco no válido"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            index = int(self.path.split("/")[2])
            deleted_paciente = self.controller.delete_paciente(index)
            if deleted_paciente:
                HTTPDataHandler.handle_response(
                    self, 200, {"message": "Taco eliminado correctamente"}
                )
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "Índice de taco no válido"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    

def run(server_class=HTTPServer, handler_class=PacienteHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()