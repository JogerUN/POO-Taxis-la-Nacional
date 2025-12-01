# ================================================================
# VALIDADORES DE ENTRADA
# Funciones simples que validan datos ingresados por el usuario.
# ================================================================

from datetime import datetime

# -------------------------------------------------------
# 1. Campo obligatorio (string no vacío)
# -------------------------------------------------------
def inputObligatorio(mensaje):
    """
    Pide una entrada al usuario.
    No permite valores vacíos.
    Retorna la cadena limpia.
    """
    while True:
        entrada = input(mensaje).strip()
        if entrada == "":
            print(" ⚠️ Este campo no puede estar vacío. Intente de nuevo.\n")
            continue
        return entrada


# -------------------------------------------------------
# 2. Validación de fecha DD/MM/AAAA
# -------------------------------------------------------
def validarFecha(mensaje):
    """
    Valida fechas en formato DD/MM/YYYY.
    Retorna la fecha string validada.
    """
    formato = "%d/%m/%Y"
    while True:
        entrada = inputObligatorio(mensaje)
        try:
            datetime.strptime(entrada, formato)
            return entrada
        except ValueError:
            print("❌ Fecha inválida. Use el formato DD/MM/AAAA.\n")


# -------------------------------------------------------
# 3. Validación de número entero
# -------------------------------------------------------
def validarEntero(mensaje, allowed_values=None):
    """
    Valida que la entrada sea un número entero.
    Si allowed_values se pasa (lista de strings),
    solo permite esos valores.
    Retorna el entero.
    """
    while True:
        entrada = inputObligatorio(mensaje)

        # Si hay restricciones
        if allowed_values is not None:
            if entrada not in allowed_values:
                print(f"❌ Valor inválido. Opciones permitidas: {allowed_values}\n")
                continue
            return int(entrada)

        # Entero general
        if entrada.isdigit():
            return int(entrada)

        print("❌ Ingrese un número entero válido.\n")


# -------------------------------------------------------
# 4. Convertir placa a mayúsculas
# -------------------------------------------------------
def convertirPlaca(mensaje):
    """
    Pide una placa, valida que no sea vacía,
    y la retorna en mayúsculas sin espacios.
    """
    while True:
        entrada = input(mensaje).strip()
        if entrada == "":
            print(" ⚠️ La placa no puede estar vacía. Intente nuevamente.\n")
            continue
        return entrada.upper()


# -------------------------------------------------------
# 5. Validar que la placa no exista
# -------------------------------------------------------
def convertirFecha(fecha_str):
    """
    Convierte una fecha string en formato DD/MM/AAAA a un objeto datetime.
    """
    format = "%d/%m/%Y"
    return datetime.strptime(fecha_str, format)