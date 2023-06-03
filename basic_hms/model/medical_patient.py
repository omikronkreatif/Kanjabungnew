# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import date,datetime
from dateutil.relativedelta import relativedelta 

class medical_patient(models.Model):
    _name = 'medical.patient'
    _rec_name = 'patient_id'

    # @api.onchange('patient_id')
    # def _onchange_patient(self):
    #     '''
    #     The purpose of the method is to define a domain for the available
    #     purchase orders.
    #     '''
    #     address_id = self.patient_id
    #     self.partner_address_id = address_id

    def print_report(self):
        return self.env.ref('basic_hms.report_print_patient_card').report_action(self)

    # @api.depends('date_of_birth')
    # def onchange_age(self):
    #     for rec in self:
    #         if rec.date_of_birth:
    #             d1 = rec.date_of_birth
    #             d2 = datetime.today().date()
    #             rd = relativedelta(d2, d1)
    #             rec.age = str(rd.years) + "y" +" "+ str(rd.months) + "m" +" "+ str(rd.days) + "d"
    #         else:
    #             rec.age = "No Date Of Birth!!"

    patient_id = fields.Many2one('res.partner', string="Patient", required=False, domain="[('is_sapi', '=', True)]")
    sapi_id = fields.Many2one('sapi', string='Sapi')
    name = fields.Char(string='ID', readonly=True)
    last_name = fields.Char('Last Name')
    date_of_birth = fields.Date(related="sapi_id.date_of_birth", string="Date of Birth")
    sex = fields.Selection([('m', 'Male'),('f', 'Female')], string ="Sex")
    age = fields.Char(related="sapi_id.age", string="Patient Age",store=True)
    critical_info = fields.Text(string="Patient Critical Information")
    image_1920 = fields.Binary(string="Picture")
    blood_type = fields.Selection([('A', 'A'),('B', 'B'),('AB', 'AB'),('O', 'O')], string ="Blood Type")
    rh = fields.Selection([('-+', '+'),('--', '-')], string ="Rh")
    marital_status = fields.Selection([('s','Single'),('m','Married'),('w','Widowed'),('d','Divorced'),('x','Seperated')],string='Marital Status')
    deceased = fields.Boolean(string='Deceased')
    date_of_death = fields.Datetime(string="Date of Death")
    cause_of_death = fields.Char(string='Cause of Death')
    receivable = fields.Float(string="Receivable", readonly=True)
    current_insurance_id = fields.Many2one('medical.insurance',string="Insurance")
    partner_address_id = fields.Text(string="Address")
    phone = fields.Char(string="Phone")
    primary_care_physician_id = fields.Many2one('medical.physician', string="Primary Care Doctor")
    patient_status = fields.Char(string="Hospitalization Status",readonly=True)
    patient_disease_ids = fields.One2many('medical.patient.disease','patient_id')
    patient_psc_ids = fields.One2many('medical.patient.psc','patient_id')
    excercise = fields.Boolean(string='Excercise')
    excercise_minutes_day = fields.Integer(string="Minutes/Day")
    sleep_hours = fields.Integer(string="Hours of sleep")
    sleep_during_daytime = fields.Boolean(string="Sleep at daytime")
    number_of_meals = fields.Integer(string="Meals per day")
    coffee = fields.Boolean('Coffee')
    coffee_cups = fields.Integer(string='Cups Per Day')
    eats_alone = fields.Boolean(string="Eats alone")
    soft_drinks = fields.Boolean(string="Soft drinks(sugar)")
    salt = fields.Boolean(string="Salt")
    diet = fields.Boolean(string=" Currently on a diet ")
    diet_info = fields.Integer(string=' Diet info ')
    general_info = fields.Text(string="Info")
    lifestyle_info = fields.Text('Lifestyle Information')
    smoking = fields.Boolean(string="Smokes")
    smoking_number = fields.Integer(string="Cigarretes a day")
    ex_smoker = fields.Boolean(string="Ex-smoker")
    second_hand_smoker = fields.Boolean(string="Passive smoker")
    age_start_smoking = fields.Integer(string="Age started to smoke")
    age_quit_smoking = fields.Integer(string="Age of quitting")
    drug_usage = fields.Boolean(string='Drug Habits')
    drug_iv = fields.Boolean(string='IV drug user')
    ex_drug_addict = fields.Boolean(string='Ex drug addict')
    age_start_drugs = fields.Integer(string='Age started drugs')
    age_quit_drugs = fields.Integer(string="Age quit drugs")
    alcohol = fields.Boolean(string="Drinks Alcohol")
    ex_alcohol = fields.Boolean(string="Ex alcoholic")
    age_start_drinking = fields.Integer(string="Age started to drink")
    age_quit_drinking = fields.Integer(string="Age quit drinking")
    alcohol_beer_number = fields.Integer(string="Beer / day")
    alcohol_wine_number = fields.Integer(string="Wine / day")
    alcohol_liquor_number = fields.Integer(string="Liquor / day")
    cage_ids = fields.One2many('medical.patient.cage','patient_id')
    sex_oral = fields.Selection([('0','None'),
                                 ('1','Active'),
                                 ('2','Passive'),
                                 ('3','Both')],string='Oral Sex')
    sex_anal = fields.Selection([('0','None'),
                                 ('1','Active'),
                                 ('2','Passive'),
                                 ('3','Both')],string='Anal Sex')
    prostitute = fields.Boolean(string='Prostitute')
    sex_with_prostitutes = fields.Boolean(string=' Sex with prostitutes ')
    sexual_preferences = fields.Selection([
            ('h', 'Heterosexual'),
            ('g', 'Homosexual'),
            ('b', 'Bisexual'),
            ('t', 'Transexual'),
        ], 'Sexual Orientation', sort=False)
    sexual_practices = fields.Selection([
            ('s', 'Safe / Protected sex'),
            ('r', 'Risky / Unprotected sex'),
        ], 'Sexual Practices', sort=False)
    sexual_partners = fields.Selection([
            ('m', 'Monogamous'),
            ('t', 'Polygamous'),
        ], 'Sexual Partners', sort=False)
    sexual_partners_number = fields.Integer('Number of sexual partners')
    first_sexual_encounter = fields.Integer('Age first sexual encounter')
    anticonceptive = fields.Selection([
            ('0', 'None'),
            ('1', 'Pill / Minipill'),
            ('2', 'Male condom'),
            ('3', 'Vasectomy'),
            ('4', 'Female sterilisation'),
            ('5', 'Intra-uterine device'),
            ('6', 'Withdrawal method'),
            ('7', 'Fertility cycle awareness'),
            ('8', 'Contraceptive injection'),
            ('9', 'Skin Patch'),
            ('10', 'Female condom'),
        ], 'Anticonceptive Method', sort=False)
    sexuality_info = fields.Text('Extra Information')
    motorcycle_rider = fields.Boolean('Motorcycle Rider', help="The patient rides motorcycles")
    helmet = fields.Boolean('Uses helmet', help="The patient uses the proper motorcycle helmet")
    traffic_laws = fields.Boolean('Obeys Traffic Laws', help="Check if the patient is a safe driver")
    car_revision = fields.Boolean('Car Revision', help="Maintain the vehicle. Do periodical checks - tires,breaks ...")
    car_seat_belt = fields.Boolean('Seat belt', help="Safety measures when driving : safety belt")
    car_child_safety = fields.Boolean('Car Child Safety', help="Safety measures when driving : child seats, proper seat belting, not seating on the front seat, ....")
    home_safety = fields.Boolean('Home safety', help="Keep safety measures for kids in the kitchen, correct storage of chemicals, ...")
    fertile = fields.Boolean('Fertile')
    menarche = fields.Integer('Menarche age')
    menopausal = fields.Boolean('Menopausal')
    menopause = fields.Integer('Menopause age')
    menstrual_history_ids = fields.One2many('medical.patient.menstrual.history','patient_id')
    breast_self_examination = fields.Boolean('Breast self-examination')
    mammography = fields.Boolean('Mammography')
    pap_test = fields.Boolean('PAP test')
    last_pap_test = fields.Date('Last PAP test')
    colposcopy = fields.Boolean('Colposcopy')
    mammography_history_ids = fields.One2many('medical.patient.mammography.history','patient_id')
    pap_history_ids = fields.One2many('medical.patient.pap.history','patient_id')
    colposcopy_history_ids = fields.One2many('medical.patient.colposcopy.history','patient_id')
    pregnancies = fields.Integer('Pregnancies')
    premature = fields.Integer('Premature')
    stillbirths = fields.Integer('Stillbirths')
    abortions = fields.Integer('Abortions')
    pregnancy_history_ids = fields.One2many('medical.patient.pregnency','patient_id')
    family_history_ids = fields.Many2many('medical.family.disease',string="Family Disease Lines")
    perinatal_ids = fields.Many2many('medical.preinatal')
    ex_alcoholic = fields.Boolean('Ex alcoholic')
    currently_pregnant = fields.Boolean('Currently Pregnant')
    born_alive = fields.Integer('Born Alive')
    gpa = fields.Char('GPA')
    works_at_home = fields.Boolean('Works At Home')
    colposcopy_last = fields.Date('Last colposcopy')
    mammography_last = fields.Date('Last mammography')
    ses = fields.Selection([
            ('None', ''),
            ('0', 'Lower'),
            ('1', 'Lower-middle'),
            ('2', 'Middle'),
            ('3', 'Middle-upper'),
            ('4', 'Higher'),
        ], 'Socioeconomics', help="SES - Socioeconomic Status", sort=False)
    education = fields.Selection([('o','None'),('1','Incomplete Primary School'),
                                  ('2','Primary School'),
                                  ('3','Incomplete Secondary School'),
                                  ('4','Secondary School'),
                                  ('5','University')],string='Education Level')
    housing = fields.Selection([
            ('None', ''),
            ('0', 'Shanty, deficient sanitary conditions'),
            ('1', 'Small, crowded but with good sanitary conditions'),
            ('2', 'Comfortable and good sanitary conditions'),
            ('3', 'Roomy and excellent sanitary conditions'),
            ('4', 'Luxury and excellent sanitary conditions'),
        ], 'Housing conditions', help="Housing and sanitary living conditions", sort=False)
    works = fields.Boolean('Works')
    hours_outside = fields.Integer('Hours outside home', help="Number of hours a day the patient spend outside the house")
    hostile_area = fields.Boolean('Hostile Area')
    notes = fields.Text(string="Extra info")
    sewers = fields.Boolean('Sanitary Sewers')
    water = fields.Boolean('Running Water')
    trash = fields.Boolean('Trash recollection')
    electricity = fields.Boolean('Electrical supply')
    gas = fields.Boolean('Gas supply')
    telephone = fields.Boolean('Telephone')
    television = fields.Boolean('Television')
    internet = fields.Boolean('Internet')
    single_parent= fields.Boolean('Single parent family')
    domestic_violence = fields.Boolean('Domestic violence')
    working_children = fields.Boolean('Working children')
    teenage_pregnancy = fields.Boolean('Teenage pregnancy')
    sexual_abuse = fields.Boolean('Sexual abuse')
    drug_addiction = fields.Boolean('Drug addiction')
    school_withdrawal = fields.Boolean('School withdrawal')
    prison_past = fields.Boolean('Has been in prison')
    prison_current = fields.Boolean('Is currently in prison')
    relative_in_prison = fields.Boolean('Relative in prison', help="Check if someone from the nuclear family - parents sibblings  is or has been in prison")
    fam_apgar_help = fields.Selection([
            ('None', ''),
            ('0', 'None'),
            ('1', 'Moderately'),
            ('2', 'Very much'),
        ], 'Help from family',
            help="Is the patient satisfied with the level of help coming from the family when there is a problem ?", sort=False)
    fam_apgar_discussion = fields.Selection([
            ('None', ''),
            ('0', 'None'),
            ('1', 'Moderately'),
            ('2', 'Very much'),
        ], 'Problems discussion',
            help="Is the patient satisfied with the level talking over the problems as family ?", sort=False)
    fam_apgar_decisions = fields.Selection([
            ('None', ''),
            ('0', 'None'),
            ('1', 'Moderately'),
            ('2', 'Very much'),
        ], 'Decision making',
            help="Is the patient satisfied with the level of making important decisions as a group ?", sort=False)
    fam_apgar_timesharing = fields.Selection([
            ('None', ''),
            ('0', 'None'),
            ('1', 'Moderately'),
            ('2', 'Very much'),
        ], 'Time sharing',
            help="Is the patient satisfied with the level of time that they spend together ?", sort=False)
    fam_apgar_affection = fields.Selection([
            ('None', ''),
            ('0', 'None'),
            ('1', 'Moderately'),
            ('2', 'Very much'),
        ], 'Family affection',
            help="Is the patient satisfied with the level of affection coming from the family ?", sort=False)
    fam_apgar_score = fields.Integer('Score', help="Total Family APGAR 7 - 10 : Functional Family 4 - 6  : Some level of disfunction \n"
                                          "0 - 3  : Severe disfunctional family \n")
    lab_test_ids = fields.One2many('medical.patient.lab.test','patient_id')
    fertile = fields.Boolean('Fertile')
    menarche_age  = fields.Integer('Menarche age')
    menopausal = fields.Boolean('Menopausal')
    pap_test_last = fields.Date('Last PAP Test')
    colposcopy = fields.Boolean('Colpscopy')
    gravida = fields.Integer('Pregnancies')
    medical_vaccination_ids = fields.One2many('medical.vaccination','medical_patient_vaccines_id')
    medical_appointments_ids = fields.One2many('medical.appointment','patient_id',string='Appointments')
    lastname = fields.Char('Last Name')
    report_date = fields.Date('Date',default = datetime.today().date())
    medication_ids = fields.One2many('medical.patient.medication1','medical_patient_medication_id')
    medication_line_ids = fields.One2many('medical.prescription.line','medical_patient')
    deaths_2nd_week = fields.Integer('Deceased after 2nd week')
    deaths_1st_week = fields.Integer('Deceased after 1st week')
    full_term = fields.Integer('Full Term')
    ses_notes = fields.Text('Notes')
    weight = fields.Integer(related="sapi_id.bobot", string='Bobot kg')
    height = fields.Integer(related="sapi_id.height", string='Tinggi cm')
    panjang = fields.Integer(related="sapi_id.panjang", string='Panjnag cm')
    lgkr_perut = fields.Integer (related="sapi_id.lgkr_perut", string='Lingkar Perut cm')
    category = fields.Selection([('c1','Class 1'),('c2','Class 2'),('c3','Class 3')], string="Category")
    peternak_id = fields.Many2one('peternak.sapi', 'Peternak')
    code_sapi = fields.Char( string='ID Sapi')
    jenis_sapi = fields.Many2one('jenis.sapi.master', related='sapi_id.jenis_sapi', string='Jenis Sapi')
    #kehamilan
    status_rep = fields.Selection([
        ('1', 'Tidak Ada'),
        ('2', 'Pernah di IB/KAWIN'),
        ('3', 'Kosong'),
        ('4', 'Bunting'),
        ('5', 'Melahirkan'),
        ('6', 'Donor'),
        ], 'Status Reproduksi')
    tanda_kebun = fields.Selection([
        ('1', 'Fluktuas'),
        ('2', 'Slip Membran'),
        ('3', 'Kotiledon'),
        ('4', 'Undulasi'),
        ('5', 'Kornua Kiri'),
        ('6', 'Kornua Kanan'),
        ('7', 'Bifurcatio'),
        ('8', 'Amniotic Vesicle'),
        ], 'Tanda Kebuntingan')
    umur_khmln = fields.Integer('Umur Kehamilan')
    bcs = fields.Integer('Body Condition Score')

    #kelahiran
    jmlh_lahir = fields.Integer('jumlah Lahir')
    jmlh_mati = fields.Integer('Jumlah Mati')
    jns_kelam = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female'),
    ], 'Jenis Kelamin')
    stts_reprod = fields.Selection([
        ('1', 'Sudah IB'),
        ('2', 'Kosong'),
        ('3', 'Bunting'),
        ('4', 'Ragu Bunting'),
        ('5', 'Lain-Lain')
    ], string='Status Reproduksi', required=False)
    metod_perolehan = fields.Selection([
        ('1', 'Lahir'),
        ('2', 'Beli'),
        ('3', 'Kredit'),
        ('4', 'Pindah'),
        ('5', 'Bagi Hasil')
    ], string='Metode Perolehan', required=False)
    stats_laktasi = fields.Selection([
        ('kering', 'Kering'),
        ('laktasi', 'Laktasi'),
        ('tdk', 'Tidak Ada'),
    ], string='Status Laktasi', required=True)
    tipe = fields.Selection([
        ('1', 'Induk'),
        ('2', 'Dara'),
        ('3', 'Pedet Btn'),
    ], string='Tipe', required=True)
    laktasi_ke = fields.Integer('Laktasi Ke')
    id_induk = fields.Char('ID Induk')
    id_ayah = fields.Char('ID Ayah')

    jml_puting = fields.Integer('Jumlah Puting')
    kon_kaki = fields.Selection([
        ('sim', 'Simetris'),
        ('tdk', 'Tidak Simetris'),
    ], string='Kondisi Kaki')
    punggung = fields.Selection([
        ('lor', 'Lordosis'),
        ('kif', 'Kifosis'),
        ('lur', 'Lurus'),
    ], string='Punggung')

    @api.onchange('tipe')
    def onchange_tipe(self):
        if self.tipe and self.sapi_id:
            # Ubah nilai tipe di objek sapi_id jika field sapi_tipe diisi
            self.sapi_id.write({'tipe': self.tipe})

    @api.onchange('sapi_id.tipe')
    def onchange_tipe_sapi(self):
        if self.sapi_id.tipe == '1':
            # Lakukan sesuatu jika tipe sapi = Induk
            pass
        elif self.sapi_id.tipe == '2':
            # Lakukan sesuatu jika tipe sapi = Dara
            pass
        elif self.sapi_id.tipe == '3':
            # Lakukan sesuatu jika tipe sapi = Pedet Btn
            pass

    @api.onchange('sapi_id')
    def onchange_sapi_id_sex(self):
        if self.sapi_id:
            if self.sapi_id.sex:
                self.sex = self.sapi_id.sex
        else:
            self.sex = ''

    @api.onchange('sapi_id')
    def onchange_peternak_id(self):
        if self.sapi_id:
            if self.sapi_id.peternak_id:
                self.peternak_id = self.sapi_id.peternak_id
        else:
            self.peternak_id = ''

    @api.onchange('patient_id')
    def _onchange_patient_id_image(self):
        if self.patient_id:
            self.image_1920 = self.patient_id.image_1920

    @api.model
    def create(self,val):
        appointment = self._context.get('appointment_id')
        res_partner_obj = self.env['res.partner']
        if appointment:
            val_1 = {'name': self.env['res.partner'].browse(val['patient_id']).name}
            patient= res_partner_obj.create(val_1)
            val.update({'patient_id': patient.id})
        if val.get('date_of_birth'):
            dt = val.get('date_of_birth')
            d1 = datetime.strptime(str(dt), "%Y-%m-%d").date()
            d2 = datetime.today().date()
            rd = relativedelta(d2, d1)
            age = str(rd.years) + "y" +" "+ str(rd.months) + "m" +" "+ str(rd.days) + "d"
            val.update({'age':age} )

        patient_id  = self.env['ir.sequence'].next_by_code('medical.patient')
        if patient_id:
            val.update({
                        'name':patient_id,
                       })
        result = super(medical_patient, self).create(val)
        return result

    appointment_count = fields.Integer(compute='compute_appointment_count')

    def get_appointment(self):
        action = self.env.ref('basic_hms.'
                              'action_medical_appointment').read()[0]
        action['domain'] = [('patient_id', 'in', self.ids)]
        return action

    def compute_appointment_count(self):
        for record in self:
            record.appointment_count = self.env['medical.appointment'].search_count(
                [('patient_id', 'in', self.ids)])

    inpatient_count = fields.Integer(compute='compute_inpatient_count')

    def get_inpatient(self):
        action = self.env.ref('basic_hms.'
                              'action_medical_inpatient_registration').read()[0]
        action['domain'] = [('patient_id', 'in', self.ids)]
        return action

    def compute_inpatient_count(self):
        for record in self:
            record.inpatient_count = self.env['medical.inpatient.registration'].search_count(
                [('patient_id', 'in', self.ids)])

    # lab_count = fields.Integer(compute='compute_lab_count')
    #
    # def get_lab(self):
    #     action = self.env.ref('basic_hms.'
    #                           'action_medical_lab_form').read()[0]
    #     action['domain'] = [('patient_id', 'in', self.ids)]
    #     return action
    #
    # def compute_lab_count(self):
    #     for record in self:
    #         record.lab_count = self.env['medical.lab'].search_count(
    #             [('patient_id', 'in', self.ids)])

    medicament_count = fields.Integer(compute='compute_medicament_count')

    def get_medicament(self):
        action = self.env.ref('basic_hms.'
                              'action_medical_prescription_order').read()[0]
        action['domain'] = [('patient_id', 'in', self.ids)]
        return action

    def compute_medicament_count(self):
        for record in self:
            record.medicament_count = self.env['medical.prescription.order'].search_count(
                [('patient_id', 'in', self.ids)])
