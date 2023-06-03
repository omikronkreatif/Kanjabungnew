# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    nama_user = fields.Char(string='Username')
    kata_kunci = fields.Char(string='Password')

class AccountAsset(models.Model):
    _inherit = 'account.asset.asset'

    analytic_id = fields.Many2one('account.analytic.account', 'Analytic Account')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: