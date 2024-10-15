from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class TemuanOption(models.Model):
    _name = 'temuan.option'
    _description = 'Temuan Option'

    name = fields.Char(string='Jenis Temuan', required=True)

class PengecekanSample(models.Model):
    _name = 'pengecekan.sample'
    _description = 'Pengecekan Sample'    

    name = fields.Char('Reference', copy=False, readonly=True,default='New')
    
    # Kode Untuk Sequence QC/SHTL/0000
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('pengecekan.sample.sequence') or 'New'
        return super(PengecekanSample, self).create(vals)

    product_id = fields.Many2one('product.product', compute='_compute_product_id', store=True)

    pengecekan_sample_line = fields.One2many('pengecekan.sample.line', 'pengecekan_sample_id')

    manufacturing_order = fields.Many2one('mrp.production', string='Manufacturing Order')

    marel_sample_id = fields.Many2one('msp.sample.dev', string='Sample Development')
    timestamp = fields.Datetime(string='Timestamp', default=fields.Datetime.now, readonly=True)
    tgl_buat = fields.Date(string='Tanggal', default=fields.Date.context_today)
    tgl_mulai = fields.Date(string='Tanggal Mulai')
    tgl_selesai = fields.Datetime(string=u'Tanggal Selesai',readonly=True)
    nama_operator_id = fields.Many2one('marel.nama.qiusi', string='Inspector')
    temuan = fields.Char(string='Temuan')
    no_mesin = fields.Many2one('mesin.marel.produksi', string='Mesin')
    style = fields.Char(string='Style', related='marel_sample_id.style')
    warna = fields.Char(string='Warna', related='marel_sample_id.warna')
    keterangan = fields.Text(string='Keterangan')
    
    state = fields.Selection(
        [('draft', 'Pending'),
         ('ready', 'Ready'),
         ('waiting', 'Waiting For Approval'),
         ('success', 'Check Success'),
         ('failed', 'Check Failed'),
         ('canceled', 'Canceled')],
        string='State', readonly=True, default='draft',
        track_visibility='onchange',
        widget='statusbar',
        statusbar_colors='{"success": "green", "failed": "red", "canceled": "red"}',
        )
    success_header = fields.Boolean(
        compute="_compute_success_header", string='Status',
        help='This field will be marked if all tests have succeeded.',
        store=True)

    gum_relaxed_x= fields.Float(string='Gum Relaxed x ', related='marel_sample_id.gum_relaxed_x')
    gum_relaxed_y= fields.Float(string='Gum Relaxed y ',related='marel_sample_id.gum_relaxed_y')

    leg_gum_relaxed_x= fields.Float(string='Leg Gum Relaxed x ',related='marel_sample_id.leg_gum_relaxed_x')
    leg_gum_relaxed_y= fields.Float(string='Leg Gum Relaxed y ',related='marel_sample_id.leg_gum_relaxed_y')

    leg_gum_atas_relaxed_x= fields.Float(string='Leg Gum Atas Relaxed x ',)
    leg_gum_atas_relaxed_y= fields.Float(string='Leg Gum Atas Relaxed y ',)

    leg_gum_bawah_relaxed_x= fields.Float(string='Leg Gum Bawah Relaxed x ',related='marel_sample_id.leg_gum_bawah_relaxed_x')
    leg_gum_bawah_relaxed_y= fields.Float(string='Leg Gum Bawah Relaxed y ',related='marel_sample_id.leg_gum_bawah_relaxed_y')

    leg_relaxed_x= fields.Float(string=' Leg Relaxed x',related='marel_sample_id.leg_relaxed_x')
    leg_relaxed_y= fields.Float(string='Leg Relaxed y ',related='marel_sample_id.leg_relaxed_y')
    
    foot_relaxed_x= fields.Float(string=' Foot Relaxed x',related='marel_sample_id.foot_relaxed_x')
    foot_relaxed_y= fields.Float(string=' Foot Relaxed y',related='marel_sample_id.foot_relaxed_y')

    foot_gum_relaxed_x= fields.Float(string='Foot Gum Relaxed x ',related='marel_sample_id.foot_gum_relaxed_x')
    foot_gum_relaxed_y= fields.Float(string='Foot Gum Relaxed y ',related='marel_sample_id.foot_gum_relaxed_y')

    hell_relaxed_x= fields.Float(string='Heel Relaxed x ',)
    hell_relaxed_y= fields.Float(string='Heel Relaxed y ',)

    #tambhan 190820---------------------------------
    gum_atas_relaxed_x = fields.Float(string='Gum Atas Relaxed X',)
    gum_atas_relaxed_y = fields.Float(string='Gum Atas Relaxed Y',)

    gum_bawah_relaxed_x = fields.Float(string='Gum Bawah relaxed X',)
    gum_bawah_relaxed_y = fields.Float(string='Gum Bawah Relaxed Y' ,)
    
    leg_gum_tengah_relaxed_x = fields.Float(string='Leg Gum Tengah Relaxed X',)
    leg_gum_tengah_relaxed_y = fields.Float(string='Leg Gum Tengah Relaxed Y',)
    
    #Tambahan relaxedout 20230413
    gum_relaxed_out_x= fields.Float(string='Gum Relaxed Out X',)
    gum_relaxed_out_y= fields.Float(string='Gum Relaxed Out Y',)

    leg_gum_relaxed_out_x= fields.Float(string='Leg Gum Relaxed Out X',)
    leg_gum_relaxed_out_y= fields.Float(string='Leg Gum Relaxed Out Y',)

    leg_gum_atas_relaxed_out_x= fields.Float(string='Leg Gum Atas Relaxed Out X',)
    leg_gum_atas_relaxed_out_y= fields.Float(string='Leg Gum Atas Relaxed Out Y',)

    leg_gum_bawah_relaxed_out_x= fields.Float(string='Leg Gum Bawah Relaxed Out X',)
    leg_gum_bawah_relaxed_out_y= fields.Float(string='Leg Gum Bawah Relaxed Out Y',)

    leg_relaxed_out_x= fields.Float(string=' Leg Relaxed Out X',)
    leg_relaxed_out_y= fields.Float(string='Leg Relaxed Out Y',)

    foot_relaxed_out_x= fields.Float(string=' Foot Relaxed Out X',)
    foot_relaxed_out_y= fields.Float(string=' Foot Relaxed Out Y',)

    foot_gum_relaxed_out_x= fields.Float(string='Foot Gum Relaxed Out X',)
    foot_gum_relaxed_out_y= fields.Float(string='Foot Gum Relaxed Out Y',)

    heel_relaxed_out_x= fields.Float(string='Heel Relaxed Out X',)
    heel_relaxed_out_y= fields.Float(string='Heel Relaxed Out Y',)

    gum_atas_relaxed_out_x = fields.Float(string='Gum Atas Relaxed Out X',)
    gum_atas_relaxed_out_y = fields.Float(string='Gum Atas Relaxed Out Y',)

    gum_bawah_relaxed_out_x = fields.Float(string='Gum Bawah Relaxed Out X',)
    gum_bawah_relaxed_out_y = fields.Float(string='Gum Bawah Relaxed Out Y' ,)
    
    leg_gum_tengah_relaxed_out_x = fields.Float(string='Leg Gum Tengah Relaxed Out X',)
    leg_gum_tengah_relaxed_out_y = fields.Float(string='Leg Gum Tengah Relaxed Out Y',)

    @api.onchange('marel_sample_id')
    def _onchange_marel_sample_id(self):
        if self.marel_sample_id and self.marel_sample_id.state == 'done':
            self.style= self.marel_sample_id.style
            self.warna=self.marel_sample_id.warna
            self.gum_relaxed_x = self.marel_sample_id.gum_relaxed_x
            self.gum_relaxed_y = self.marel_sample_id.gum_relaxed_y
            self.leg_gum_relaxed_x = self.marel_sample_id.leg_gum_relaxed_x
            self.leg_gum_relaxed_y = self.marel_sample_id.leg_gum_relaxed_y
            self.leg_gum_atas_relaxed_x = self.marel_sample_id.leg_gum_atas_relaxed_x
            self.leg_gum_atas_relaxed_y = self.marel_sample_id.leg_gum_atas_relaxed_y
            self.leg_gum_bawah_relaxed_x = self.marel_sample_id.leg_gum_bawah_relaxed_x
            self.leg_gum_bawah_relaxed_y = self.marel_sample_id.leg_gum_bawah_relaxed_y
            self.leg_relaxed_x = self.marel_sample_id.leg_relaxed_x
            self.leg_relaxed_y = self.marel_sample_id.leg_relaxed_y
            self.foot_relaxed_x = self.marel_sample_id.foot_relaxed_x
            self.foot_relaxed_y = self.marel_sample_id.foot_relaxed_y
            self.foot_gum_relaxed_x = self.marel_sample_id.foot_gum_relaxed_x
            self.foot_gum_relaxed_y = self.marel_sample_id.foot_gum_relaxed_y
            self.hell_relaxed_x = self.marel_sample_id.hell_relaxed_x
            self.hell_relaxed_y = self.marel_sample_id.hell_relaxed_y
            self.gum_atas_relaxed_x = self.marel_sample_id.gum_atas_relaxed_x
            self.gum_atas_relaxed_y = self.marel_sample_id.gum_atas_relaxed_y
            self.gum_bawah_relaxed_x = self.marel_sample_id.gum_bawah_relaxed_x
            self.gum_bawah_relaxed_y = self.marel_sample_id.gum_bawah_relaxed_y
            self.leg_gum_tengah_relaxed_x = self.marel_sample_id.leg_gum_tengah_relaxed_x
            self.leg_gum_tengah_relaxed_y = self.marel_sample_id.leg_gum_tengah_relaxed_y
            self.gum_relaxed_out_x = self.marel_sample_id.gum_relaxed_out_x
            self.gum_relaxed_out_y = self.marel_sample_id.gum_relaxed_out_y
            self.leg_gum_relaxed_out_x = self.marel_sample_id.leg_gum_relaxed_out_x
            self.leg_gum_relaxed_out_y = self.marel_sample_id.leg_gum_relaxed_out_y
            self.leg_gum_atas_relaxed_out_x = self.marel_sample_id.leg_gum_atas_relaxed_out_x
            self.leg_gum_atas_relaxed_out_y = self.marel_sample_id.leg_gum_atas_relaxed_out_y
            self.leg_gum_bawah_relaxed_out_x = self.marel_sample_id.leg_gum_bawah_relaxed_out_x
            self.leg_gum_bawah_relaxed_out_y = self.marel_sample_id.leg_gum_bawah_relaxed_out_y
            self.leg_relaxed_out_x = self.marel_sample_id.leg_relaxed_out_x
            self.leg_relaxed_out_y = self.marel_sample_id.leg_relaxed_out_y
            self.foot_relaxed_out_x = self.marel_sample_id.foot_relaxed_out_x
            self.foot_relaxed_out_y = self.marel_sample_id.foot_relaxed_out_y
            self.foot_gum_relaxed_out_x = self.marel_sample_id.foot_gum_relaxed_out_x
            self.foot_gum_relaxed_out_y = self.marel_sample_id.foot_gum_relaxed_out_y
            self.heel_relaxed_out_x = self.marel_sample_id.heel_relaxed_out_x
            self.heel_relaxed_out_y = self.marel_sample_id.heel_relaxed_out_y
            self.gum_atas_relaxed_out_x = self.marel_sample_id.gum_atas_relaxed_out_x
            self.gum_atas_relaxed_out_y = self.marel_sample_id.gum_atas_relaxed_out_y
            self.gum_bawah_relaxed_out_x = self.marel_sample_id.gum_bawah_relaxed_out_x
            self.gum_bawah_relaxed_out_y = self.marel_sample_id.gum_bawah_relaxed_out_y
            self.leg_gum_tengah_relaxed_out_x = self.marel_sample_id.leg_gum_tengah_relaxed_out_x
            self.leg_gum_tengah_relaxed_out_y = self.marel_sample_id.leg_gum_tengah_relaxed_out_y
        

    @api.depends('manufacturing_order')
    def _compute_product_id(self):
        for record in self:
            record.product_id = record.manufacturing_order.product_id if record.manufacturing_order else False
    
    # @api.multi
    def _update_success_header(self):
        for pengecekan in self:
            pengecekan.success_header = all(line.success for line in pengecekan.pengecekan_sample_line)

    # @api.multi
    def action_approve(self):
        for pengecekan in self:
            pengecekan.success_header = True
            pengecekan.state = 'success'
            pengecekan.tgl_selesai=fields.Datetime.now()

    # @api.multi
    def action_cancel(self):
        for pengecekan in self:
            pengecekan.success_header = False
            pengecekan.state = 'canceled'
            pengecekan.write({'success_header': False})

    # @api.multi
    def action_draft(self):
        for pengecekan in self:
            pengecekan.success_header=False
            pengecekan.state='draft'        