# vim=expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

class form_abortus(models.Model):
    _name = 'form.abortus'
    _inherit = 'image.mixin'
    _rec_name = 'sapi_id'

    peternak_id = fields.Many2one('peternak.sapi', 'Anggota/Peternak')
    id_pemilik = fields.Char('ID Pemilik', related='peternak_id.kode_peternak')
    kelompok_id = fields.Many2one('peternak.group', related='peternak_id.kelompok_id')
    petugas_id = fields.Many2one('medical.physician', 'Petugas')
    sapi_id = fields.Many2one('sapi', 'Nama Sapi', domain="[('peternak_id', '=', peternak_id)]")
    eartag_id = fields.Char('ID Eartag Sapi')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    penyebab_abortus = fields.Text('Penyebab Abortus')
    masa_kebun = fields.Integer('Masa kebuntingan')
    komentar = fields.Text('Komentar')

class form_pkb(models.Model):
    _name = 'form.pkb'
    _inherit = 'image.mixin'
    _rec_name = 'sapi_id'

    peternak_id = fields.Many2one('peternak.sapi', 'Anggota/Peternak')
    id_pemilik = fields.Char('ID Pemilik', related='peternak_id.kode_peternak')
    kelompok_id = fields.Many2one('peternak.group', related='peternak_id.kelompok_id')
    petugas_id = fields.Many2one('medical.physician', 'Petugas')
    sapi_id = fields.Many2one('sapi', 'Nama Sapi', domain="[('peternak_id', '=', peternak_id)]")
    eartag_id = fields.Char('ID Eartag Sapi')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    bcs = fields.Char('BCS')
    tanda_bunting = fields.Selection([
        ('bunting', 'Bunting'),
        ('kosong', 'Kosong'),
        ('ragu_bunting', 'Ragu Bunting')
    ], string='Tanda Kebuntingan')
    posisi = fields.Char('Posisi')
    tgl_ib_akhir = fields.Date('Tanggal IB Terakhir')
    umur_bunting = fields.Integer('Umur Kebuntingan')

