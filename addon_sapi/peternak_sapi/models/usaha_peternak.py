from odoo import models, fields, api

class usaha_peternak(models.Model):
    _name = "usaha.peternak"
    _description = "Peternak Sapi"
    _rec_name = 'jenis_usaha'

    usaha_name = fields.Char(string='Nama Usaha')
    jenis_usaha = fields.Selection([
        ('sapi', 'Sapi'),
        ('tebu', 'Tebu')
    ], 'Jenis Usaha', required=True, default=False)
