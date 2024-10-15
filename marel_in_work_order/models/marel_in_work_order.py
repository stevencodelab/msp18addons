from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

# -------------------------------- 25/10/21 table Operator rijek kaoskaki------------------------

class TargetProduksi(models.Model):
    _name = 'target.produksi'
    _description = u'Target Produksi'
    _rec_name = 'target'
    
    
    target = fields.Char(string='Target',default='Target',store=True)
    target_knitting = fields.Integer(string='Target Knitting',store=True)
    target_conti = fields.Integer(string='Target Conti',store=True)
    target_sewing = fields.Integer(string='Target Sewing',store=True)
    target_as = fields.Integer(string='Target Anti Slip',store=True)
    target_setting = fields.Integer(string='Target Setting',store=True)
    target_bordir = fields.Integer(string='Target Bordir',store=True)
    marel_nama_operatorlist_ids = fields.One2many('marel.nama.operatorlist','target_produksi_id',string='Operator Rijek Kaoskaki',)


class JenisRijekKaoskaki(models.Model):
    _name = 'jenis.rijek.kaoskaki'
    _description = u'Jenis Rijek Kaoskaki'

    name = fields.Char(string='Jenis Rijek',)
    active = fields.Boolean(default=True, help="If the active field is set to False, it will allow you to hide the payment terms without removing it.")

class OperatorRijekKaoskaki(models.Model):
    _name = 'operator.rijek.kaoskaki'
    _description = u'Operator Rijek Kaoskaki'

    marel_nama_operatorlist_id = fields.Many2one('marel.nama.operatorlist',string='Nama Operatorlist',)

    jenis_rijek_kaoskaki_id = fields.Many2one('jenis.rijek.kaoskaki',string='Jenis Rijek Kaoskaki',)
    keterangan = fields.Text(string='keterangan',)
    jumlah_rjk = fields.Integer( string='Jumlah Rijek', )