class form_bsk(models.Model):
    _name = 'form.bsk'
    _inherit = 'image.mixin'
    _rec_name = 'sapi_id'

    peternak_id = fields.Many2one('peternak.sapi', 'Anggota/Peternak')
    id_pemilik = fields.Char('ID Pemilik', related='peternak_id.kode_peternak')
    kelompok_id = fields.Many2one('peternak.group', related='peternak_id.kelompok_id')
    petugas_id = fields.Many2one('medical.physician', 'Petugas')
    sapi_id = fields.Many2one('sapi', 'Nama Sapi', domain="[('peternak_id', '=', peternak_id)]")
    eartag_id = fields.Char('ID Eartag Sapi')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    cat_petugas = fields.Text('Catatan Petugas')

class form_dara_metestrus(models.Model):
    _name = 'form.dm'
    _rec_name = 'sapi_id'

    peternak_id = fields.Many2one('peternak.sapi', 'Anggota/Peternak')
    id_pemilik = fields.Char('ID Pemilik', related='peternak_id.kode_peternak')
    kelompok_id = fields.Many2one('peternak.group', related='peternak_id.kelompok_id')
    petugas_id = fields.Many2one('medical.physician', 'Petugas')
    sapi_id = fields.Many2one('sapi', 'Nama Sapi', domain="[('peternak_id', '=', peternak_id)]")
    eartag_id = fields.Char('ID Eartag Sapi')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    komentar = fields.Text('Komentar')

