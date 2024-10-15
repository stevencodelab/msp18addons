from flectra import models, fields, api, _
from flectra.exceptions import UserError, ValidationError
from flectra.addons import decimal_precision as dp

class MrpRoutingRijek(models.Model):
    _name = 'mrp.routing.rijek'
    _description = u'MRP Rputing Rijek'
    # _rec_name = 'primary_id'
    

    def _default_msp_reouting_rijek(self):
        return self.env['mrp.workorder'].browse(self._context.get('active_ids'))

    workorder_id = fields.Many2one('mrp.workorder',string="Work Order Id",default=_default_msp_reouting_rijek, readonly=True,)
    

    def get_mrp_routing_rijek(self):
        nama_baru = self.env['ir.sequence'].next_by_code('mrp.routing.rijek.no')
        return nama_baru

    name = fields.Char(string='Id', required=True,copy=False, default=get_mrp_routing_rijek, readonly=True )
    tgl_create = fields.Datetime(string='Tanggal', default=fields.Datetime.now, readonly=True,)
    mrp_productioin_id = fields.Many2one(string=u'No MO', related='name.production_id', readonly=True,)

    gread_d = fields.Integer(string="Gread D",)
    # new rijek
    putus_benang = fields.Integer(string=u'PTS BENANG',)
    bolong = fields.Integer(string=u' BOLONG / SOBEK',)
    vanise = fields.Integer(string=u' VANISE',)
    singker = fields.Integer(string=u' SINGKER/ LIDAH SERET',)
    kotor = fields.Integer(string=u' KOTOR',)
    terry = fields.Integer(string=u' TERRY',)
    jumpstich = fields.Integer(string=u' JUMPSTICH',)
    renggang = fields.Integer(string=u' RENGGANG',)
    tidak_loading = fields.Integer(string=u' TIDAK LOADING',)
    belang = fields.Integer(string=u' BELANG',)
    ukuran = fields.Integer(string=u' UKURAN',)

    lingtu = fields.Integer(string=u' LINGTU',)
    pecah = fields.Integer(string=u' PECAH',)
    loncat = fields.Integer(string=u' LONCAT',)
    transfer = fields.Integer(string=u' TRANSFER NYANGKOL',)
    gumpal = fields.Integer(string=u' GUMPAL',)
    kasar = fields.Integer(string=u' KASAR',)
    benang_gabung = fields.Integer(string=u' BENANG GABUNG',)
    bintik_bintik = fields.Integer(string=u' BINTIK BINTIK',)
    jarum = fields.Integer(string=u'Jarum',)
    transfer_jebol = fields.Integer(string=u' TRANSFER Jebol',)
    partner_id = fields.Many2one('res.partner', string='Customer', )
    # jam_kerja_buat_rijek = fields.Float(string=u'JAM KERJA', default=480.0,readonly = True,)
