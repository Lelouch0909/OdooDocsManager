import xlrd
from odoo import fields, models


class ImportEtudiants(models.TransientModel):
    _name = 'import.etudiants'

    file = fields.Binary(string="Fichier Excel")

    def import_from_excel(self):
        workbook = xlrd.open_workbook(file_contents=self.file)
        sheet = workbook.sheet_by_index(0)

        for row in range(1, sheet.nrows):
            matricule = sheet.cell_value(row, 0)
            password = sheet.cell_value(row, 1)

            # Création de l'étudiant avec matricule et mot de passe
            self.env['etudiant'].create({
                'matricule': matricule,
                'password': password,
                'role': 'etudiant',  # On s'assure que le rôle est bien celui d'étudiant
            })
