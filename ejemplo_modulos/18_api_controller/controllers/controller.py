import json
import jinja2
from odoo import http
from odoo.http import Response
import logging
_logger = logging.getLogger(__name__)

# loader = jinja2.PackageLoader('odoo.addons.master_credit_base', 'views/web')
env = jinja2.Environment(loader=False, autoescape=True)


class Master(http.Controller):

    @http.route('/api/partner/info/<nif>/<token>', auth='public', cors='*')
    def get_coach(self, nif,token):
        valid_token = http.request.env['api.token'].sudo().search([('token', '=', token), ('is_active', '=', True)], limit=1)
        if valid_token:
            PartnerObj = http.request.env['res.partner'].sudo()
            response = PartnerObj.prepare_api_partner_values(nif=nif)
            if not response:
                response = {'error': 'No se ha encontrado el partner con NIF: {}'.format(nif)}
        else:
            response = {'error': 'Token invaido'}
        if response:
            return Response(
                json.dumps(response),
                headers={
                    'Content-Type': 'application/json',
                    'Referrer-Policy': 'no-referrer-when-downgrade',
                }
            )
        return Response(status=404)

