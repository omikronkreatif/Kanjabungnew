from odoo import models, fields, api

class liter_sapi(models.Model):
    _name = "liter.sapi"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Liter Sapi"
    _rec_name = 'tps_id'

    tgl_awal = fields.Date('Tanggal Awal')
    tgl_akhir = fields.Date('Tanggal Akhir')
    tps_id = fields.Many2one('tps.liter', string='TPS')
    peternak_id = fields.Many2one('peternak.sapi', 'Peternak')
    kode_peternak = fields.Char(related='peternak_id.kode_peternak', string='ID Peternak')
    sapi_id = fields.Many2many('sapi', string='Nama Sapi', domain=[('state', '=', 'laktasi')], related='peternak_id.sapi_ids', readonly=False)
    sapi_ids = fields.One2many('sapi', 'peternak_id' ,string='Nama Sapi', domain=[('state', '=', 'laktasi')], related='peternak_id.list_sapi_ids', readonly=False)
    # sapi_ids = fields.One2many('sapi', 'peternak_id', string='Nama Sapi', compute='_compute_sapi_ids', readonly=False,
    #                            store=True, domain=[('state', '=', 'kering')])
    kelompok_id = fields.Many2one(related='peternak_id.kelompok_id', string='Kelompok Peternak')
    contact_address = fields.Char('Alamat', related='peternak_id.contact_address')
    setor = fields.Char('Setor Liter')
    bj = fields.Integer('BJ')
    grade = fields.Char('Grade')
    purchase_count = fields.Integer(compute='compute_purchase_count')
    setoran = fields.Float('Total Setoran Susu', compute='_compute_setoran')
    harga_kual = fields.Float('Harga Kualitas', compute='hitung_harga_kualitas')
    insen_prod = fields.Float('Insentif Produksi', compute='jumlah_insen_prod')
    insen_pmk = fields.Float('Insentif PMK', compute='jumlah_insen_pmk')
    insen_daya_saing = fields.Float('Insentif Daya Saing', default=200)
    harga_satuan = fields.Float('Harga Satuan', compute='hitung_jumlah_harga_satuan')
    #lab
    suhu = fields.Float('Suhu')
    fat = fields.Float('FAT')
    snf = fields.Float('SNF')
    ts = fields.Float('TS')
    bj = fields.Float('BJ')
    pro = fields.Float('Pro')
    lac = fields.Float('Lac')
    salts = fields.Float('Salts')
    add_water = fields.Float('Add Water')
    freez_point = fields.Float('Freezing Point')
    tpc_kan = fields.Float('TPC KAN')
    mbrt = fields.Char('MBRT/Rezazurin')
    grade = fields.Float('Grade', compute='jumlah_grade')
    pres_grade = fields.Float('%Grade', compute='hitung_grade')
    tpc_ips = fields.Float('TPC IPS')
    # jenis_pelanggaran_liter_ids = fields.One2many('pelanggaran.peternak', 'peternak_name', 'Jenis Pelanggaran')
    jenis_pelanggaran = fields.Many2one('pelanggaran.peternak', 'Pelanggaran')
    keterangan = fields.Text(related='jenis_pelanggaran.keterangan', string='Keterangan')
    product_id = fields.Many2one('product.template', 'Product')

    total_harga_susu = fields.Float('Total Harga Susu', compute='hitung_total_harga_susu')
    jumlah_hari = fields.Integer('Jumlah Hari', default=11)
    avg_setor = fields.Float('Rata-Rata Setor', compute='hitung_avg_setor')

    # @api.depends('setoran_line_ids')
    # def _compute_jumlah_hari(self):
    #     for record in self:
    #         record.jumlah_hari = len(record.setoran_line_ids)

    @api.depends('insen_pmk', 'avg_setor')
    def jumlah_insen_pmk(self):
        for record in self:
            if record.avg_setor >= 1 and record.setoran <= 20:
                record.insen_pmk = 600
            elif record.avg_setor > 20:
                record.insen_pmk = 500
            else:
                record.insen_pmk = 0

    @api.depends('setoran', 'jumlah_hari')
    def hitung_avg_setor(self):
        for record in self:
            if record.setoran != 0:
                record.avg_setor = record.setoran / record.jumlah_hari
            else:
                record.avg_setor = 0

    @api.depends('avg_setor')
    def jumlah_insen_prod(self):
        for record in self:
            if record.avg_setor >= 1 and record.avg_setor <= 20:
                record.insen_prod = 1300
            elif record.avg_setor >= 21 and record.avg_setor <= 30:
                record.insen_prod = 1340
            elif record.avg_setor >= 31 and record.avg_setor <= 50:
                record.insen_prod = 1405
            elif record.avg_setor >= 51 and record.avg_setor <= 100:
                record.insen_prod = 1470
            elif record.avg_setor > 101:
                record.insen_prod = 1560
            else:
                record.insen_prod = 0

    @api.depends('setoran_line_ids.berat_setoran')
    def _compute_setoran(self):
        for record in self:
            total_setoran = sum(setoran.berat_setoran for setoran in record.setoran_line_ids)
            record.setoran = total_setoran

    @api.depends('peternak_id')
    def _compute_sapi_ids(self):
        for record in self:
            record.sapi_ids = self.env['sapi'].search(
                [('peternak_id', '=', record.peternak_id.id), ('state', '=', 'kering')])

    @api.constrains('tgl_awal', 'tgl_akhir')
    def _check_dates(self):
        for period in self:
            if period.tgl_awal > period.tgl_akhir:
                raise models.ValidationError("Tanggal Awal Harus Sebelum Tanggal Akhir!")

    @api.depends('setoran', 'harga_satuan')
    def hitung_total_harga_susu(self):
        for record in self:
            if record.setoran != 0:
                record.total_harga_susu = record.setoran * record.harga_satuan
            else:
                record.total_harga_susu = 0

    @api.depends('tpc_kan', 'tpc_ips')
    def hitung_grade(self):
        for record in self:
            if record.tpc_ips != 0:
                record.pres_grade = record.tpc_kan / record.tpc_ips
            else:
                record.pres_grade = 0

    @api.depends('grade', 'tpc_kan')
    def jumlah_grade(self):
        for record in self:
            if record.tpc_kan <= 1000000:
                record.grade = 1
            elif record.tpc_kan <= 2000000:
                record.grade = 2
            elif record.tpc_kan <= 3000000:
                record.grade = 3
            elif record.tpc_kan <= 4000000:
                record.grade = 4
            else:
                record.grade = 0

    @api.depends('grade', 'ts')
    def hitung_harga_kualitas(self):
        for record in self:
            if record.grade == 1:
                grade_value = 4343
            elif record.grade == 1.5:
                grade_value = 4293
            elif record.grade == 2:
                grade_value = 4243
            elif record.grade == 2.5:
                grade_value = 4193
            elif record.grade == 3:
                grade_value = 4143
            else:
                grade_value = 0

            if record.ts >= 12:
                record.harga_kual = grade_value / 12 * record.ts
            else:
                record.harga_kual = 0

    @api.depends('harga_kual', 'insen_prod', 'insen_pmk', 'insen_daya_saing')
    def hitung_jumlah_harga_satuan(self):
        for record in self:
            record.harga_satuan = record.harga_kual + record.insen_prod + record.insen_pmk + record.insen_daya_saing

    def get_purchase(self):
        action = self.env.ref('purchase.'
                              'purchase_form_action').read()[0]
        action['domain'] = [('sapi_id', 'in', self.ids)]
        return action

    def compute_purchase_count(self):
        for record in self:
            record.purchase_count = self.env['purchase.order'].search_count(
                [('sapi_id', 'in', self.ids)])

    setoran_line_ids = fields.One2many('setoran.line', 'liter_sapi_id', string='Setoran Line Ids')

