from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class Etudiant(models.Model):
    _inherit = 'res.users'

    matricule = fields.Char(string='Matricule', required=True)
    motdepasse = fields.Char(string='Mot de passe', required=True)

    date_entree = fields.Datetime(string='Date de Dernière Modification', readonly=True,
                                  default=fields.Datetime.now)
    niveau_academique = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ], required=True)

    @api.model
    def create(self, vals):
        vals['login'] = vals.get('matricule')
        vals['password'] = vals.get('motdepasse')
        # Vérification si un mot de passe a été fourni, sinon générer un mot de passe par défaut
        if not vals.get('login') or not vals.get('password'):
            ValidationError('pas de matricule ou de mot de passe fournit')

        etudiant = super(Etudiant, self).create(vals)

        group_etudiant = self.env.ref('Enspd_Dms.group_etudiant')

        etudiant.groups_id = [(4, group_etudiant.id)]

        return etudiant
