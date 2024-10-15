from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

class MrpProduction(models.Model):
    _inherit = ['mrp.production']


    total_qty_done = fields.Integer(string='Total Done',compute='_get_jumlah_total_done',store=True)

    @api.depends('move_raw_ids')
    def _get_jumlah_total_done(self):
        for production_id in self:
            production_id.total_qty_done = sum((line_id.qty_done) for line_id in production_id.finished_move_line_ids)


    qty_kekurangan = fields.Float(string='Qty Kekurangan',compute='_get_jumlah_qty_kekurangan',store=True)

    @api.depends('move_raw_ids')
    def _get_jumlah_qty_kekurangan(self):
        for production_id in self:
            production_id.qty_kekurangan = production_id.product_qty - production_id.total_qty_done


    jumlah_reject_mo = fields.Float(string=u'Jumlah Rijek MO',compute='_get_jumlah_semua_rijek_mo',store=True)

    @api.depends('move_raw_ids')
    def _get_jumlah_semua_rijek_mo(self):
        for production_id in self:
            production_id.jumlah_reject_mo = sum((line_id.jumlah_reject_wo) for line_id in production_id.workorder_ids)