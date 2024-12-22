import base64

from odoo import http
from odoo.http import request, route, Response
import logging
import json

_logger = logging.getLogger(__name__)


class CertificatDeScolariteController(http.Controller):

    @route('/certificats', type='json', auth='public', methods=['POST'], csrf=False, cors='*')
    def get_certificats(self):

        _logger.warning('Request received for certificats')
        data = json.loads(request.httprequest.data)
        matricule = data.get('matricule')

        logging.warning('matricule: %s', matricule)

        if not matricule:
            return {'error': 'matricule is required'}, 400
        certificat_records = request.env['document_certificat_scolarite'].sudo().search([('matricule', '=', matricule)])

        # Renvoyer les diplômes sous forme de dictionnaire
        certificat_data = [{
            'matricule': d.matricule,
            'annee_academique': d.annee_academique,
            'date_emission': d.date_emission.strftime('%Y-%m-%d') if d.annee_academique else None,
            'etablissement': d.etablissement,
            'filiere': d.filiere,
            'cycle': d.cycle,
            'type': d.type,
            'is_sign': d.is_sign,
            'file_path': d.file_path if d.file_path else None,
        } for d in certificat_records]
        return {'certificats': certificat_data}