class form_mutasi(models.Model):
    _name = 'form.mutasi'
    _rec_name = 'sapi_id'

    peternak_id = fields.Many2one('peternak.sapi', 'Anggota/Peternak')
    id_pemilik = fields.Char('ID Pemilik', related='peternak_id.kode_peternak')
    kelompok_id = fields.Many2one('peternak.group', related='peternak_id.kelompok_id')
    petugas_id = fields.Many2one('medical.physician', 'Petugas')
    sapi_id = fields.Many2one('sapi', 'Nama Sapi', domain="[('peternak_id', '=', peternak_id)]")
    eartag_id = fields.Char('ID Eartag Sapi')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    jns_mutasi = fields.Many2one('master.jenis.mutasi', 'Jenis Mutasi')
    mati = fields.Boolean('Mati')
    aktif = fields.Boolean('Aktif')
    alamat1 = fields.Char('Alamat 1')
    alamat2 = fields.Char('Alamat 2')
    penerimaan = fields.Float('Penerimaan')
    bertambah = fields.Boolean('Bertambah')
    cat_petugas = fields.Text('Catatan Petugas')

class form_et(models.Model):
    _name = 'form.et'
    _rec_name = 'sapi_id'

    peternak_id = fields.Many2one('peternak.sapi', 'Anggota/Peternak')
    id_pemilik = fields.Char('ID Pemilik', related='peternak_id.kode_peternak')
    kelompok_id = fields.Many2one('peternak.group', related='peternak_id.kelompok_id')
    petugas_id = fields.Many2one('medical.physician', 'Petugas')
    sapi_id = fields.Many2one('sapi', 'Nama Sapi', domain="[('peternak_id', '=', peternak_id)]")
    eartag_id = fields.Char('ID Eartag Sapi')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    kode_embrio = fields.Char('Kode Embrio')
    id_pejantan = fields.Char('ID Pejantan')
    id_donor = fields.Char('ID Donor')
    biaya = fields.Float('Biaya')
    cat_petugas = fields.Text('Catatan Petugas')

