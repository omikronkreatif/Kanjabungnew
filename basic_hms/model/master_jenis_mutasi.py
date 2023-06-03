from odoo import models, fields, api, _

class master_jenis_mutasi(models.Model):
    _name = 'master.jenis.mutasi'
    _rec_name = 'jenis_mutasi'

    jenis_mutasi = fields.Char('Nama Ruangan')
    id_jenis_mutasi = fields.Char('ID Jenis Mutasi')