# ---------------------------------------- beda data -----------------------
class MarelNamaOperatorList(models.Model):
    
    _name = 'marel.nama.operatorlist'
    _description = u'Marel Nama Operator'
    _rec_name = 'nama_operator_id'


    workcenter_id = fields.Many2one('mrp.workcenter', 'Work Center',store=True)
    target_produksi_id = fields.Many2one('target.produksi', 'Target Produksi', store=True,default=1)

    # production_id = fields.Many2one('mrp.production', 'Production', store=True)
    workorder_id = fields.Many2one('mrp.workorder', 'Workorder', store=True)
    operator_rijek_kaoskaki_ids = fields.One2many('operator.rijek.kaoskaki','marel_nama_operatorlist_id',string='Operator Rijek Kaoskaki',)

    # @api.model
    # def _default_no_mesin(self):
    #      return self.env['mesin.marel.produksi'].search([('id', '=',206)],limit=1)
    
    # nama_operator_id = fields.Many2one('hr.employee',string=u'Nama Operator', domain = "[('job_id','=',12)]")
    # nama_qiusi_id = fields.Many2one('hr.employee',string=u'Nama Qiusi', domain = "['|',('job_id','=',14),('job_id','=',15)]")
    nama_operator_id = fields.Many2one('hr.employee',string=u'Nama Operator', )
    nama_qiusi_id = fields.Many2one('hr.employee',string=u'Nama Qiusi', )
    no_mesin_id = fields.Many2one('mesin.marel.produksi',string=u'No Mesin',)
    # no_mesin_id = fields.Many2one('mesin.marel.produksi',string=u'No Mesin', default=_default_no_mesin)
    shift = fields.Selection([
        ('A',_('A')),
        ('B',_('B')),
	    ('C',_('C')),], string="Shift",)
    no_kkp = fields.Char(string=u'No KKP',)
    jumlah_reject = fields.Integer(string=u'Jumlah Reject',compute='_get_jumlah_semua_rijek',store=True)
    tgl_kerja = fields.Date(string=u'tgl Kerja',default=fields.Date.context_today,)
    jumlah_yg_selesai = fields.Integer(string=u'Qty Yg Selesai',)
    # jumlah_yg_selesai_sementara = fields.Integer(string=u'Qty Yg Selesai backUp',)
    krono_kk_menit = fields.Float(string=u'Krono KK (menit)',default=3.0)
    jam_kerja = fields.Float(string=u'Jam Kerja', default=480.0,readonly = True,)
    # gread_d = fields.Integer(string="Gread D",)

    status = fields.Selection([
        ('draft', 'Draft'),
        ('done','Done'),
        ('cancel','Canceled')
        ],string="Status", readonly=True, copy=False, default='draft')

    target_knitting = fields.Integer(string=u'Target KK Operator',store=True,related='target_produksi_id.target_knitting',)
    target_conti = fields.Integer(string='Target Conti',store=True,related='target_produksi_id.target_conti',)
    target_as = fields.Integer(string='Target Anti Slip',store=True,related='target_produksi_id.target_as',)
    target_sewing = fields.Integer(string='Target Sewing',store=True,related='target_produksi_id.target_sewing',)
    target_bordir = fields.Integer(string='Target Bordir',store=True,related='target_produksi_id.target_bordir',)
    target_setting = fields.Integer(string='Target Setting',store=True,related='target_produksi_id.target_bordir',)

    # @api.model
    # def _default_no_box_packing (self):
    #     for l in self :
    #         if l.workcenter_id == 8 :
    #             l.no_box != 0
    #         else :
    #             l.no_box == 0

    # no_box = fields.Integer(string='No Box', default=_default_no_box_packing, )

    # def action_confirm_value_fix(self):
    #     for l in self :
    #         if (l.production_id.product_uom_id.id == 21) & (l.production_id.workcenter_id.id != 8):
    #             if l.jumlah_yg_selesai_sementara != 0:
    #                 l.jumlah_yg_selesai = ((l.jumlah_yg_selesai_sementara)/2)
    #             l.write({'status': 'done'})
    #         else :
    #             if l.jumlah_yg_selesai_sementara != 0:
    #                 l.jumlah_yg_selesai = l.jumlah_yg_selesai_sementara
    #             l.write({'status': 'done'})
    #     self._action_ubah_data()
    #     self._get_mengisi_krono_kk()
    #     self._get_target_conti()
    #     self._get_target_as()
    #     self._get_target_sewing()
    #     self._get_target_bordir()
    #     self._get_target_setting()

    # def _action_ubah_data(self):
    #     for l in self :
    #         if l.status == 'done':
    #             l.jumlah_yg_selesai_sementara = 0

    # def _get_mengisi_krono_kk(self):
    #     for l in self :
    #         if l.jam_kerja > 0.0 :
    #             l.target_knitting = int(l.jam_kerja/l.krono_kk_menit)

    # def _get_target_conti(self):
    #     for l in self :
    #         if l.production_id.target_conti == 5000:
    #             l.target_conti = l.production_id.target_conti

    
    # def _get_target_as(self):
    #     for l in self :
    #         if l.production_id.target_as > 0:
    #             l.target_as = l.production_id.target_as

    
    # def _get_target_sewing(self):
    #     for l in self :
    #         if l.production_id.target_sewing > 0:
    #             l.target_sewing = l.production_id.target_sewing

    
    # def _get_target_bordir(self):
    #     for l in self :
    #         if l.production_id.target_bordir > 0:
    #             l.target_bordir = l.production_id.target_bordir

    
    # def _get_target_setting(self):
    #     for l in self :
    #         if l.production_id.target_setting == 12000:
    #             l.target_setting = l.production_id.target_setting

    @api.depends('operator_rijek_kaoskaki_ids')
    def _get_jumlah_semua_rijek(self):
        for marel_nama_operatorlist_id in self:
            marel_nama_operatorlist_id.jumlah_reject = sum((line_id.jumlah_rjk) for line_id in marel_nama_operatorlist_id.operator_rijek_kaoskaki_ids)


