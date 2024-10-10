import base64
from odoo.exceptions import ValidationError


class FileStorage:

    def __init__(self, env):
        self.env = env

    def save_file(self, model_name, record_id, file_data, file_name):
        if not file_data:
            raise ValidationError("No file data provided.")

        # Créer une entrée ir.attachment pour stocker le fichier
        attachment = {
            'name': file_name,
            'type': 'binary',
            'datas': base64.b64encode(file_data).decode('utf-8'),
            'res_model': model_name,  # Le modèle lié, par exemple 'diplome' ou 'releve_de_note'
            'res_id': record_id,  # ID de l'enregistrement lié
            'mimetype': 'application/pdf',

        }

        # Créer l'attachment dans la base de données
        attachment_id = self.env['ir.attachment'].create(attachment)

        return f'/web/content/{attachment_id.id}'

