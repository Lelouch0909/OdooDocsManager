import base64
import qrcode
from io import BytesIO

from PIL import Image
from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class FileModification:

    @staticmethod
    def add_signature_to_pdf(record, file, positions, signature):
        # Charger le PDF existant
        pdf_reader = PdfReader(BytesIO(base64.b64decode(file)))
        pdf_writer = PdfWriter()

        # Convertir la signature en image
        signature_image = Image.open(BytesIO(base64.b64decode(signature)))
        signature_image = signature_image.convert("RGBA")
        signature_image.save('signature_temp.png', format='PNG')

        for page_number, page in enumerate(pdf_reader.pages):
            temp_pdf_path = "temp_signed_page.pdf"

            c = canvas.Canvas(temp_pdf_path, pagesize=letter)
            c.drawImage('signature_temp.png', positions[0], positions[1], width=signature_image.width * 40 / 100,
                        height=signature_image.height * 40 / 100, mask='auto')
            c.showPage()
            c.save()

            signed_pdf_reader = PdfReader(temp_pdf_path)
            signed_page = signed_pdf_reader.pages[0]
            page.merge_page(signed_page)

            pdf_writer.add_page(page)

        # Sauvegarder le PDF modifié
        output_stream = BytesIO()
        pdf_writer.write(output_stream)

        # Retourner le contenu du nouveau PDF
        new_pdf = base64.b64encode(output_stream.getvalue())
        record.file = new_pdf
        return new_pdf

    @staticmethod
    def add_qrcode_to_pdf(record, file, filepath, positions):
        # Definir les donnees du Qr
        data = "https://enspddocverification.centry/?url=" + filepath

        # Creer un qrcode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=1,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Convertir l'image QR code en bytes
        img_byte_array = BytesIO()
        img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)
        img_binary = base64.b64encode(img_byte_array.getvalue()).decode('utf-8')

        FileModification.add_signature_to_pdf(record, file, positions, img_binary)
        record.qrcode = img_binary
        return img_binary