class purchase(models.Model):
    _inherit = "purchase.order"

    sapi_id = fields.Many2one('sapi', 'Sapi')
    bj = fields.Integer('BJ')
    grade = fields.Char('Grade')

class SetoranLine(models.Model):
    _name = 'setoran.line'
    _description = 'Setoran Line'

    liter_sapi_id = fields.Many2one('liter.sapi', 'Liter Sapi Id')
    berat_setoran = fields.Float('Setoran Susu', default=0.0)
    uom_id = fields.Many2one('uom.uom', 'Uom')
    # harga_total = fields.Float('Total Harga', compute='hitung_jumlah_harga')
    # total_harga_susu = fields.Float('Total Harga Susu', compute='hitung_total_harga_susu')
    # harga_kual = fields.Float('Harga Kualitas', compute='hitung_harga_kualitas')
    # grade = fields.Float('Grade', compute='jumlah_grade')
    # ts = fields.Float('TS')
    # tpc_kan = fields.Float('TPC KAN')
    # insen_prod = fields.Float('Ins Produksi')
    # insen_ef = fields.Float('Ins Efesiensi')
    tgl_setor = fields.Datetime('Tanggal Setor')
    tipe_setor = fields.Selection([
        ('0', ''),
        ('1', 'Pagi'),
        ('2', 'Sore')
    ], 'Tipe Setor', required=True, default=False)
    bj = fields.Float('BJ')
    # total_line_harga_susu = fields.Float('Subtotal', compute='_compute_total_line_harga_susu')
    #
    # @api.depends('setoran.line')
    # def _compute_total_line_harga_susu(self):
    #     for record in self:
    #         record.total_line_harga_susu = sum(line.total_harga_susu for line in record)

    @api.onchange('tgl_setor')
    def _onchange_tgl_setor(self):
        if self.tgl_setor:
            hour = fields.Datetime.from_string(self.tgl_setor).hour
            if 6 <= hour < 12:
                self.tipe_setor = '2'  # Pagi
            elif 12 <= hour < 17:
                self.tipe_setor = '1'  # Sore

    # @api.onchange('ts')
    # def _onchange_ts(self):
    #     if self.ts:
    #         # Lakukan tindakan yang sesuai untuk mengisi field "ts" di model "setoran.line"
    #         # Misalnya, lakukan sesuatu dengan nilai self.ts
    #         # self.ts = ...
    #         pass

    # @api.depends('harga_kual', 'insen_prod', 'insen_ef')
    # def hitung_jumlah_harga(self):
    #     for record in self:
    #         record.harga_total = record.harga_kual + record.insen_prod + record.insen_ef

    # @api.depends('setoran', 'harga_total')
    # def hitung_total_harga_susu(self):
    #     for record in self:
    #         if record.setoran != 0:
    #             record.total_harga_susu = record.setoran * record.harga_total
    #         else:
    #             record.total_harga_susu = 0

    # @api.depends('grade', 'ts')
    # def hitung_harga_kualitas(self):
    #     for record in self:
    #         if record.grade == 1:
    #             grade_value = 4343
    #         elif record.grade == 1.5:
    #             grade_value = 4293
    #         elif record.grade == 2:
    #             grade_value = 4243
    #         elif record.grade == 2.5:
    #             grade_value = 4193
    #         elif record.grade == 3:
    #             grade_value = 4143
    #         else:
    #             grade_value = 0
    #
    #         if record.ts >= 12:
    #             record.harga_kual = grade_value / 12 * record.ts
    #         else:
    #             record.harga_kual = 0

    # @api.depends('grade', 'tpc_kan')
    # def jumlah_grade(self):
    #     for record in self:
    #         if record.tpc_kan <= 1000000:
    #             record.grade = 1
    #         elif record.tpc_kan <= 2000000:
    #             record.grade = 2
    #         elif record.tpc_kan <= 3000000:
    #             record.grade = 3
    #         elif record.tpc_kan <= 4000000:
    #             record.grade = 4
    #         else:
    #             record.grade = 0