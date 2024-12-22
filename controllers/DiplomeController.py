import base64

from odoo import http
from odoo.http import request, route, Response
import logging
import json

_logger = logging.getLogger(__name__)


class DiplomeController(http.Controller):

    @route('/diplomes', type='json', auth='public', methods=['POST'], csrf=False, cors='*')
    def get_diplomes(self):

        _logger.warning('Request received for diplomas')
        data = json.loads(request.httprequest.data)
        matricule = data.get('matricule')

        logging.warning('matricule: %s', matricule)

        if not matricule:
            return {'error': 'matricule is required'}, 400

        # Récupérer tous les diplômes
        diplome_records = request.env['document_diplome'].sudo().search([('matricule', '=', matricule)])
        logging.warning('Diplome records: %s', diplome_records)

        # Renvoyer les diplômes sous forme de dictionnaire
        diplome_data = [{
            'matricule': d.matricule,
            'nom_diplome': d.nom_diplome,
            'date_obtention': d.date_obtention.strftime('%Y-%m-%d') if d.date_obtention else None,
            'mention': d.mention,
            'etablissement': d.etablissement,
            'specialite': d.specialite,
            'cycle': d.cycle,
            'is_sign': d.is_sign,
            'file_path': d.file_path if d.file_path else None,
        } for d in diplome_records]
        return {'diplomes': diplome_data}
