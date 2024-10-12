import base64
from datetime import datetime, timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

from ..services.FileModification import FileModification
from ..services.FileStorage import FileStorage


class Diplome(models.Model):
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

    nom_etudiant = fields.Char(string='Nom de l\'Étudiant', required=True)

    nom_diplome = fields.Char(string='Nom du Diplôme', required=True, default='Diplome d\'ingenieur')

    date_obtention = fields.Date(string='Date d\'Obtention',
                                 default=lambda self: (datetime.now()))

    etablissement = fields.Char(string='Etablissement', required=True, readonly=True,
                                default='Ecole Nationale Supérieure Polytechnique de Douala')

    mention = fields.Selection([
        ('bien', 'bien'),
        ('passable', 'passable'),
        ('tres bien', 'tres bien'),
        ('excellent', 'excellent')
    ], required=True)

    specialite = fields.Selection([
        ('glo', 'ingenieurie logicielle'),
        ('grt', 'ingenieurie reseau'),
        ('gesi', 'ingenieurie  électrique et systemes intelligents'),
        ('ge', 'ingenieurie energétique'),
        ('gc', 'ingenieurie civile'),
        ('gam', 'ingenieurie automobile et mécatronique'),
        ('gm', 'ingenieurie mecanique'),
        ('gp', 'ingenieurie des procedes'),
    ], required=True, readonly=True)

    cycle = fields.Selection([
        ('ingenieur', 'Ingénieur'),
        ('science_de_l_ingenieur', 'Science de l\'Ingénieur'),
    ],
        string="Cycle",
        required=True,
    )
    date_emission = fields.Date(string='Date d\'Emission', default=fields.Datetime.now)

    create_date = fields.Datetime('create_date', readonly=True)

    write_date = fields.Datetime('write_date', readonly=True)

    date_derniere_modif = fields.Datetime(string='Date de Dernière Modification', readonly=True,
                                          default=fields.Datetime.now)

    write_uid = fields.Many2one('res.users', string='write_uid', readonly=True, ondelete='set null')

    type = fields.Char(string='Type', required=True, readonly=True, default='Diplome')

    file = fields.Binary(string="Fichier PDF", required=True)

    file_path = fields.Char(string='Chemin du Fichier', required=True, readonly=True, default='hidden')

    is_sign = fields.Boolean(string='Signé', default=False, readonly=True)

    signature = fields.Binary(string="Signature", default=None)

    qrcode = fields.Binary(string="QRCode", default=None)

    @api.model
    def write(self, vals):
        if self.is_sign and self.env.user.has_group('Enspd_Dms.group_gestionnaire'):
            raise UserError("Vous n'avez pas le droit de modifier un diplôme deja signé.")
        return super(Diplome, self).write(vals)

    @api.model
    def create(self, vals):
        record = super(Diplome, self).create(vals)
        if vals.get('file'):
            file_storage = FileStorage(self.env)
            file_name = f"diplome_{record.id}.pdf"
            file_content = base64.b64decode(vals.get('file'))
            file_path = file_storage.save_file('document_diplome', '', file_content, file_name)
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            record.file_path = f"{base_url}{file_path}"
            FileModification.add_qrcode_to_pdf(record, vals.get('file'), file_path, [10, 380])
        return record

    @api.onchange('matricule')
    def _onchange_matricule_etudiant(self):
        if self.matricule:
            self.cycle = self.matricule.cycle
            self.specialite = self.matricule.filiere
            self.nom_etudiant = self.matricule.nom_etudiant

    @api.onchange('signature')
    def _onchange_signature(self):

        if self.signature and not self.file:
            raise ValidationError("No file provided.")

    def action_sign(self):
        for record in self:
            if record.signature:
                record.write({
                    'is_sign': True,
                    'signature': record.signature  # Assurez-vous que la signature est persistée
                })
                if self.signature:
                    FileModification.add_signature_to_pdf(record, self.file, [250, 10], self.signature)

                else:
                    raise ValidationError("Signature not provided.")
