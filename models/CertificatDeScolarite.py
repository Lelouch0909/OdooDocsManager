import base64

from odoo import models, fields, api

from ..services.FileStorage import FileStorage


class CertificatDeScolarite(models.Model):
    _name = 'document_certificat_scolarite'
    _description = 'Certificat de Scolarité'
    _order = 'date_emission desc'

    annee_academique = fields.Char(string='Année Académique', required=True)

    filiere = fields.Selection([
        ('git', 'genie informatique et telecommunications'),
        ('gesi', 'génie électrique et systemes intelligents'),
        ('ge', 'génie energétique'),
        ('gam', 'génie automobile et mécatronique'),
        ('gm', 'génie mécanique'),
        ('gp', 'génie des procédés'),
    ], required=True)

    date_emission = fields.Date(string='Date d\'Emission', default=fields.Datetime.now, required=True)

    create_date = fields.Datetime('create_date', readonly=True)
    write_date = fields.Datetime('write_date', readonly=True)

    date_derniere_modif = fields.Datetime(string='Date de Dernière Modification', readonly=True,
                                          default=fields.Datetime.now)
    write_uid = fields.Many2one('res.users', string='write_uid', readonly=True, ondelete='set null')

    type = fields.Char(string='Type', required=True, readonly=True, default='Certificat_Scolarite')

    file = fields.Binary(string="Fichier PDF")

    file_path = fields.Char(string='Chemin du Fichier', required=True, readonly=True, default='hidden')

    @api.model
    def create(self, vals):
        record = super(CertificatDeScolarite, self).create(vals)

        if vals.get('file'):
            file_storage = FileStorage(self.env)
            file_name = f"certificat_scolarite{record.id}.pdf"
            file_content = base64.b64decode(vals.get('file'))
            file_path = file_storage.save_file('document_certificat_scolarite', '', file_content, file_name)
            record.file_path = file_path
        return record