class form_gis(models.Model):
    _name = 'form.gis'
    _rec_name = 'sapi_id'

    peternak_id = fields.Many2one('peternak.sapi', 'Anggota/Peternak')
    id_pemilik = fields.Char('ID Pemilik', related='peternak_id.kode_peternak')
    kelompok_id = fields.Many2one('peternak.group', related='peternak_id.kelompok_id')
    petugas_id = fields.Many2one('medical.physician', 'Petugas')
    sapi_id = fields.Many2one('sapi', 'Nama Sapi', domain="[('peternak_id', '=', peternak_id)]")
    eartag_id = fields.Char('ID Eartag Sapi Lama', related='sapi_id.eartag_id')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    eartag_id_baru = fields.Char('ID Eartag Sapi Baru')
    cat_petugas = fields.Text('Catatan Petugas')
    image1 = fields.Char('Gambar1')
    image2 = fields.Char('Gambar2')
    image3 = fields.Char('Gambar3')	

class form_hormon(models.Model):
    _name = 'form.hormon'
    _inherit = 'image.mixin'
    _rec_name = 'eartag_id'
    
    peternak_id = fields.Many2one('peternak.sapi', 'Anggota/Peternak') 
    id_pemilik = fields.Char('ID Pemilik')
    sapi_id = fields.Many2one('sapi', 'Nama Sapi', domain="[('peternak_id', '=', peternak_id)]")
    eartag_id = fields.Char('ID Eartag Sapi')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    cat_petugas = fields.Text('Catatan Petugas')

