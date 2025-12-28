# ===========================================================
#  GENERADOR DE PDF PARA FICHA INTEGRADA DEL VEHÍCULO (OO)
# ===========================================================

import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
from database.Old_connection import crearConexion
from repositorios.vehiculo_repo import RepositorioVehiculo

def generarFichaVehiculoPDF(placa):
    """
    Genera un PDF completo con la información del vehículo,
    el conductor asignado y el historial de mantenimientos.
    """

    connection = crearConexion()
    repo = RepositorioVehiculo(connection)

    vehiculo = repo.buscar_por_placa(placa)

    if vehiculo is None:
        print(f"❌ No existe un vehículo con la placa {placa}.")
        return

    # Crear carpeta si no existe
    ruta_salida = r"C:\POO\Programs\TAXIS_LA_NACIONAL\output\pdfs"
    os.makedirs(ruta_salida, exist_ok=True)

    archivo_pdf = os.path.join(ruta_salida, f"Ficha_Vehiculo_{placa}.pdf")

    # --- 1. Buscar conductor asignado ---
    cursor = connection.cursor()
    cursor.execute("""
        SELECT nombreCompleto, telefono, correoElectronico, direccion
        FROM conductores WHERE placaVehiculo=?
    """, (placa,))
    conductor = cursor.fetchone()

    # --- 2. Buscar mantenimientos ---
    cursor.execute("""
        SELECT numeroOrden, nombreProveedor, nitProveedor,
               descripcionServicio, valorFacturado, fechaServicio
        FROM mantenimientos WHERE placaVehiculo=?
        ORDER BY fechaServicio DESC
    """, (placa,))
    mantenimientos = cursor.fetchall()

    # --- 3. CREACIÓN PDF ---
    c = canvas.Canvas(archivo_pdf, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, "🚖 FICHA INTEGRADA DE VEHÍCULO")

    c.line(50, height - 60, width - 50, height - 60)

    # ---------- SECCIÓN VEHÍCULO ----------
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 90, "📘 Información del vehículo:")
    c.setFont("Helvetica", 11)

    info = vehiculo.infVehiculo()

    etiquetas = [
        f"Placa: {info[0]}",
        f"Marca: {info[1]}",
        f"Referencia: {info[2]}",
        f"Modelo: {info[3]}",
        f"Chasis: {info[4]}",
        f"Motor: {info[5]}",
        f"Color: {info[6]}",
        f"Concesionario: {info[7]}",
        f"Fecha compra: {info[8]}",
        f"Garantía: {info[9]} meses",
        f"Fecha póliza: {info[10]} ({info[11]})",
        f"Fecha SOAT: {info[12]} ({info[13]})",
        f"Activo: {'Sí' if info[14] == 1 else 'No'}"
    ]

    y = height - 110
    for e in etiquetas:
        c.drawString(60, y, e)
        y -= 15

    # -------- SECCIÓN CONDUCTOR --------
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "🧍 Conductor asignado:")
    c.setFont("Helvetica", 11)
    y -= 20

    if conductor:
        c.drawString(60, y, f"Nombre: {conductor[0]}")
        y -= 15
        c.drawString(60, y, f"Teléfono: {conductor[1]}")
        y -= 15
        c.drawString(60, y, f"Correo: {conductor[2]}")
        y -= 15
        c.drawString(60, y, f"Dirección: {conductor[3]}")
    else:
        c.drawString(60, y, "Sin conductor asignado.")

    # -------- SECCIÓN MANTENIMIENTOS --------
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "🧾 Historial de mantenimientos:")
    y -= 20
    c.setFont("Helvetica", 10)

    if not mantenimientos:
        c.drawString(60, y, "No hay registros de mantenimiento.")
    else:
        for m in mantenimientos:
            if y < 100:
                c.showPage()
                y = height - 80
                c.setFont("Helvetica", 10)

            c.drawString(60, y, f"Orden #{m[0]} | Fecha: {m[5]}")
            y -= 12
            c.drawString(80, y, f"Proveedor: {m[1]} ({m[2]})")
            y -= 12
            c.drawString(80, y, f"Servicio: {m[3]}")
            y -= 12
            c.drawString(80, y, f"Valor: ${m[4]:,.0f}")
            y -= 18

    # Pie de página
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(
        width / 2, 40,
        f"Generado automáticamente — {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    )

    c.save()
    print(f"✅ PDF generado exitosamente en:\n{archivo_pdf}")