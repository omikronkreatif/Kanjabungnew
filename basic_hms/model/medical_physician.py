# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _

class medical_physician(models.Model):
    _name="medical.physician"
    _rec_name = 'nama_petugas'

    kode_petugas = fields.Char('kode Petugas')
    nama_petugas = fields.Char('Nama Petugas')
    # jabatan_id
    gender = fields.Selection([
        ('laki', 'Laki-Laki'),
        ('p', 'Perempuan'),
        ('l', 'Lainnya'),
    ], string='Jenis Kelamin')
    email = fields.Char(string='Email', required=True)
    no_hp = fields.Char(string='Handphone', track_visibility='onchange')
    kelurahan_id = fields.Many2one('wilayah.kelurahan', string='Kelurahan', track_visibility='onchange')
    kecamatan_id = fields.Many2one('wilayah.kecamatan', string='Kecamatan', track_visibility='onchange')
    kabkota_id = fields.Many2one('wilayah.kabkota', string='Kab / Kota', track_visibility='onchange')
    provinsi_id = fields.Many2one('wilayah.provinsi', string='Provinsi')
    wilayah_id = fields.Many2one('master.wilayah', 'Wilayah', required=True)
    partner_id = fields.Many2one('res.partner', 'Partner')
