from odoo import api, fields, models, _

class UserType(models.Model):
    _inherit = 'res.users'

    tipe_user = fields.Selection([
        ('anggota', 'Anggota'),
        ('petugas', 'Petugas'),
    ], string='Tipe Anggota')