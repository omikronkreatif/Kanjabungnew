# Copyright (C) 2020 Brahoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _anglo_saxon_sale_move_lines(
        self,
        name,
        product,
        uom,
        qty,
        price_unit,
        currency=False,
        amount_currency=False,
        fiscal_position=False,
        account_analytic=False,
        analytic_tags=False,
    ):
        res = super()._anglo_saxon_sale_move_lines(
            name,
            product,
            uom,
            qty,
            price_unit,
            currency=currency,
            amount_currency=amount_currency,
            fiscal_position=fiscal_position,
            account_analytic=account_analytic,
            analytic_tags=analytic_tags,
        )
        if res:
            res[0]["account_analytic_id"] = account_analytic and account_analytic.id
            res[0]["analytic_tag_ids"] = (
                analytic_tags
                and analytic_tags.ids
                and [(6, 0, analytic_tags.ids)]
                or False
            )
        return res

class ProcurementRule(models.Model):
    _inherit = 'stock.rule'


    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values):
        move_values = super()._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, company_id, values)
        move_values['analytic_account_id'] = values['analytic_account_id']
        return move_values


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    def _prepare_procurement_values(self, group_id=False):
        res = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        # I am assuming field name in both sale.order.line and in stock.move are same and called 'YourField'
        res.update({'analytic_account_id': self.order_id.analytic_account_id.id})
        return res


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _prepare_stock_moves(self, picking):
        res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        for re in res:
            re['analytic_account_id'] = self.account_analytic_id.id
        return res
