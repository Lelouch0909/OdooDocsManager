import base64
import logging
from io import BytesIO

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import pandas as pd

from ..services.AuthService import create_client_user


# Importer un fichier excel avec les champs nom matricule filiere(gle,grt,gesi,ge,gc,gam,gm,gp,tco)

class ListeEtudiant(models.Model):
    _name = 'liste_etudiant'
    _description = 'liste des etudiants'
    _order = 'annee desc'

    annee = fields.Datetime(string='Annee',
                            default=fields.Datetime.now, required=True)
    # A modifier

    filiere = fields.Selection([
        ('glo', 'génie logicielle'),
        ('grt', 'génie reseau'),
        ('gesi', 'génie électrique et systemes intelligents'),
        ('ge', 'génie energétique'),
        ('gam', 'génie automobile et mécatronique'),
        ('gc', 'genie civile'),
        ('gm', 'génie mécanique'),
        ('gp', 'génie des procédés'),
        ('tco', 'tronc commun'),

    ], required=True)

    file = fields.Binary(string="Fichier Excel", required=True)

    cycle = fields.Selection([
        ('ingenieur', 'Ingénieur'),
        ('science_de_l_ingenieur', 'Science de l\'Ingénieur'),
    ],
        string="Cycle",
        required=True
    )
    niveau_academique = fields.Selection([
        ('1', '1'),
        ('3', '3'),
    ], required=True, default='1')

    @api.model
    def create(self, vals):
        record = super(ListeEtudiant, self).create(vals)

        if not vals.get('file'):
            raise ValueError("Aucun fichier chargé.")

        file = vals.get('file')

        file_content = base64.b64decode(file)
        df = pd.read_excel(BytesIO(file_content))
        filieres = ['glo', 'grt', 'gesi', 'ge', 'gc', 'gam', 'gm', 'gp', 'tco']
        errors = []

        logging.warning(f"Import de {len(df)} étudiants")

        for index, row in df.iterrows():
            matricule = row.get('matricule')
            nom = row.get('nom')
            filiere = row.get('filiere')

            # Vérifier si tous les champs requis sont présents
            if not matricule or not nom or not filiere:
                errors.append(f"Étudiant à la ligne {index + 1} : Matricule ou nom ou filiere manquant.")
                continue
            if filiere not in filieres:
                errors.append(f"Étudiant à la ligne {index + 1} : Filiere non valide.")
                continue
            # Vérifier si l'étudiant existe déjà
            existing_student = self.env['etudiant'].search([('matricule', '=', matricule)], limit=1)
            if existing_student:
                errors.append(
                    f"Étudiant à la ligne {index + 1} : Un étudiant avec le matricule {matricule} existe déjà.")
                continue
        logging.warning(f"Import terminé avec {len(errors)} erreurs")
        # Si des erreurs ont été collectées, lever une exception
        if errors:
            error_message = "\n".join(errors)
            raise UserError(f"Erreur(s) lors de l'importation des étudiants :\n{error_message}")
        else:
            for index, row in df.iterrows():
                matricule = row.get('matricule')
                nom = row.get('nom')
                try:
                    create_client_user(matricule, nom)
                except Exception as e:
                    raise ValidationError(
                        "impossible d ajouter l'etudiant a l api distant, verifiez votre connection internet ou contactez un administrateur")
                filiere = row.get('filiere')
                logging.warning(f"Création de l'étudiant {matricule}")
                self.env['etudiant'].create({
                    'matricule': matricule,
                    'nom_etudiant': nom,
                    'filiere': filiere,
                    'niveau_academique': vals.get('niveau_academique'),
                    'cycle': vals.get('cycle'),
                    'date_entree': vals.get('date_entree'),
                })
        return record
