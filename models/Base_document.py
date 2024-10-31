import logging

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import base64

from ..services.FileModification import FileModification
from ..services.FileStorage import FileStorage


class Base_document(models.AbstractModel):
    _name = 'base_document'
    _description = 'Base Document'

    matricule = fields.Many2one(
        'etudiant',
        string="Matricule de l'Étudiant",
        required=True,
        domain="[('matricule', '!=', False)]",
        help="Sélectionner le matricule de l'étudiant"
    )

    nom_etudiant = fields.Char(string='Nom de l\'Étudiant', required=True)

    cycle = fields.Selection([
        ('ingenieur', 'Ingénieur'),
        ('science_de_l_ingenieur', 'Science de l\'Ingénieur'),
    ],
        string="Cycle",
        required=True,
    )
    create_date = fields.Datetime('create_date', readonly=True)
    write_date = fields.Datetime('write_date', readonly=True)

    date_derniere_modif = fields.Datetime(string='Date de Dernière Modification', readonly=True,
                                          default=fields.Datetime.now)
    write_uid = fields.Many2one('res.users', string='write_uid', readonly=True, ondelete='set null')

    is_sign = fields.Boolean(string='Signé', default=False, readonly=True)

    signature = fields.Binary(string="Signature", default=None)

    qrcode = fields.Binary(string="QRCode", default=None)
    file = fields.Binary(string="Fichier PDF", required=True)

    file_path = fields.Char(string='Chemin du Fichier', required=True, readonly=True, default='hidden')

    @api.model
    def create(self, vals):
        logging.warning(f"Entre dans la fonction create, {self.matricule.nom_etudiant}")

        vals.update({"nom_etudiant": self.matricule.nom_etudiant,
                     "cycle": self.matricule.cycle,
                     "specialite": self.matricule.filiere})
        logging.warning(vals.get("nom_etudiant"))
        logging.warning(vals.get("cycle"))
        logging.warning(vals.get("matricule"))
        logging.warning(vals.get("specialite"))
        record = super(Base_document, self).create(vals)
        child_class_name = self._name
        if vals.get('file'):
            file_storage = FileStorage(self.env)
            file_name = f"{child_class_name}_{record.id}.pdf"
            file_content = base64.b64decode(vals.get('file'))
            file_path = file_storage.save_file(child_class_name, '', file_content, file_name)
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            record.file_path = f"{base_url}{file_path}"
            positions = {
                'document_certificat_scolarite': [10, 380],
                'document_diplome': [10, 380],
                'document_releve_de_note': [10, 380],
            }
            FileModification.add_qrcode_to_pdf(record, vals.get('file'), file_path, positions.get(child_class_name))
        return record

    @api.model
    def write(self, vals):
        logging.warning("Entre dans la fonction write")

        if self.is_sign and self.env.user.has_group('Enspd_Dms.group_gestionnaire'):
            raise UserError("Vous n'avez pas le droit de modifier un document deja signé.")
        return super(Base_document, self).write(vals)

    @api.onchange('signature')
    def _onchange_signature(self):

        if self.signature and not self.file:
            raise ValidationError("No file provided.")

    def action_sign(self):
        logging.warning("Entre dans la fonction action_sign")
        for record in self:
            if record.signature:
                positions = {
                    'document_certificat_scolarite': [250, 10],
                    'document_diplome': [250, 10],
                    'document_releve_de_note': [250, 10],
                }
                record.write({
                    'is_sign': True,
                    'signature': record.signature
                })
                if self.signature:
                    FileModification.add_signature_to_pdf(record, self.file, positions, self.signature)

                else:
                    raise ValidationError("Signature not provided.")

    @api.onchange('matricule')
    def _onchange_matricule_etudiant(self):
        if self.matricule:
            self.cycle = self.matricule.cycle
            self.nom_etudiant = self.matricule.nom_etudiant
