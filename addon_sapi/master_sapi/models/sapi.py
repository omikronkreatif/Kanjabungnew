from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import date,datetime

class sapi(models.Model):
    _name = "sapi"
    _description = "Sapi"
    _inherits = {"res.partner": "partner_id"}
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'first_name'

    @api.depends('date_of_birth')
    def onchange_age(self):
        for rec in self:
            if rec.date_of_birth:
                d1 = rec.date_of_birth
                d2 = datetime.today().date()
                rd = relativedelta(d2, d1)
                rec.age = str(rd.years) + "y" +" "+ str(rd.months) + "m" +" "+ str(rd.days) + "d"
            else:
                rec.age = "No Date Of Birth!!"

    partner_id = fields.Many2one('res.partner', 'Partner',
                                 required=True, ondelete="cascade")
    patient_id = fields.Many2one('medical.patient')
    first_name = fields.Char('Name', size=128, translate=True)
    middle_name = fields.Char('Middle Name', size=128, translate=True)
    last_name = fields.Char('Last Name', size=128, translate=True)
    date_of_birth = fields.Date('Birth Date')
    blood_group = fields.Selection([
        ('A+', 'A+ve'),
        ('B+', 'B+ve'),
        ('O+', 'O+ve'),
        ('AB+', 'AB+ve'),
        ('A-', 'A-ve'),
        ('B-', 'B-ve'),
        ('O-', 'O-ve'),
        ('AB-', 'AB-ve')
    ], string='Blood Group')
    sex = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    ], 'Gender', required=True, default='m')
    id_number = fields.Char('ID Card Number', size=64)
    user_id = fields.Many2one('res.users', 'User', ondelete="cascade")
    category_id = fields.Many2one('op.category', 'Category')
    active = fields.Boolean(default=True)
    emergency_contact = fields.Many2one('res.partner', 'Emergency Contact')
    kandang_id = fields.Many2one('kandang.sapi.perah', 'Kandang')
    ibu_id = fields.Char('ID Sapi Ibu')
    ayah_id = fields.Char('ID Sapi Ayah')
    bobot = fields.Integer( string='Bobot Kg')
    panjang = fields.Integer('Panjang cm')
    kondisi_sapi = fields.Char('Kondisi Sapi')
    jenis_sapi = fields.Many2one('jenis.sapi.master', 'Jenis Sapi')
    eartag_id = fields.Char('ID Ear Tag')
    jenis_id = fields.Char(related='jenis_sapi.id_jenis_sapi', string="ID Jenis Sapi")
    keterangan = fields.Text(related="jenis_sapi.keterangan", string="Keterangan")
    tgl_kematian = fields.Datetime('Tanggal Kematian')
    alasan = fields.Char('Alasan')
    sehat = fields.Boolean('Sehat')
    sakit = fields.Boolean('Sakit')
    hamil = fields.Boolean('Hamil')
    tdk_hamil = fields.Boolean('Tidak Hamil')
    state = fields.Selection([
        ('kering', 'Kering'),
        ('laktasi', 'Laktasi'),
    ], string='State', readonly=True, default='kering', required=True)
    ibu_titipan = fields.Char('Ibu Titipan')
    jenis_kehamilan = fields.Selection([
        ('ib', 'IB'),
        ('alami', 'Alami'),
    ], string='Jenis Kehamilan', required=False)
    height = fields.Integer('Tinggi cm')
    lgkr_perut = fields.Integer('Lingkar Perut cm')
    peternak_id = fields.Many2one('peternak.sapi', 'Peternak')
    age = fields.Char(compute=onchange_age, string="Age", store=True)
    tipe = fields.Selection([
        ('1', 'Induk'),
        ('2', 'Dara'),
        ('3', 'Pedet Btn'),
    ], string='Tipe', required=True)
    posisi_eartag = fields.Selection([
        ('kanan', 'Kanan'),
        ('kiri', 'Kiri')
    ], string='Posisi Eartag')
    kembar = fields.Selection([
        ('y', 'Ya'),
        ('t', 'Tidak')
    ], string='Kembar')
    metoda = fields.Char('Metoda')
    tgl_identifikasi = fields.Date('Tanggal Identifikasi')
    kode_kelahiran = fields.Char('Kode Kelahiran')
    id_breed = fields.Char('ID Breed')
    nama_breed = fields.Char('Nama Breed')
    status_aktif = fields.Selection([
        ('a', 'Aktif'),
        ('ta', 'Tidak Aktif')
    ], string='Status Aktif')
    status_hidup = fields.Selection([
        ('h', 'Hidup'),
        ('m', 'Mati')
    ], string='Status Hidup')

    def func_kering(self):
        if self.state == 'kering':
            self.state = 'laktasi'

    def func_laktasi(self):
        if self.state == 'laktasi':
            self.state = 'kering'

    _sql_constraints = [(
        'unique_gr_no',
        'unique(gr_no)',
        'GR Number must be unique per student!'
    )]

    @api.model
    def create(self, vals):
        vals['partner_id'] = self.env['res.partner'].create({
            'name': vals.get('name'),
            'is_sapi': True,
            'company_type': 'person'
        }).id
        return super(sapi, self).create(vals)

    @api.onchange('first_name', 'middle_name', 'last_name')
    def _onchange_name(self):
        if not self.middle_name:
            self.name = str(self.first_name) + " " + str(
                self.last_name
            )
        else:
            self.name = str(self.first_name) + " " + str(
                self.middle_name) + " " + str(self.last_name)

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))

    def create_employee(self):
        for record in self:
            vals = {
                'name': record.name,
                'country_id': record.nationality.id,
                'sex': record.sex,
                'address_home_id': record.partner_id.id
            }
            emp_id = self.env['hr.employee'].create(vals)
            record.write({'emp_id': emp_id.id})
            record.partner_id.write({'partner_share': True, 'employee': True})
