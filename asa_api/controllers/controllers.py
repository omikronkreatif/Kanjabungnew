# -*- coding: utf-8 -*-
from odoo import http, models
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)


class AsaApi(http.Controller):

	@http.route('/change_password', auth="user", type='json',cors='*')
	def change_password(self, **rec):
		result = {}
		if request.jsonrequest :
			if rec.get('new_password') and rec.get('user_id'):
				user = request.env['res.users'].sudo().search([('id','=',rec.get('user_id'))])
				user.write({'password': rec['new_password']})
				return ({'result':'success'})
			return ({'result':'User Or Password is Empty'})
		return ({'result':'Failed Check Your Parameter'})
