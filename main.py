#!/usr/bin/env python3

from PyPDF2 import PdfReader, PdfWriter
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tempfile
import config

def merge_pdfs(paths, output):
    pdf_writer = PdfWriter()

    for path in paths:
        pdf_reader = PdfReader(path)
        for page_num in range(len(pdf_reader.pages)):
            # Añadir cada página al writer object
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

    # Escribe el PDF resultante en el archivo de salida
    with open(output, 'wb') as out_pdf_file:
        pdf_writer.write(out_pdf_file)

def create_file_without_caratula():
    pdfs = config.pdfs

    # Nombre del archivo de salida
    output_pdf = 'FILE/PDF1.pdf'

    merge_pdfs(pdfs, output_pdf)

def create_file_with_caratula():
    input_pdf = 'FILE/PDF1.pdf'
    pdfs = [
        "0.CARATULA.pdf",
        input_pdf
    ]
    output_pdf = "FILE/PDF2.pdf"
    merge_pdfs(pdfs, output_pdf)

def add_page_number(pdf_path, output_path):
    pdf_reader = PdfReader(pdf_path)
    pdf_writer = PdfWriter()

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]

        # Crea un archivo PDF temporal con el número de página
        packet = tempfile.NamedTemporaryFile(delete=False)
        c = canvas.Canvas(packet, pagesize=letter)
        c.drawString(550, 20, str(page_num + 1))  # Ajusta la posición según necesites
        c.setFont("Helvetica", 12)
        c.save()

        # Mueve el archivo PDF a un objeto PdfReader
        packet.seek(0)
        watermark = PdfReader(packet.name)
        
        # Fusiona el archivo PDF original con el número de página
        page.merge_page(watermark.pages[0])
        
        pdf_writer.add_page(page)

    # Guarda el PDF resultante
    with open(output_path, "wb") as out_pdf_file:
        pdf_writer.write(out_pdf_file)


def main():
  while True:
    # Menu:
    # 1. Crear pre-file (sin caratula)
    # 2. Crear file (con caratula)
    # 3. Enumerar páginas
    print("MENU:")
    print("1: Crear pre-file (sin caratula)")
    print("2: Crear file (con caratula)")
    print("3: Enumerar páginas")
    print("4: Salir")
    opcion = input("Elige una opción: ")

    if opcion == '1':
      create_file_without_caratula()
      exit()
    elif opcion == '2':
      create_file_with_caratula()
      exit()
    elif opcion == '3':
      add_page_number("FILE/PDF2.pdf", "FILE/FILE_CUSTOMER.pdf")
      exit()
    elif opcion == '4':
      print("Saliendo ...")
      exit()
    else:
      print("Opción no válida. Inténtalo de nuevo.")

if __name__ == '__main__':
  main()