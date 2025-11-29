from datetime import datetime

class inputObligatorio:
    
    def __init__ (self, mensaje):
        while True:
            entrada = input(mensaje).strip()
            if entrada == "":
                print(" ⚠️ Lo sentimos el campo no puede estar vacio, porfavor intente de nuevo.")
                print("Regresando al menu anterior...")
                return None
            else:
                return entrada
            
class validarFecha: 
    def __init__(self, mensaje):
        """Valida formato DD/MM/AAAA."""
        while True:
            entrada = inputObligatorio(mensaje)
            try:
                formatoFechas = "%d/%m/%Y"
                datetime.strptime(entrada, formatoFechas)
                return entrada
            except ValueError:
                print("❌ Fecha invalida. Use el formato DD/MM/AAAA.")

class validarEntero:
    def __init__(self, mensaje):
        """Verifica que sea un número entero."""
        while True:
            entrada = inputObligatorio(mensaje)
            if entrada.isdigit():
                return int(entrada)
            else:
                print("❌ Ingrese un numero entero.")

class convertirPlaca:
    def __init__(slef, mensaje):
        """Verifica que sea un número entero."""
        while True:
            entrada = input(mensaje).strip()
            if entrada == "":
                print(" ⚠️ Lo sentimos el campo no puede estar vacio, porfavor intente de nuevo. ")
            else:
                return entrada.upper()
