from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler

# Define la función del servicio
def sumar(int1,int2):
    return(int1+int2)

def resta(int1,int2):
    return(int1-int2)

def multiplicacion(int1,int2):
    return(int1*int2)

def division(int1,int2):
    return(int1/int2)

# Creamos la ruta del servidor SOAP
dispatcher = SoapDispatcher(
    "ejemplo-soap-server",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)

# Registramos el servicio
dispatcher.register_function(
    "SumarDosNumeros",
    sumar,
    returns={"resultado": int},
    args={"int1":int, "int2":int},
    
)
dispatcher.register_function(
    "RestarDosNumeros",
    resta,
    returns={"resultado": int},
    args={"int1":int, "int2":int},
    
)
dispatcher.register_function(
    "MultiplicarDosNumeros",
    multiplicacion,
    returns={"resultado": int},
    args={"int1":int, "int2":int},
    
)
dispatcher.register_function(
    "DividirDosNumeros",
    division,
    returns={"resultado": float},
    args={"int1":int, "int2":int},
    
)




# Iniciamos el servidor HTTP
try:
    server = HTTPServer(("0.0.0.0", 8000), SOAPHandler)
    server.dispatcher = dispatcher
    print("Servidor SOAP iniciado en http://localhost:8000/")
    server.serve_forever()
except KeyboardInterrupt:
    print("Apagando servidor web")
    server.socket.close()