# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Lot Number Barcode',
    'version': '15.0.1.0',
    'summary': 'Print Lot Number barcode',
    'description': '''
       Print Barcode for Lot Number
    ''',
    'category': 'Stock',
    'author': "Aardug, Arjan Rosman",
    'website': "http://www.aardug.nl/",
    'depends': ['product_expiry', 'stock', 'purchase', 'batch_specification'],
    'data': [
        'views/product_view.xml',
        'report/report_lot_barcode_small.xml',
        'data/barcode_report.xml',
        'report/lot_barcode_report_view.xml',
        'report/report_lot_barcode_big_extend.xml',
    ],
    'web.report_assets_common': [
        'lot_barcode/static/src/css/lot_report.css',
    ],
    'installable': True,
    'license': 'LGPL-3',

}
