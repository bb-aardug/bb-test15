# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################
{
    'name': 'Batch Specification',
    'description': """
    1. Configure Product Field Configuration in inventory menu
    2. Maximum and Minimum value required to fill if required check box
    selected in Product Field Configuration.  
    3. Select batch configuration in product. When we create lot number for 
    that product then batch specification entry is filled
    4. User can view lots from stock picking form view and manufacturing form 
    view through lot smart button 
""",
    'version': '15.0.1.0',
    'category': 'Product',
    'website': "http://www.aardug.nl/",
    'author': "Aardug, Arjan Rosman",
    'images': [],
    'depends': ['product', 'stock', 'mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_view.xml',
        'views/product_field_config_view.xml',
        'views/mrp_production.xml',
        'views/stock_picking_view.xml',
        'views/stock_production_lot_view.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    'qweb': [],
}
