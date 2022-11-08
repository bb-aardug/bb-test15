# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Merge MO For Same Product',
    'summary': "Merge MO",
    'description': """
        1. merge MO of same product.
        2. restrict creating extra picking after MO done
    """,
    'author': 'Aardug, Arjan Rosman',
    'website': 'arosman@aardug.nl',
    'category': 'Product',
    'version': '15.0.1.0',
    'depends': ['mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/merge_mo.xml'
        ],
    'license': 'LGPL-3',
    'installable': True,
}
