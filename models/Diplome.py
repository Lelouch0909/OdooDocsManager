from datetime import datetime
from odoo import models, fields, api

from ..models.Base_document import Base_document


class Diplome(models.Model, Base_document):
    _name = 'document_diplome'
    _description = 'Diplome'
    _order = 'date_emission desc'

    matricule = fields.Many2one(
        'etudiant',
        string="Matricule de l'Étudiant",
        required=True,
        domain="[('matricule', '!=', False)]",
        help="Sélectionner le matricule de l'étudiant"
    )
    nom_diplome = fields.Char(string='Nom du Diplôme', required=True, default='Diplome d\'ingenieur')

    date_obtention = fields.Date(string='Date d\'Obtention',
                                 default=lambda self: (datetime.now()))


    mention = fields.Selection([
        ('bien', 'bien'),
        ('passable', 'passable'),
        ('tres bien', 'tres bien'),
        ('excellent', 'excellent')
    ], required=True)

    date_emission = fields.Date(string='Date d\'Emission', default=fields.Datetime.now)

    create_date = fields.Datetime('create_date', readonly=True)

    write_date = fields.Datetime('write_date', readonly=True)

    date_derniere_modif = fields.Datetime(string='Date de Dernière Modification', readonly=True,
                                          default=fields.Datetime.now)

    write_uid = fields.Many2one('res.users', string='write_uid', readonly=True, ondelete='set null')

    type = fields.Char(string='Type', required=True, readonly=True, default='Diplome')

    specialite = fields.Selection([
        ('glo', 'ingenieurie logicielle'),
        ('grt', 'ingenieurie reseau'),
        ('gesi', 'ingenieurie  électrique et systemes intelligents'),
        ('ge', 'ingenieurie energétique'),
        ('gc', 'ingenieurie civile'),
        ('gam', 'ingenieurie automobile et mécatronique'),
        ('gm', 'ingenieurie mecanique'),
        ('gp', 'ingenieurie des procedes'),
        ('tco', 'none'),

    ], required=True, readonly=True)

    @api.onchange('matricule')
    def _onchange_matricule_etudiant(self):
        super(Diplome, self)._onchange_matricule_etudiant()

        if self.matricule:
            self.specialite = self.matricule.filiere

