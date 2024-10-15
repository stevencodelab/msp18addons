from odoo import models, fields, api
from datetime import datetime, date
from odoo import http
from odoo.http import content_disposition, request
import io
import xlsxwriter

class ResumeProduksiWo(models.Model):
    _name = 'resume.produksi.wo'
    _description = 'Resume Produksi WO'

    name = fields.Char(string='Report', default='Resume Produksi WO' )
    date_start = fields.Datetime(string="Tanggal Awal", required=True, )
    date_end = fields.Datetime(string="Tanggal Akhir", required=True, )
    report_ids = fields.One2many('close.kiriman.line', 'report_id', string="Headre Report")
    categ_id = fields.Many2many('product.category', string='Produk Kategori')
    workcenter_id = fields.Many2many('mrp.workcenter', 'Work Center',)


    @api.onchange('kategory')
    def _onchange_categ_id(self):
        if self.kategory:
            self.categ_id = self.kategory
    
    
    def generate_report(self):
        sql = """select 
                    mnol.id,
                    mnol.tgl_kerja,
                    mnol.jumlah_reject,
                    mnol.nama_operator,
                    mnol.nama_qiusi,
                    mnol.no_mesin,
                    mnol.no_kkp,
                    mwo.jumlah_yg_selesai,
                    mwo.qty_production,
                    mwo.kekurangan_produksi,
                    mwo.no_mo,
                    mwo.nama_produk,
                    
                from
                    marel_nama_operatorlist mnol
                LEFT JOIN
                    operator_rijek_kaoskaki ork ON (ork.marel_nama_operatorlist_id = mnol.id)
                LEFT JOIN
                    jenis_rijek_kaoskaki jrk ON (ork.jenis_rijek_kaoskaki_id = jrk.id)
                LEFT JOIN
                    mrp_workorder mwo ON (mnol.nama_operator_work_order_id = mwo.id)
                JOIN
                    product_product pp ON (mwo.product_id = pp.id)
                JOIN 
                    product_template pt ON (pp.product_tmpl_id = pt.id)
                where
                    pt.categ_id in %s
                    or workcenter_id in %s
                    and mnol.tgl_kerja between %s and %s
                """
        # qc = """Select pc.id 
        # form product_category pc
        # where pc.id in (%s)
        #     """
        # import pdb; pdb.set_trace()
        cr = self.env.cr

        cr.execute(sql,(self.date_start,self.date_end,))
        result = cr.fetchall()

        sql = 'delete from resume_produksi_wo_line where report_id=%s'
        cr.execute(sql, (self.id,))

        for res in result:
            lis = self.env['resume.produksi.wo.line']
            lis.create({
                #isi field2 yang di line tapi disesuaikan dengan tabel atau querimya
                'report_id' : self.id,
                'nama_produk': res[9],
                'produk_id': res[8],
                'qty': res[10],
                'uom': res[11],
                'nw': res[12],
                'so': res[6],
                'reference':res[7],
                'date_done':res[1],
                'date_kirim':res[2],
                'contak':res[3],
                'dest_loc_id':res[5],
                'source_loc_id':res[4],
                           })
    



class ResumeProduksiWoLine(models.Model):
    _name = 'resume.produksi.wo.line'
    _description = 'Resume Produksi WO Line'

# marel.nama.operatorlist
    report_id = fields.Many2one('resume.produksi.wo', string="Report Line")
    tgl_kerja = fields.Date(string=u'tgl Kerja',default=fields.Date.context_today,)
    jumlah_reject = fields.Integer( string='Jumlah Rijek',)
    nama_operator = fields.Char(string=u'Nama Operator',)
    nama_qiusi = fields.Char(string=u'Nama qiusi',)
    no_mesin = fields.Char(string=u'No Mesin',)
    no_kkp = fields.Char(string=u'No KKP',)

# mrp.workorder
    jumlah_yg_selesai = fields.Integer(string=u'Qty Yg Selesai',)
    qty_production = fields.Integer(string=u'Total Orderan',)
    kekurangan_produksi = fields.Integer(string=u'Kekurangan Qty',)
    no_mo = fields.Char(string='MO',)
    nama_produk = fields.Char(string='Nama Produk')

    # date_done = fields.Datetime(string="Date Of Transfer")
    # date_kirim = fields.Datetime(string="Tgl Kirim")
    # contak = fields.Char(string="Contak")
    # dest_loc_id = fields.Char(string="Destination Location")
    # source_loc_id = fields.Char(string="Source Location")
    # reference = fields.Char(string="WH/OUT")
    # produk_id = fields.Integer(string="ID Produk")
    # qty = fields.Float(string="Jumlah/ m",)
    # uom = fields.Char(string="Satuan")
    # nw = fields.Float(string="Berat/Kg")
    # mo = fields.Char(string="Mo/Kp")
    # so = fields.Char(string="SO")
    # state = fields.Selection([
    #                              ('done','Stock'),
    #                              ('assigned','Acc'),
    #                              ('confirmed','Konfrim')],string="Posisi",copy= False, store=True,)