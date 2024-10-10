import json

from odoo import http
from odoo.http import request, route, Response
import logging

_logger = logging.getLogger(__name__)


class DiplomeController(http.Controller):

    @route('/filedownload', type='json', auth='public', methods=['GET'], csrf=False)
    def get_file(self):
        _logger.warning('Request received for get file')
        data = json.loads(request.httprequest.data)
        file_path = data.get('file_path')

        logging.warning('filePath: %s', file_path)

        if not file_path:
            return {'error': 'filePath is required'}, 400

        diplome_records = request.env['document_diplome'].sudo().search([('file_path', '=', file_path)])

        file_data = [
            {'file_data': d.file}
            for d in diplome_records
        ]
        return file_data