class form_ib(models.Model):
    _name = 'form.ib'
    _inherit = 'image.mixin'
    _rec_name = 'eartag_id'

    peternak_id = fields.Many2one('peternak.sapi', 'Anggota/Peternak')
    id_pemilik = fields.Char('ID Pemilik', related='peternak_id.kode_peternak')
    kelompok_id = fields.Many2one('peternak.group', related='peternak_id.kelompok_id')
    petugas_id = fields.Many2one('medical.physician', 'Petugas')
    sapi_id = fields.Many2one('sapi', 'Nama Sapi', domain="[('peternak_id', '=', peternak_id)]")
    eartag_id = fields.Char('ID Eartag Sapi')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    bcs = fields.Char('BCS')
    stts_reprod = fields.Selection([
        ('1', 'Tidak Ada'),
        ('2', 'Pernah Di IB/Kawin'),
        ('3', 'Kosong'),
        ('4', 'Bunting'),
        ('5', 'Melahirkan'),
        ('6', 'Donor')
    ], string='Status Reproduksi')
    nama_pejantan = fields.Char('Nama Pejantan')
    id_pejantan = fields.Char('ID Pejantan')
    no_batch = fields.Integer('No Batch')
    lama_birahi = fields.Integer('Lama Birahi')
    ib_ke = fields.Integer('IB Ke')
    pengamat_birahi = fields.Char('Pengamat Birahi')
    dose = fields.Integer('Dosis')
    cat_petugas = fields.Text('Catatan Petugas')


class form_pedet(models.Model):
    _name = 'form.pedet'
    _inherit = 'image.mixin'
    _rec_name = 'eartag_id'

    id_pemilik = fields.Char('ID Pemilik')
    eartag_id = fields.Char('ID Eartag Sapi')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    cat_petugas = fields.Text('Catatan Petugas')

class form_kk(models.Model):
    _name = 'form.kk'
    _inherit = 'image.mixin'
    _rec_name = 'eartag_id'

    peternak_id = fields.Many2one('peternak.sapi', 'Anggota/Peternak')
    id_pemilik = fields.Char('ID Pemilik', related='peternak_id.kode_peternak')
    kelompok_id = fields.Many2one('peternak.group', related='peternak_id.kelompok_id')
    petugas_id = fields.Many2one('medical.physician', 'Petugas')
    sapi_id = fields.Many2one('sapi', 'Nama Sapi', domain="[('peternak_id', '=', peternak_id)]")
    eartag_id = fields.Char('ID Eartag Sapi')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    cat_petugas = fields.Text('Catatan Petugas')
    tipe_pengeringan = fields.Char('Tipe Pengeringan')
    depan_kiri = fields.Char('Depan Kiri')
    depan_kanan = fields.Char('Depan Kanan')
    blkg_kiri = fields.Char('Belakang Kiri')
    blkg_kanan = fields.Char('Belakang Kanan')
    pengobatan1 = fields.Char('Pengobatan Lain#1')
    pengobatan2 = fields.Char('Pengobatan Lain#2')
    saran = fields.Text('Saran')

