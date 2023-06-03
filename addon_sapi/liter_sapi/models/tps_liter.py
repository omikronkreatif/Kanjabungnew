from odoo import models, fields, api
class tps_liter(models.Model):
    _name = "tps.liter"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "TPS Liter"
    _rec_name = 'tps_name'

    tps_name = fields.Char('Nama TPS')
    wilayah_id = fields.Many2one('master.wilayah', 'Wilayah')
