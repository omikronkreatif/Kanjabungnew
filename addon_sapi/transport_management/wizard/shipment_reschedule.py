# -*- coding: utf-8 -*-
# Copyright 2020-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _


class ShipmentReschedule(models.TransientModel):
    _name = 'shipment.reschedule'
    _description = 'Shipment Reschedule'

    pickup_date = fields.Datetime(string="Pickup Date", required=True)
    delivery_date = fields.Datetime(string="Expected Delivery Date", required=True)

    def shipment_reschedule(self):
        shipment_order_id = self._context.get('active_id')
        shipment_order = self.env['transport.shipment'].sudo().search([('id', '=', int(shipment_order_id))])
        shipment_order.write({
            'shipment_date': self.pickup_date,
            'delivery_date': self.delivery_date,
            'status': 'draft',
        })
        for do in shipment_order.transport_do_ids:
            if do.status == 'cancel':
                do.status = 'draft'

