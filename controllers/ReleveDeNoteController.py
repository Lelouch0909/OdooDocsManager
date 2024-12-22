import base64

from odoo import http
from odoo.http import request, route, Response
import logging
import json

_logger = logging.getLogger(__name__)


class ReleveDeNoteController(http.Controller):

    @route('/releves', type='json', auth='public', methods=['POST'], csrf=False, cors='*')
    def get_releves(self):

        _logger.warning('Request received for releves')
        data = json.loads(request.httprequest.data)
        matricule = data.get('matricule')

        logging.warning('matricule: %s', matricule)

        if not matricule:
            return {'error': 'matricule is required'}, 400

        releve_records = request.env['document_releve_de_note'].sudo().search([('matricule', '=', matricule)])

        # Renvoyer les diplômes sous forme de dictionnaire
        releve_data = [{
            'matricule': d.matricule,
            'semestre': d.semestre,
            'annee_academique': d.annee_academique,
            'date_emission': d.date_emission.strftime('%Y-%m-%d') if d.annee_academique else None,
            'etablissement': d.etablissement,
            'filiere': d.filiere,
            'cycle': d.cycle,
            'type': d.type,
            'file_path': d.file_path if d.file_path else None,
            'is_sign' : d.is_sign
        } for d in releve_records]
        return {'releves': releve_data}
