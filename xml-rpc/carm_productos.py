#!/usr/bin/python3
# ************#
# Importación Clientes y Proveedores #
# ************#

import xmlrpc.client
import json
import time
from itertools import chain
import logging

_logger = logging.getLogger('MigracionV14')
logging.basicConfig(filename='/root/reads.log', level=logging.INFO)

# SERVIDOR DE DONDE VOY A CARGAR
host = '127.0.0.1'
port = 8069
db = 'db10-chile'
user = 'admin'
password = 'Azul2020'
url = 'http://%s:%d/xmlrpc/2/' % (host, port)
#######################################################
# TEMPORAL TRABJANDO DESDE SERVER NUEVO PARA LOCAL
#######################################################

#######################################################
# TEMPORAL TRABJANDO DESDE SERVER NUEVO PARA LOCAL
#######################################################

common_proxy = xmlrpc.client.ServerProxy(url + 'common')
object_proxy = xmlrpc.client.ServerProxy(url + 'object')
uid = common_proxy.login(db, user, password)
if uid:
    _logger.info('Conectado al servidor maestro')

# SERVIDOR PARA DONDE VOY A CARGAR LOS DATOS
# new_host = '127.0.0.1'
new_host = 'arquipunto14.demoazul.org'
new_port = 8069
new_db = 'db14-test'
new_user = 'admin'
new_password = 'Red2021'
new_url = 'http://%s:%d/xmlrpc/2/' % (new_host, new_port)

new_common_proxy = xmlrpc.client.ServerProxy(new_url + 'common')
new_object_proxy = xmlrpc.client.ServerProxy(new_url + 'object')
new_uid = new_common_proxy.login(new_db, new_user, new_password)

BATCH_LIMIT = 100  # Definimos cuantos productos crear por batch
COMMON_FIELDS = ['name', 'company_id', 'available_in_pos', 'default_code', 'list_price', 'delivery_price', 'delivery_price_extra', 'sale_ok', 'purchase_ok', 'sale_delay', 'type', 'tracking', 'weight', 'volume', 'active', 'discontinued', 'categ_id', 'pos_categ_id', 'product_brand_id', 'image', 'standard_price', 'website_description', 'attribute_line_ids']
OTHER_FIELDS = ['low_price', 'last_name', 'short_name', 'default_code_last', 'package_cost', 'hs_code', 'disponible_distribuidor', 'disponible_despacho_web', 'pricelist_price', 'website_unsellable', 'min_availability', 'availability_location_ids', 'website_style_ids', 'discount_type', 'discount_amount', 'country_origen', 'product_ancho', 'product_largo', 'product_espesor', 'volume', 'package_ancho', 'package_largo', 'package_espesor', 'package_volume', 'package_fits']

if new_uid:
    _logger.info('Conectado al servidor esclavo')


def map_xml_data(model):
    new_server_ids = {}
    for data in new_object_proxy.execute_kw(new_db, new_uid, new_password, 'ir.model.data', 'search_read', [[('model', '=', model)], ['module', 'name', 'res_id']], {'order': 'id'}):
        new_server_ids['%(module)s.%(name)s' % data] = data['res_id']
    current_ids = {}
    for data in object_proxy.execute_kw(db, uid, password, 'ir.model.data', 'search_read', [[('model', '=', model)], ['module', 'name', 'res_id']], {'order': 'id'}):
        current_ids[data['res_id']] = new_server_ids.get('%(module)s.%(name)s' % data)
    return current_ids


CATEG_IDS = map_xml_data('product.category')
POS_CATEG_IDS = map_xml_data('pos.category')
BRAND_IDS = map_xml_data('product.brand')
ATTR_IDS = map_xml_data('product.attribute')
ATTR_VALS_IDS = map_xml_data('product.attribute.value')


def _find_product_categ_id(category_id):
    return CATEG_IDS.get(category_id[0]) if category_id else False


def _find_pos_categ_id(category_id):
    return POS_CATEG_IDS.get(category_id[0]) if category_id else False


def _find_brand(brand):
    return BRAND_IDS.get(brand[0]) if brand else False


def _find_attr(attr_id):
    return ATTR_IDS.get(attr_id[0]) if attr_id else False


def _find_attr_val(attr_id):
    return ATTR_VALS_IDS.get(attr_id) if attr_id else False


