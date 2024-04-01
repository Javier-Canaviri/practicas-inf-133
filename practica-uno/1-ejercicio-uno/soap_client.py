from zeep import Client

client = Client('http://localhost:8000')
int1 = 8
int2 = 4

# Realizar la suma
suma = client.service.SumarDosNumeros(int1, int2)
print("Suma:", int1, "+", int2, "=", suma)

# Realizar la resta
resta = client.service.RestarDosNumeros(int1, int2)
print("Resta:", int1, "-", int2, "=", resta)

#Realizar la multiplicación
multiplicacion = client.service.MultiplicarDosNumeros(int1, int2)
print("Multiplicación:", int1, "*", int2, "=", multiplicacion)

#Realizar la división
division = client.service.DividirDosNumeros(int1, int2)
print("División:", int1, "/", int2, "=", division)