class PengecekanSampleLine(models.Model):    
    _name = 'pengecekan.sample.line'
    _description = 'Pengecekan Sample Line'
    
    pengecekan_sample_id = fields.Many2one('pengecekan.sample', string='Sample Reference', ondelete='cascade', index=True, copy=False)
    tgl_buat = fields.Date(string='Tanggal', default=fields.Date.context_today)
    nama_operator_id = fields.Many2one('hr.employee', string='Inspector')
    no_mesin = fields.Many2one('mesin.marel.produksi', string='No Mesin')
    temuan = fields.Many2one('temuan.option', string='Temuan', required=True)
    keterangan = fields.Char(string='Keterangan')
    tgl_selesai = fields.Datetime(string=u'Tgl Selesai', readonly=True)

    stretch_gum_x = fields.Char(string='Gum X')
    stretch_gum_y = fields.Char(string='Gum Y')

    stretch_leg_x = fields.Char(string='Leg X')
    stretch_leg_y = fields.Char(string='Leg Y')

    stretch_leg_gum_x = fields.Char(string='Leg Gum X')
    stretch_leg_gum_y = fields.Char(string='Leg Gum Y')
    
    stretch_leg_gum_bawah_x = fields.Char(string='Leg Gum Bawah X')
    stretch_leg_gum_bawah_y = fields.Char(string='Leg Gum Bawah Y')

    stretch_foot_x = fields.Char(string='Foot x')
    stretch_foot_y = fields.Char(string='Foot y')

    stretch_foot_gum_x = fields.Char(string='Foot Gum X')
    stretch_foot_gum_y = fields.Char(string='Foot Gum Y')

    @api.depends('temuan', 'keterangan')
    def _compute_quality_test_check(self):
        for line in self:
            line.success = line.temuan and line.keterangan
            if line.success:
                line.pengecekan_sample_id._update_success_header()