def _migrate_products(offset=0):
    products = object_proxy.execute_kw(db, uid, password, 'product.template', 'search_read', [['|', ('active', '=', True), ('active', '=', False)], COMMON_FIELDS + OTHER_FIELDS], {'limit': BATCH_LIMIT, 'offset': offset, 'order': 'id'})
    next_offset = offset + len(products)
    product_ids = [p['id'] for p in products]

    # Buscamos los XML de los que ya existan
    existing_xmls = object_proxy.execute_kw(db, uid, password, 'ir.model.data', 'search_read', [[('model', '=', 'product.template'), ('res_id', 'in', product_ids)], ['module', 'name', 'res_id']])
    products_xml = {xml['res_id']: '%(module)s.%(name)s' % xml for xml in existing_xmls}

    # Si en el servidor antiguo no tiene un xml_id, se lo creamos
    for product_id in product_ids:
        if product_id in products_xml:
            continue
        xml_values = {
            'name': 'product_template_%d' % product_id,
            'res_id': product_id,
            'model': 'product.template',
            'module': 'arquipunto_v10',
        }
        object_proxy.execute(db, uid, password, 'ir.model.data', 'create', xml_values)
        products_xml.update({xml_values['res_id']: '%(module)s.%(name)s' % xml_values})

    # Según el xml_id, si ya existe en el servidor nuevo, no lo creamos
    new_server_xml_ids = new_object_proxy.execute_kw(new_db, new_uid, new_password, 'ir.model.data', 'search_read', [[
        ('name', 'in', [p.split('.')[1] for p in products_xml.values()]), ('model', '=', 'product.template')], ['module', 'name']])
    products = [product for product in products if products_xml[product['id']] not in ['%(module)s.%(name)s' % new_xmlid for new_xmlid in new_server_xml_ids]]

    # Consultamos en una sola llamada todos los atributos que se deben crear
    attrs_line_ids = list(chain(*[p.pop('attribute_line_ids') for p in products if p['attribute_line_ids']]))
    for attr_map in object_proxy.execute_kw(db, uid, password, 'product.attribute.line', 'read', [attrs_line_ids, ['attribute_id', 'value_ids', 'product_tmpl_id']]):
        attr_map.pop('id')
        product_id = attr_map.pop('product_tmpl_id')[0]
        attr_map['attribute_id'] = _find_attr(attr_map['attribute_id'])
        attr_map['value_ids'] = [_find_attr_val(val) for val in attr_map['value_ids']]
        for product in products:
            if product['id'] == product_id:
                if 'attribute_line_ids' in product:
                    product['attribute_line_ids'].append((0, 0, attr_map))
                else:
                    product['attribute_line_ids'] = [(0, 0, attr_map)]
                break

    total_exe = len(products)
    _logger.info('Productos a migrar %d, offset %d', total_exe, offset)
    if uid:
        new_xmlids_to_create = []
        for i, product in enumerate(products, offset+1):
            pstart = time.time()
            vals = product.copy()
            # Agregando campos aun no creados en 14
            other_fields = {field_name: vals.pop(field_name, False) for field_name in OTHER_FIELDS}
            vals['description'] = json.dumps(other_fields)
            vals['old_id'] = product['id']
            vals['categ_id'] = _find_product_categ_id(product['categ_id'])
            vals['pos_categ_id'] = _find_pos_categ_id(product['pos_categ_id'])
            vals['product_brand_id'] = _find_brand(product['product_brand_id'])
            vals['standard_price'] = product['standard_price']
            vals['website_description'] = product['website_description']
            vals['image_1920'] = vals.pop('image')
            if product['company_id']:
                vals['company_id'] = product['company_id'][0]

            try:
                new_product_id = new_object_proxy.execute(new_db, new_uid, new_password, 'product.template', 'create', vals)
            except Exception as exc:
                _logger.error('Error creando producto %d', product['id'], exc_info=True)
                new_product_id = False
            if new_product_id:
                # Guardamos los valores de los xml_ids que crearemos después en una sola llamada.
                module, name = products_xml[product['id']].split('.')
                new_xmlids_to_create.append({'module': module, 'name': name, 'model': 'product.template', 'res_id': new_product_id})
                # _create_single_product_attribute_lines(product['id'])
            _logger.info('Producto %s de %s\tTiempo: %.3f segundos', i, total_exe + offset, time.time() - pstart)

        # Creamos todos los xml_ids pendientes
        new_object_proxy.execute(new_db, new_uid, new_password, 'ir.model.data', 'create', new_xmlids_to_create)
    else:
        _logger.error("No Conectado en piezas")
    return next_offset


if __name__ == '__main__':
    _logger.info('Ha comenzado el proceso')
    _logger.info('Categorias: %d', len(CATEG_IDS))
    _logger.info('Categorias TPV: %d', len(POS_CATEG_IDS))
    _logger.info('Marcas: %d', len(BRAND_IDS))
    start = time.time()
    this_offset = 0
    while this_offset < 2500:
        last_offset = this_offset
        this_offset = _migrate_products(this_offset)

    _logger.info('Ha finalizado el proceso en %.2f minutos', (time.time() - start) / 60)
