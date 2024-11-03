import base64

from odoo import models, fields, api


class CertificatDeScolarite(models.Model):
    _name = 'document_certificat_scolarite'
    _inherit = 'base_document'

    _description = 'Certificat de Scolarité'
    _order = 'date_emission desc'

    annee_academique = fields.Char(string='Année Académique', required=True)
    matricule = fields.Many2one(
        'etudiant',
        string="Matricule de l'Étudiant",
        required=True,
        domain="[('matricule', '!=', False)]",
        help="Sélectionner le matricule de l'étudiant"
    )
    filiere = fields.Selection([
        ('git', 'genie informatique et telecommunications'),
        ('gesi', 'génie électrique et systemes intelligents'),
        ('ge', 'génie energétique'),
        ('gam', 'génie automobile et mécatronique'),
        ('gm', 'génie mécanique'),
        ('gp', 'génie des procédés'),
        ('tco', 'tronc commun'),

    ], required=True)

    date_emission = fields.Date(string='Date d\'Emission', default=fields.Datetime.now, required=True)

    type = fields.Char(string='Type', required=True, readonly=True, default='Certificat_Scolarite')

    @api.onchange('matricule')
    def _onchange_matricule_etudiant(self):
        super(CertificatDeScolarite, self)._onchange_matricule_etudiant()

        if self.matricule:
            self.filiere = self.matricule.filiere
