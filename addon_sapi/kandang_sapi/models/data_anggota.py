from odoo import models, fields

class data_anggota(models.Model):
    _name = "data.anggota"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Data Anggota"
    _rec_name = 'peternak_id'

    peternak_id = fields.Many2one('peternak.sapi', string='Nama Anggota')
    kode_peternak = fields.Char(related='peternak_id.kode_peternak', string='ID Anggota')
    status_anggota = fields.Selection(related='peternak_id.state', string='Status Anggota')
    gmbr = fields.Binary(related='peternak_id.gmbr', string='Image')
    wilayah_id = fields.Many2one('master.wilayah', related='peternak_id.wilayah_id', string='Wilayah')
    thp = fields.Char('THP')
    prod_susu = fields.Char('Produksi Susu')
    jum_induk_laktasi = fields.Integer('Jumlah Induk Laktasi')
    jum_induk_kering = fields.Integer('Jumlah Induk Kering')
    jum_sapi_dara = fields.Integer('Jumlah Sapi Dara')
    fat = fields.Char('Fat')
    bj = fields.Char('BJ')
    grade = fields.Char('Grade')
    active = fields.Boolean(default=True)
    jenis_pelanggaran_ids = fields.One2many('pelanggaran.peternak', 'peternak_id', 'Jenis Pelanggaran')

    gdfp_count = fields.Integer(compute='compute_gdfp_count')

    def get_gdfp_count(self):
        action = self.env.ref('kandang_sapi.'
                              'act_gdfp_view').read()[0]
        action['domain'] = [('peternak_id', 'in', self.ids)]
        return action

    def compute_gdfp_count(self):
        for record in self:
            record.gdfp_count = self.env['entry.gdfp'].search_count(
                [('peternak_id', 'in', self.ids)])

    pelanggaran_gdfp_count = fields.Integer(compute='compute_pelanggaran_gdfp_count')

    def get_pelanggaran_gdfp_count(self):
        action = self.env.ref('peternak_sapi.'
                              'act_pelanggaran_view').read()[0]
        action['domain'] = [('peternak_id', 'in', self.ids)]
        return action

    def compute_pelanggaran_gdfp_count(self):
        for record in self:
            record.pelanggaran_gdfp_count = self.env['pelanggaran.peternak'].search_count(
                [('peternak_id', 'in', self.ids)])

#     gdfp_pelanggaran_line = fields.One2many('gdfp.pelanggaran.line', 'gdfp_pelanggaran_id', string='GDFP Pelanggaran Lines')
#
# class GDFPPelanggaranLine(models.Model):
#     _name = 'gdfp.pelanggaran.line'
#     _description = 'GDFP Pelanggaran Line'
#
#     peternak_name = fields.Many2one('peternak.sapi', string='Nama Anggota')
#     id_peternak = fields.Char(related='peternak_name.id_peternak', string='ID Anggota')
#     pelanggaran = fields.Many2one('jenis.pelanggaran', 'Pelanggaran')
#     keterangan = fields.Text('Keterangan')
#     gdfp_pelanggaran_id = fields.Many2one('data.anggota', string='GDFP Pelanggaran')