class MrpWorkorder(models.Model):
    _inherit = ['mrp.workorder']

    marel_nama_operatorlist_ids = fields.One2many('marel.nama.operatorlist','workorder_id',string=u'Nama Operator ',required=True,)
    
    jumlah_reject_wo = fields.Integer(string=u'Jumlah Rijek WO',compute='_get_jumlah_semua_rijek_wo',store=True)
    jumlah_selesai_wo = fields.Integer(string=u'Jumlah Selesai WO',compute='_get_jumlah_semua_selesai_wo',store=True)

    @api.depends('marel_nama_operatorlist_ids')
    def _get_jumlah_semua_rijek_wo(self):
        for nama_operator_work_order_id in self:
            nama_operator_work_order_id.jumlah_reject_wo = sum((line_id.jumlah_reject) for line_id in nama_operator_work_order_id.marel_nama_operatorlist_ids)

    @api.depends('marel_nama_operatorlist_ids')
    def _get_jumlah_semua_selesai_wo(self):
        for nama_operator_work_order_id in self:
            nama_operator_work_order_id.jumlah_selesai_wo = sum((line_id.jumlah_yg_selesai) for line_id in nama_operator_work_order_id.marel_nama_operatorlist_ids)



    # target_conti = fields.Integer(string='Target Conti',)
    # target_as = fields.Integer(string='Target Anti Slip',)
    # target_sewing = fields.Integer(string='Target Sewing',)
    # target_bordir = fields.Integer(string='Target Bordir',)
    # target_setting = fields.Integer(string='Target Setting',)

    # qty_producing = fields.Float('Currently Produced Quantity', default=1.0,digits=dp.get_precision('Product Unit of Measure'),states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, compute='_get_jumlah_yg_selesai_producing',)


    # qty_input_operator = fields.Float(string='Qty Input Operator', compute='_get_jumlah_yg_selesai', store=True)
    # jumlah_reject_wo = fields.Integer(string=u'Jumlah Rijek WO',compute='_get_jumlah_semua_rijek_wo',store=True)
    # jumlah_selesai_wo = fields.Integer(string=u'Jumlah Selesai WO',compute='_get_jumlah_semua_selesai_wo',store=True)
    # total_putus_benang = fields.Integer(string=u'Total Pts Benang',compute='_get_jumlah_yg_selesai_total_putus_benang',store=True)
    # total_bolong = fields.Integer(string=u'Total BOLONG / SOBEK',compute='_get_jumlah_yg_selesai_total_bolong',store=True)
    # total_vanise = fields.Integer(string=u'Total VANISE',compute='_get_jumlah_yg_selesai_total_vanise',store=True)
    # total_singker = fields.Integer(string=u' SINGKER/ LIDAH SERET',compute='_get_jumlah_yg_selesai_total_singker',store=True)
    # total_kotor = fields.Integer(string=u'Total KOTOR',compute='_get_jumlah_yg_selesai_total_kotor',store=True)
    # total_terry = fields.Integer(string=u'Total TERRY',compute='_get_jumlah_yg_selesai_total_terry',store=True)
    # total_jumpstich = fields.Integer(string=u'Total JUMPSTICH',compute='_get_jumlah_yg_selesai_total_jumpstich',store=True)
    # total_renggang = fields.Integer(string=u'Total RENGGANG',compute='_get_jumlah_yg_selesai_total_renggang',store=True)
    # total_tidak_loading = fields.Integer(string=u'Total TIDAK LOADING',compute='_get_jumlah_yg_selesai_total_tidak_loading',store=True)
    # total_belang = fields.Integer(string=u'Total BELANG',compute='_get_jumlah_yg_selesai_total_belang',store=True)
    # total_ukuran = fields.Integer(string=u'Total UKURAN',compute='_get_jumlah_yg_selesai_total_ukuran',store=True)
    # total_lingtu = fields.Integer(string=u'Total LINGTU',compute='_get_jumlah_yg_selesai_total_lingtu',store=True)
    # total_pecah = fields.Integer(string=u'Total PECAH',compute='_get_jumlah_yg_selesai_total_pecah',store=True)
    # total_loncat = fields.Integer(string=u'Total LONCAT',compute='_get_jumlah_yg_selesai_total_loncat',store=True)
    # total_transfer = fields.Integer(string=u'Total TRANSFER NYANGKOL',compute='_get_jumlah_yg_selesai_total_transfer',store=True)
    # total_gumpal = fields.Integer(string=u'Total GUMPAL',compute='_get_jumlah_yg_selesai_total_gumpal',store=True)
    # total_kasar = fields.Integer(string=u'Total KASAR',compute='_get_jumlah_yg_selesai_total_kasar',store=True)
    # total_benang_gabung = fields.Integer(string=u'Total BENANG GABUNG',compute='_get_jumlah_yg_selesai_total_benang_gabung',store=True)
    # total_bintik_bintik = fields.Integer(string=u'Total BINTIK BINTIK',compute='_get_jumlah_yg_selesai_total_bintik_bintik',store=True)
    # total_jarum = fields.Integer(string=u'Total Jarum',compute='_get_jumlah_yg_selesai_total_jarum',store=True)
    # total_transfer_jebol = fields.Integer(string=u'Total TRANSFER Jebol',compute='_get_jumlah_yg_selesai_total_transfer_jebol',store=True)
    

    # def write(self, values):
    #     if ('date_planned_start' in values or 'date_planned_finished' in values):
    #         raise UserError(_('You can not change the finished work order.'))
    #     return super(MarelInWorkOrder, self).write(values)


    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_semua_rijek_wo(self):
    #     for production_id in self:
    #         production_id.jumlah_reject_wo = sum((line_id.jumlah_reject) for line_id in production_id.marel_nama_operatorlist_ids)

    
    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_semua_selesai_wo(self):
    #     for production_id in self:
    #         production_id.jumlah_selesai_wo = sum((line_id.jumlah_yg_selesai) for line_id in production_id.marel_nama_operatorlist_ids)


    
    # def get_kurangi_jumlah_kkp(self):
    #     self.qty_producing = 0
    #     kurang_kkp = (self.qty_producing + self.jumlah_yg_dikurangi)/2
    #     self.qty_producing = kurang_kkp
    #     return
    
    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai(self):
    #     for production_id in self:
    #         production_id.qty_input_operator = sum((line_id.jumlah_yg_selesai_sementara) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_total_putus_benang(self):
    #     for production_id in self:
    #         production_id.total_putus_benang = sum((line_id.putus_benang) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_total_bolong(self):
    #     for production_id in self:
    #         production_id.total_bolong = sum((line_id.bolong) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_total_vanise(self):
    #     for production_id in self:
    #         production_id.total_vanise = sum((line_id.vanise) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_total_singker(self):
    #     for production_id in self:
    #         production_id.total_singker = sum((line_id.singker) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_total_kotor(self):
    #     for production_id in self:
    #         production_id.total_kotor = sum((line_id.kotor) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_total_terry(self):
    #     for production_id in self:
    #         production_id.total_terry = sum((line_id.terry) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_total_jumpstich(self):
    #     for production_id in self:
    #         production_id.total_jumpstich = sum((line_id.jumpstich) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_total_renggang(self):
    #     for production_id in self:
    #         production_id.total_renggang = sum((line_id.renggang) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_total_tidak_loading(self):
    #     for production_id in self:
    #         production_id.total_tidak_loading = sum((line_id.tidak_loading) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_total_belang(self):
    #     for production_id in self:
    #         production_id.total_belang = sum((line_id.belang) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_total_ukuran(self):
    #     for production_id in self:
    #         production_id.total_ukuran = sum((line_id.ukuran) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_total_lingtu(self):
    #     for production_id in self:
    #         production_id.total_lingtu = sum((line_id.lingtu) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_total_pecah(self):
    #     for production_id in self:
    #         production_id.total_pecah = sum((line_id.pecah) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_total_loncat(self):
    #     for production_id in self:
    #         production_id.total_loncat = sum((line_id.loncat) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_total_transfer(self):
    #     for production_id in self:
    #         production_id.total_transfer = sum((line_id.transfer) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_total_gumpal(self):
    #     for production_id in self:
    #         production_id.total_gumpal = sum((line_id.gumpal) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_total_kasar(self):
    #     for production_id in self:
    #         production_id.total_kasar = sum((line_id.kasar) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_total_benang_gabung(self):
    #     for production_id in self:
    #         production_id.total_benang_gabung = sum((line_id.benang_gabung) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_total_bintik_bintik(self):
    #     for production_id in self:
    #         production_id.total_bintik_bintik = sum((line_id.bintik_bintik) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_total_jarum(self):
    #     for production_id in self:
    #         production_id.total_jarum = sum((line_id.jarum) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_total_transfer_jebol(self):
    #     for production_id in self:
    #         production_id.total_transfer_jebol = sum((line_id.transfer_jebol) for line_id in production_id.marel_nama_operatorlist_ids)

    # @api.depends('marel_nama_operatorlist_ids')
    # def _get_jumlah_yg_selesai_producing(self):
    #     if (self.product_uom_id.id == 21) & (self.workcenter_id.id != 8):
    #         for production_id in self:
    #             production_id.qty_producing = sum(((line_id.jumlah_yg_selesai_sementara)/2) for line_id in production_id.marel_nama_operatorlist_ids)
    #     else:
    #         for production_id in self:
    #             production_id.qty_producing = sum((line_id.jumlah_yg_selesai_sementara) for line_id in production_id.marel_nama_operatorlist_ids)

    
    # def record_production_2(self):
    #     self.ensure_one()
    #     if self.qty_producing <= 0:
    #         raise UserError(_('Please set the quantity you are currently producing. It should be different from zero.'))

    #     self.record_production()
    #     self.marel_nama_operatorlist_ids.action_confirm_value_fix()
