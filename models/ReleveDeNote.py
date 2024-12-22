import base64

from odoo import models, fields, api


class ReleveDeNote(models.Model):
    _name = 'document_releve_de_note'
    _description = 'Releve de Note'
    _order = 'date_emission desc'
    _inherit = 'base_document'

    id = fields.Integer(string='ID', required=True)
    matricule = fields.Many2one(
        'etudiant',
        string="Matricule de l'Étudiant",
        required=True,
        domain="[('matricule', '!=', False)]",
        help="Sélectionner le matricule de l'étudiant"
    )
    semestre = fields.Char(string='Semestre', required=True)

    annee_academique = fields.Char(string='Année Académique', required=True)

    filiere = fields.Selection([
        ('gesi', 'génie électrique et systemes intelligents'),
        ('ge', 'génie energétique'),
        ('gam', 'génie automobile et mécatronique'),
        ('gm', 'génie mécanique'),
        ('gp', 'génie des procédés'),
        ('tco', 'tronc commun'),
        ('glo','genie logicielle'),
        ('grt', 'genie reseau et telecom'),

    ], required=True)

    date_emission = fields.Date(string='Date d\'Emission', default=fields.Datetime.now, required=True)

    type = fields.Char(string='Type', required=True, readonly=True, default='Releve_Note')

    @api.onchange('matricule')
    def _onchange_matricule_etudiant(self):
        super(ReleveDeNote, self)._onchange_matricule_etudiant()

        if self.matricule:
            self.filiere = self.matricule.filiere