class form_masuk(models.Model):
    _name = 'form.masuk'
    _inherit = 'image.mixin'
    _rec_name = 'eartag_id'

    id_pemilik = fields.Char('ID Pemilik')
    eartag_id = fields.Char('ID Eartag Sapi')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    cat_petugas = fields.Text('Catatan Petugas')
    eartag = fields.Char('Ear Tag')
    telinga_ki_ka = fields.Char('Telinga Ki/Ka')
    nama_sapi = fields.Char('Nama Sapi')
    tgl_ident = fields.Char('Tanggal Identifikasi')
    breed = fields.Char('Breed')
    metoda = fields.Char('Metoda')
    tgl_lahir = fields.Char('Tanggal Lahir')
    et = fields.Char('ET')
    kembar = fields.Boolean('Kembar')
    tie = fields.Char('TIE')
    kode_klhrn = fields.Char('Kode Kelahiran')
    stts_prod = fields.Char('Status Produksi')
    stts_laktasi = fields.Char('Status Laktasi')
    lak_ke = fields.Char('Laktasi Ke')
    no_induk = fields.Integer('No Induk')
    no_bapak = fields.Integer('No Bapak')

class form_melahirkan(models.Model):
    _name = 'form.melahirkan'
    _inherit = 'image.mixin'
    _rec_name = 'id_pemilik'

    id_pemilik = fields.Char('ID Pemilik')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    id_sapi_induk = fields.Char('ID Sapi Induk')
    eartag_id = fields.Char('ID Eartag Sapi')
    id_sapi_jantan = fields.Char('ID Sapi Jantan')
    tgl_lahir = fields.Datetime('Tanggal Lahir')
    jns_klmn = fields.Selection([
        ('l', 'Laki-Laki'),
        ('p', 'Perempuan'),
    ], string='Jenis Kelamin')
    pengobatan = fields.Char('Pengobatan')
    cat_petugas = fields.Text('Catatan Petugas')
    image = fields.Binary(string='Image')

class form_nkt(models.Model):
    _name = 'form.nkt'
    _inherit = 'image.mixin'
    _rec_name = 'eartag_id'
    
    peternak_id = fields.Many2one('peternak.sapi', 'Anggota/Peternak')
    id_pemilik = fields.Char('ID Pemilik')
    eartag_id = fields.Char('ID Eartag Sapi')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    berat = fields.Float('Berat')
    tinggi = fields.Float('Tinggi')
    cat_petugas = fields.Text('Catatan Petugas')
    image = fields.Binary(string='Image')

class form_pr(models.Model):
    _name = 'form.pr'
    _inherit = 'image.mixin'
    _rec_name = 'eartag_id'

    peternak_id = fields.Many2one('peternak.sapi', 'Anggota/Peternak')
    id_pemilik = fields.Char('ID Pemilik')
    eartag_id = fields.Char('ID Eartag Sapi')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    cat_petugas = fields.Text('Catatan Petugas')
    alsn_pal_rek = fields.Text('Alasan Palpasi Rektal')
    uterus = fields.Char('Uterus')
    ovarikiri = fields.Char('Ovarikiri')
    ovarikanan = fields.Char('Ovarikanan')
    cervix = fields.Char('Cervix')
    perk_siklus = fields.Char('Perkiraan Siklus')


class form_pt(models.Model):
    _name = 'form.pt'
    _inherit = 'image.mixin'
    _rec_name = 'eartag_id'

    peternak_id = fields.Many2one('peternak.sapi', 'Anggota/Peternak')
    id_pemilik = fields.Char('ID Pemilik')
    eartag_id = fields.Char('ID Eartag Sapi')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    pengobatan = fields.Char('Pengobatan')
    cat_petugas = fields.Text('Catatan Petugas')
    image = fields.Binary(string='Image')

class form_sq(models.Model):
    _name = 'form.sq'
    _inherit = 'image.mixin'
    _rec_name = 'eartag_id'

    peternak_id = fields.Many2one('peternak.sapi', 'Anggota/Peternak')
    id_pemilik = fields.Char('ID Pemilik')
    eartag_id = fields.Char('ID Eartag Sapi')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    cat_petugas = fields.Text('Catatan Petugas')
    met_pengh_jss = fields.Char('Metode Penghitungan JSS')
    knn_dpn_jss = fields.Char('Kanan Depan JSS')
    knn_dpn_kuman = fields.Char('Kanan Depan Kuman')
    knn_blkg_jss = fields.Char('Kanan Belakang JSS')
    knn_blkg_kuman = fields.Char('Kanan Belakang Kuman')
    kiri_dpn_jss = fields.Char('Kiri Depan JSS')
    kanan_dpn_kuman = fields.Char('Kanan Depan Kuman')
    kiri_blkg_jss = fields.Char('Kiri Belakang JSS')
    kiri_blkg_kuman = fields.Char('Kiri Belakang Kuman')
    biaya = fields.Boolean('Biaya')

class form_specimen(models.Model):
    _name = 'form.specimen'
    _inherit = 'image.mixin'
    _rec_name = 'eartag_id'

    peternak_id = fields.Many2one('peternak.sapi', 'Anggota/Peternak')
    id_pemilik = fields.Char('ID Pemilik')
    eartag_id = fields.Char('ID Eartag Sapi')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    cat_petugas = fields.Text('Catatan Petugas')
    no_id_sample = fields.Integer('No ID Sample')
    jns_specimen = fields.Char('Jenis Specimen')
    untuk_tes = fields.Char('Untuk Test')

