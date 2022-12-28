##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2018 Marlon Falcon Hernandez
#    (<http://www.marlonfalcon.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Sale Advance Permissions MFH',
    'version': '16.0.1.0.0',
    'author': 'Marlon Falcon Hernandez',
    'maintainer': 'Marlon Falcon Hernandez',
    'website': 'http://www.marlonfalcon.com',
    'license': 'AGPL-3',
    'category': 'Sale',
    'summary': 'Sale Advance Permissions.',
    'depends': ['sale_management'],
    'data': [
              'security/security.xml',
              'views/sale_order_view.xml',
              'views/product_view.xml',
            ],
    'images': ['static/description/banner.jpg'],
}
