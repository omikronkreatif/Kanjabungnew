# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import date, datetime
from odoo.exceptions import ValidationError

# classes under  menus of laboratry

class peternak_sapi_anggota_create(models.TransientModel):
    _name = 'peternak.sapi.anggota.create'

    def create_peternak_sapi_anggota(self):
        res_ids = []
        anggota_rqu_obj = self.env['peternak.sapi']
        browse_records = anggota_rqu_obj.browse(self._context.get('active_ids'))
        result = {}
        for browse_record in browse_records:
            if self.env['simpin_syariah.member'].search([('email', '=', browse_record.email)]):
                raise ValidationError(_("The member with email %s already exists!") % browse_record.email)

            peternak_anggota_obj = self.env['simpin_syariah.member']
            res = peternak_anggota_obj.create({'name': self.env['ir.sequence'].next_by_code('simpin_syariah.member'),
                                               'name': browse_record.peternak_name or False,
                                               'email': browse_record.email or False,
                                               'gender': browse_record.gender or False,
                                               'wilayah_id': browse_record.wilayah_id.id,
                                               'jabatan_id': browse_record.jabatan_id.id,
                                               'no_hp': browse_record.phone or False,
                                               'address': browse_record.contact_address or False,
                                               })
            res_ids.append(res.id)
            if res_ids:
                imd = self.env['ir.model.data']
                # write_ids = lab_rqu_obj.browse(self._context.get('active_id'))
                # write_ids.write({'state': 'tested'})
                action = imd.sudo().xmlid_to_object('asa_simpin_syariah.simpin_syariah_member_menu_action')
                list_view_id = imd.sudo().xmlid_to_res_id('asa_simpin_syariah.simpin_syariah_member_tree')
                form_view_id = imd.sudo().xmlid_to_res_id('asa_simpin_syariah.simpin_syariah_member_form')
                result = {
                    'name': action.name,
                    'help': action.help,
                    'type': action.type,
                    'views': [[list_view_id, 'tree'], [form_view_id, 'form']],
                    'target': action.target,
                    'context': action.context,
                    'res_model': action.res_model,
                    'res_id': res.id,

                }

            if res_ids:
                result['domain'] = "[('id','=',%s)]" % res_ids

        return result

    # @api.model
    # def create(self, vals):
    #     anggota_count = self.env['simpin_syariah.member'].search_count([])
    #     if anggota_count > 0:
    #         raise ValidationError(_("Anda sudah membuat anggota sebelumnya. Tidak dapat membuat anggota lagi."))
    #     return super(peternak_sapi_anggota_create, self).create(vals)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
