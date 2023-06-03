# -*- coding: utf-8 -*-
# Copyright 2020-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _


class TransportShipment(models.Model):
    _name = 'transport.shipment'
    _description = 'Transport Shipment'
    _rec_name = 'code'
    _inherit = ['mail.thread.cc',
                'mail.activity.mixin',
                'format.address.mixin',
                ]

    active = fields.Boolean(default=True)
    color = fields.Integer('Color Index', compute="_get_color_state")
    code = fields.Char(string="Number")
    tracking_ref_no = fields.Char(string="Waybill No")
    reference_no = fields.Char(string="Reference No	")

    route_id = fields.Many2one('transport.route', string="Transport Route", required=True)
    transporter_id = fields.Many2one('transporter.details', string="Transport via", required=True)
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle", required=True)
    driver_id = fields.Many2one('res.partner', domain=[('is_driver', '=', True)], string="Driver", required=True)
    responsible = fields.Many2one('res.users', string="Responsible", default=lambda self: self.env.user.id)
    shipment_date = fields.Datetime(string="Pickup Date")
    delivery_date = fields.Datetime(string="Expected Date of Delivery")
    note = fields.Text(string="Note")
    terms = fields.Html(string="Terms & Conditions")

    rate_per_km = fields.Monetary(string="Tarif", currency_field='currency_id', tracking=True)
    distance = fields.Float(string="Berat")
    total_cost = fields.Monetary(string="Total Charges", currency_field='currency_id', tracking=True)
    currency_id = fields.Many2one("res.currency", string='Currency',
                                  default=lambda self: self.env.company.currency_id.id, readonly=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company.id)
    odometer_start = fields.Integer(string="Odometer Start")
    odometer_end = fields.Integer(string="Odometer End")

    status = fields.Selection([('draft', "TPS"), ('transfer', "Transfer Truck"),
                               ('del_truck', "Delivery Truck"), ('rilis', "Rilis Produk"), ('reject', "Reject"), ('done', "Factory"), ('cancel', "Cancelled")],
                              default='draft')

    shipment_tracking_ids = fields.One2many('shipment.tracking', 'shipment_id', string="Shipment Tracking")
    transport_do_ids = fields.One2many('transport.delivery.order', 'shipment_id', string="Delivery Orders")
    volum_berat = fields.Float('Timbangan Volume/Berat')
    start_time = fields.Datetime('Start Time')
    temperatur = fields.Float('Temperatur')
    #quality
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
    grade = fields.Float('Grade')
    jns_tps = fields.Selection([
        ('cooling', "Cooling"),
        ('non_cool', "Non Cooling")
    ], string='Jenis TPS', default='')

    @api.depends('status')
    def _get_color_state(self):
        for rec in self:
            if rec.status == 'draft':
                rec.color = 0  # 1 danger 2 orange 10 green 4 info
            elif rec.status == 'rilis':
                rec.color = 10
            elif rec.status == 'transfer':
                rec.color = 2
            elif rec.status == 'del_truck':
                rec.color = 4
            else:
                rec.color = 1

    @api.onchange('transporter_id', 'route_id')
    def get_transport_route_details(self):
        for rec in self:
            if rec.transporter_id:
                rec.rate_per_km = rec.transporter_id.transport_charge
            if rec.route_id:
                rec.distance = rec.route_id.distance

            if rec.transporter_id and rec.route_id:
                rec.total_cost = rec.rate_per_km * rec.distance

    @api.onchange('rate_per_km', 'distance')
    def get_transport_cost(self):
        for rec in self:
            if rec.rate_per_km and rec.distance:
                rec.total_cost = rec.rate_per_km * rec.distance

    @api.model
    def create(self, vals):
        if vals.get("code", "") == "":
            vals["code"] = self.env["ir.sequence"].next_by_code(
                "transport.shipment")
        shipment_id = super(TransportShipment, self).create(vals)

        return shipment_id

    def shipment_transfer(self):
        for rec in self:
            rec.status = 'transfer'
            for do in rec.transport_do_ids:
                if do.status == 'draft':
                    do.status = 'transfer'

    def shipment_del_truck(self):
        for rec in self:
            rec.status = 'del_truck'
            for do in rec.transport_do_ids:
                if do.status == 'transfer':
                    do.status = 'del_truck'

    def shipment_rilis(self):
        for rec in self:
            rec.status = 'rilis'
            for do in rec.transport_do_ids:
                if do.status == 'del_truck':
                    do.status = 'rilis'

    def shipment_reject(self):
        for rec in self:
            rec.status = 'reject'
            for do in rec.transport_do_ids:
                if do.status == 'rilis':
                    do.status = 'reject'

    def shipment_delivered(self):
        for rec in self:
            rec.status = 'done'
            for do in rec.transport_do_ids:
                if do.status == 'rilis':
                    do.status = 'done'

    def shipment_cancel(self):
        for rec in self:
            rec.status = 'cancel'
            for do in rec.transport_do_ids:
                do.status = 'cancel'

    @api.model
    def get_shipment_stats(self):
        transport_shipment = self.env['transport.shipment'].sudo()
        ts_all = transport_shipment.search_count([])
        ts_pack = transport_shipment.search_count([('status', '=', 'draft')])
        ts_ship = transport_shipment.search_count([('status', '=', 'ship')])
        ts_transit = transport_shipment.search_count([('status', '=', 'in_transit')])
        ts_done = transport_shipment.search_count([('status', '=', 'done')])
        ts_cancel = transport_shipment.search_count([('status', '=', 'cancel')])

        return {
            'all': ts_all,
            'pack': ts_pack,
            'ship': ts_ship,
            'transit': ts_transit,
            'done': ts_done,
            'cancel': ts_cancel,
        }


class TransportShipmentTracking(models.Model):
    _name = 'shipment.tracking'
    _description = "Transport Shipment Tracking"

    tracking_date = fields.Date(string="Shipment Date")
    tracking_time = fields.Float(string="Time (24 Hrs. Format)")
    shipment_operation_id = fields.Many2one('shipment.operation', string="Shipment Operation")
    location = fields.Char(string="Location")
    shipment_id = fields.Many2one('transport.shipment')


class ShipmentOperation(models.Model):
    _name = 'shipment.operation'
    _description = "Transport Shipment Operation"

    name = fields.Char(string="Type of Operation", required=True)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    shipment_id = fields.Many2one('transport.shipment', string="Shipment")


class TransportDeliveryOrders(models.Model):
    _name = 'transport.delivery.order'
    _description = 'Transport Delivery Order'

    color = fields.Integer(compute='_get_color_state')
    name = fields.Many2one('stock.picking', string="Picking Order")
    so_id = fields.Many2one(related='name.sale_id', string="Sale Order")
    source_location_id = fields.Many2one('transport.location', string="Source Location")
    destination_location_id = fields.Many2one('transport.location', string="Destination Location")
    status = fields.Selection([('draft', "Packing"), ('ship', "Shipping"),
                               ('in_transit', "In Transit"), ('done', "Delivered"), ('cancel', "Cancelled")],
                              default='draft')
    shipment_id = fields.Many2one('transport.shipment', string="Shipment")

    @api.depends('status')
    def _get_color_state(self):
        for rec in self:
            if rec.status == 'draft':
                rec.color = 0  # 1 danger 2 orange 10 green 4 info
            elif rec.status == 'done':
                rec.color = 10
            elif rec.status == 'in_transit':
                rec.color = 2
            elif rec.status == 'ship':
                rec.color = 4
            else:
                rec.color = 1