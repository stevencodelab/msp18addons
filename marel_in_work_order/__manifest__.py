{
    'name': 'Inherit Mrp Work Order',
    'version': '18.0',
    'author': 'Aditya Demas',
    'license': 'OPL-1',
    'category': 'Inherit Mrp Work Order',
    'summary': 'Inherit Button and Field',
    'description': '''
    ''',
    'depends': [
        'mrp',
        'hr',
        'stock',
        'mrp_workorder'
        ],
    'data': [
        'views/mrp_production_2.xml',
        'views/marel_nama_operatorlist.xml',
        'views/target_produksi.xml',
		"security/ir.model.access.csv",
        # 'views/menu.xml',
        # 'views/ir_sequence.xml',
        # 'report/operator_rijek_kaoskaki_report.xml',
    ],
    'qweb': [
    ],
    # 'css': ['static/src/css/sale.css'],
    'auto_install': False,
    'installable': True,
    'application': True,
}