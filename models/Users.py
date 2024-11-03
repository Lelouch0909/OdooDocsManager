import base64

from odoo import models, fields, api


class Users(models.Model):
    _inherit = 'res.users'

    role = fields.Selection(
        [('administrateur', 'Administrateur'), ('gestionnaire', 'Gestionnaire')],
        string='Rôle', required=True, default='gestionnaire', )
    saved_signature = fields.Binary("Signature enregistrée",default=None)

    @api.model
    def create(self, vals):
        user = super(Users, self).create(vals)

        if vals.get('role') == 'administrateur':
            group_administrateur = self.env.ref('Enspd_Dms.group_administrateur')
            user.groups_id = [(4, group_administrateur.id)]
        elif vals.get('role') == 'gestionnaire':
            group_gestionnaire = self.env.ref('Enspd_Dms.group_gestionnaire')
            user.groups_id = [(4, group_gestionnaire.id)]

        return user