class form_peng_bb_tb(models.Model):
    _name = 'form.peng.bb.tb'
    _inherit = 'image.mixin'
    _rec_name = 'eartag_id'

    peternak_id = fields.Many2one('peternak.sapi', 'Anggota/Peternak')
    id_pemilik = fields.Char('ID Pemilik')
    eartag_id = fields.Char('ID Eartag Sapi')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    cat_petugas = fields.Text('Catatan Petugas')
    nkt = fields.Integer('NKT')
    brt_bdn = fields.Char('Berat Badan')
    tinggi_gumba = fields.Char('Tinggi Gumba')

class form_ganti_pmlk(models.Model):
    _name = 'form.ganti.pmlk'
    _inherit = 'image.mixin'
    _rec_name = 'eartag_id'

    peternak_id = fields.Many2one('peternak.sapi', 'Anggota/Peternak')
    id_pemilik_lama = fields.Char('ID Pemilik Lama')
    eartag_id = fields.Char('ID Eartag Sapi')
    id_pemilik_baru = fields.Char('ID Pemilik Baru')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    alsn_gnti_pmlk = fields.Text('Alasan Ganti Pemilik')
    cat_petugas = fields.Text('Catatan Petugas')

class form_vaksinasi(models.Model):
    _name = 'form.vaksinasi'
    _inherit = 'image.mixin'
    _rec_name = 'eartag_id'

    peternak_id = fields.Many2one('peternak.sapi', 'Anggota/Peternak')
    id_pemilik = fields.Char('ID Pemilik')
    eartag_id = fields.Char('ID Eartag Sapi')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    jns_vaksin = fields.Many2one('master.vaksin', 'Jenis Vaksin')
    dosis = fields.Char('Dosis')
    nama_vaksin = fields.Char('Nama Vaksin')
    cat_petugas = fields.Text('Catatan Petugas')
    image = fields.Binary(string='Image')

class form_susu(models.Model):
    _name = 'form.susu'
    _inherit = 'image.mixin'
    _rec_name = 'eartag_id'

    peternak_id = fields.Many2one('peternak.sapi', 'Anggota/Peternak')
    id_pemilik = fields.Char('ID Pemilik')
    eartag_id = fields.Char('ID Eartag Sapi')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    cat_petugas = fields.Text('Catatan Petugas')
    no_sample = fields.Integer('No Sample')
    susu_pgi = fields.Char('Susu Pagi')
    susu_sre = fields.Char('Susu Sore')
    fat_pgi = fields.Char('Fat Pagi')
    fat_sre = fields.Char('Fat Sore')
    prot_pgi = fields.Char('Protein Pagi')
    prot_sre = fields.Char('Protein Sore')
    jml_susu = fields.Char('Jumlah Susu')
    fat = fields.Float('%Fat')
    protein = fields.Float('%Protein')

class form_pot_kuku(models.Model):
    _name = 'form.pot.kuku'
    _inherit = 'image.mixin'
    _rec_name = 'eartag_id'

    peternak_id = fields.Many2one('peternak.sapi', 'Anggota/Peternak')
    id_pemilik = fields.Char('ID Pemilik')
    eartag_id = fields.Char('ID Eartag Sapi')
    tgl_layanan = fields.Datetime('Tanggal Layanan')
    alsn_ptg_kku = fields.Text('Alasan Potong Kuku')
    dpn_kiri = fields.Char('Depan Kiri')
    dpn_kanan = fields.Char('Depan Kanan')
    blkg_kiri = fields.Char('Belakang Kiri')
    blkg_kanan = fields.Char('Belakang Kanan')
    pngbtn_lain_1 = fields.Char('Pengobatan Lain 1')
    pngbtn_lain_2 = fields.Char('Pengobatan Lain 2')
    cat_petugas = fields.Text('Catatan Petugas')
    image = fields.Binary(string='Image')

class form_ident(models.Model):
    _name = 'form.ident'
    _inherit = 'image.mixin'
    _rec_name = 'eartag_id'

    peternak_id = fields.Many2one('peternak.sapi', 'Anggota/Peternak')
    id_pemilik = fields.Char('ID Pemilik')
    eartag_id = fields.Char('ID Eartag Sapi')
    metode_perolehan = fields.Selection([
        ('1', 'Lahir'),
        ('2', 'Beli'),
        ('3', 'Kredit'),
        ('4', 'Pindah'),
        ('5', 'Bagi Hasil')
    ], string='Metode Perolehan')
    tipe = fields.Selection([
        ('1', 'Pedet BTN'),
        ('2', 'Pedet JTN'),
        ('3', 'Betina Muda'),
        ('4', 'Dara'),
        ('5', 'Induk'),
        ('6', 'Jantan Dewasa'),
        ('7', 'Jantan Kebiri'),
    ], string='Tipe', required=True)
    stts_reprod = fields.Selection([
        ('1', 'Tidak Ada'),
        ('2', 'Pernah Di IB/Kawin'),
        ('3', 'Kosong'),
        ('4', 'Bunting'),
        ('5', 'Melahirkan'),
        ('6', 'Donor')
    ], string='Status Reproduksi')
    laktasi = fields.Selection([
        ('kering', 'Kering'),
        ('laktasi', 'Laktasi'),
        ('tdk', 'Tidak Ada'),
    ], string='Laktasi')
    lak_ke = fields.Integer('Laktasi Ke')
    id_induk = fields.Char('ID Induk')
    id_ayah = fields.Char('ID Ayah')
    tgl_lahir = fields.Date('Tanggal Lahir')
