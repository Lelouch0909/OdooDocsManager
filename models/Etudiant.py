from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class Etudiant(models.Model):
    _name = 'etudiant'
    _description = 'Etudiant'
    _order = 'date_entree desc'

    _sql_constraints = [
        ('matricule_unique', 'UNIQUE(matricule)', 'Le matricule doit être unique.')
    ]

    nom_etudiant = fields.Char(string='Nom', required=True)

    matricule = fields.Char(string='Matricule', required=True)

    date_entree = fields.Datetime(string='Date de Dernière Modification', readonly=True,
                                  default=fields.Datetime.now)
    diplome_ids = fields.One2many('document_diplome', 'matricule', string="Diplômes")
    releve_de_note_ids = fields.One2many('document_releve_de_note', 'matricule', string="Relevés de notes")
    certificat_de_scolarite_ids = fields.One2many('document_certificat_scolarite', 'matricule', string="Certificats")

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

    cycle = fields.Selection([
        ('ingenieur', 'Ingénieur'),
        ('science_de_l_ingenieur', 'Science de l\'Ingénieur'),
    ],
        string="Cycle",
        required=True
    )
    niveau_academique = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ], required=True, default='1')
