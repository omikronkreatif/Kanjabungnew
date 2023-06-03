# -*- coding: utf-8 -*-
from odoo import http, models
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)


class SapiApi(http.Controller):

	@http.route('/change_id_eartag', auth="user", type='json',cors='*')
	def change_password(self, **rec):
		result = {}
		if request.jsonrequest :
			if rec.get('peternak_id') :
				peternak = rec['peternak_id']
			else :
				peternak = False
			if rec.get('petugas_id') :
				petugas = rec['petugas_id']
			else :
				petugas = False
			if rec.get('id_sapi') :
				sapi = rec['id_sapi']
			else :
				sapi = False
			if rec.get('eartag_id_lama') :
				eartag_lama = rec['eartag_id_lama']
			else :
				eartag_lama = False
			if rec.get('eartag_id_baru') :
				eartag_baru = rec['eartag_id_baru']
			else :
				eartag_baru = False
			if rec.get('tgl_layanan') :
				tgl_layanan = rec['tgl_layanan']
			else :
				tgl_layanan = False
			if rec.get('cat_petugas') :
				cat_petugas = rec['cat_petugas']
			else :
				cat_petugas = False

			value_data = {  'peternak_id': peternak,
							'petugas_id': petugas,
							'sapi_id': sapi,
							'eartag_id': eartag_lama,
							'eartag_id_baru': eartag_baru,
							'tgl_layanan': tgl_layanan,
							'cat_petugas': cat_petugas
							  }

			new_record = request.env['form.gis'].sudo().create(value_data)

			if rec.get('id_sapi') and rec.get('eartag_id_baru') :
				sapi = request.env['sapi'].sudo().search([('id','=',rec['id_sapi'])])
				if sapi :
					sapi.sudo().write({'eartag_id': rec['eartag_id_baru']})
					return ({'result':'Success Create History Ganti ID Sapi and Update ID Eartag'})
				else :
					return ({'result':'Data Sapi Tidak Ditemukan'})
			return ({'result':'ID Peternak Or New ID Ear Tag is Empty'})
		return ({'result':'Failed Check Your Parameter'})
