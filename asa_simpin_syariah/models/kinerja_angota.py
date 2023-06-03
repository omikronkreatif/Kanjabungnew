from odoo import models, fields, api

class kinerja_anggota(models.Model):
    _name = "kinerja.anggota"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Kinerja Anggota"
    _rec_name = 'anggota_id'

    anggota_id = fields.Many2one('simpin_syariah.member', string='Nama Anggota')
    id_anggota = fields.Char('ID Anggota')

    #kompetensi bidang organisasi
    org_dsr = fields.Integer('Organisasi Dasar')
    bdy_org = fields.Integer('Budaya Organisasi')
    jti_diri = fields.Integer('Jati Diri Koperasi')
    hak_kwjbn = fields.Integer('Hak & Kewajiban')

    din_kel = fields.Integer('Dinamika Kelompok')
    kmnksi = fields.Integer('Komunikasi')
    mod_sos = fields.Integer('Modal Sosial')
    motivasi = fields.Integer('motivasi')

    kepem = fields.Integer('Kepemimpinan')
    dsr_org = fields.Integer('Komunikasi')
    mngmn = fields.Integer('Management')
    anal_lapkeu = fields.Integer('Analisa Singkat Laporan Keuangan')
    komit = fields.Integer('Komitmen')
    sis_org = fields.Integer('Sistem Dalam Organisasi')
    nilai_kompetensi = fields.Integer('Nilai Kompetensi')
    total_kompetensi = fields.Integer('Total Kompetensi')

    #pengembangan sdma
    pelatihan = fields.Integer('Pelatihan')
    studi_banding = fields.Selection([
        ('a', 'Sesuai Kompetensi A'),
        ('ka', 'Sesuai Kompetensi KA'),
        ('ko', 'Sesuai Kompetensi KO'),
    ], string='Studi Banding')
    peny_rutin = fields.Integer('Penyuluhan Rutin')
    peny_segmen =fields.Selection([
        ('a', 'Sesuai Kompetensi A'),
        ('ka', 'Sesuai Kompetensi KA'),
        ('ko', 'Sesuai Kompetensi KO'),
    ], string='Penyuluhan Segmentasi')
    peng_sdm = fields.Integer('Pengembangan SDM Anggota Khusus')
    pend_teknis = fields.Integer('Pendamping Teknis')
    total_peng_sdma = fields.Integer('Total Pengembangan SDMA')

    #pendidikan
    kriteria = fields.Selection([
        ('sd', '>SD & Paket A'),
        ('pkt1', 'Paket B'),
        ('smp', 'SMP'),
        ('pkt2', 'Paket C'),
        ('sma', 'SMA/D1'),
        ('d3', 'D3'),
        ('s1', 'S1'),
        ('s2', 'S2'),
    ], string='Kriteria')
    nilai_kriteria = fields.Float('Nilai', compute='_hitung_nilai')

    @api.depends('kriteria')
    def _hitung_nilai(self):
        for record in self:
            if record.kriteria == 'sd':
                record.nilai_kriteria = 1
            elif record.kriteria == 'pkt1':
                record.nilai_kriteria = 1.5
            elif record.kriteria == 'smp':
                record.nilai_kriteria = 2
            elif record.kriteria == 'pkt2':
                record.nilai_kriteria = 2.5
            elif record.kriteria == 'sma':
                record.nilai_kriteria = 3
            elif record.kriteria == 'd3':
                record.nilai_kriteria = 3.5
            elif record.kriteria == 's1':
                record.nilai_kriteria = 4
            elif record.kriteria == 's2':
                record.nilai_kriteria = 5
            else:
                record.nilai_kriteria = 0

    #kehadiran
