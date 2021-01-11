# -- coding: utf-8 --
# ************#
# Importación Clientes y Proveedores #
# ************#

import csv
import xmlrpc.client

# SERVIDOR DE DONDE VOY A CARGAR
host = '127.0.0.1'
port = 8069
db = 'db10-chile-sii'
user = 'admin'
password = 'nikje12'
url = 'http://%s:%d/xmlrpc/' % (host, port)
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
    print('Conectado al servidor maestro')

# SERVIDOR PARA DONDE VOY A CARGAR LOS DATOS
# new_host = '127.0.0.1'
new_host = 'arquipunto14.sepo.org'
new_port = 8069
new_db = 'db14-arquipunto'
new_user = 'admin'
new_password = 'Chile2929'
new_url = 'http://%s:%d/xmlrpc/' % (new_host, new_port)

########  INSERTAR EN LOCALHOST #################
# new_host = '127.0.0.1'
# new_port = 8061
# new_db = 'db14_prolase'
# new_user = 'admin'
# new_password = 'x1234567890'
# new_url = 'http://%s:%d/xmlrpc/' % (new_host, new_port)

new_common_proxy = xmlrpc.client.ServerProxy(new_url + 'common')
new_object_proxy = xmlrpc.client.ServerProxy(new_url + 'object')
new_uid = new_common_proxy.login(new_db, new_user, new_password)

if new_uid:
    print('Conectado al servidor esclavo')


def _find_country_id(country_name):
    # print(country_name)
    if country_name[1] == 'Spain':
        country_name[1] = 'España'

    country_id = new_object_proxy.execute(new_db, new_uid, new_password, 'res.country', 'search',
                                          [('name', '=', country_name[1])])
    # print(country_id)
    if country_id:
        return country_id[0]
    else:
        return False


def _find_state_id(state_name):
    # state = state_name[0]
    # #state_name = state[:-5]
    # state_name = state
    old_state_id = object_proxy.execute(db, uid, password, 'res.country.state', 'search_read', [('id', '=', state_name[0])])
    state_id = False
    if old_state_id:
        state_id = new_object_proxy.execute(new_db, new_uid, new_password, 'res.state.province', 'search', [('name', '=', old_state_id[0]['name'])])
    if state_id:
        return state_id[0]
    else:
        return False


def _migrate_partners():
    partner_ids = object_proxy.execute(db, uid, password, 'res.partner', 'search', [('supplier', '=', True),('customer', '=', False),('active', '=', True)])  #
    total_count = len(partner_ids)
    global_count = 0
    print('Nuevos Partners ', total_count)
    partner_ids = sorted(partner_ids)
    if uid:
        errors_count = 0
        errors_ids = []
        for id in partner_ids:
            global_count = global_count + 1
            print('Partner ', global_count, ' De ', total_count, 'Old ID ', id)
            try:
                partner = object_proxy.execute_kw(db, uid, password, 'res.partner', 'read', [id])
                new_partner = new_object_proxy.execute(new_db, new_uid, new_password, 'res.partner', 'search',
                                                       [('comment', '=', id)])
                if not new_partner:
                    vals = {}
                    receivable = object_proxy.execute(db, uid, password, 'account.account', 'search_read',
                                                      [('id', '=', partner[0]['property_account_receivable_id'][0])])
                    code_receivable = new_object_proxy.execute(new_db, new_uid, new_password, 'account.account',
                                                               'search_read', [('code', '=', receivable[0][
                            'code'])]) if receivable else False
                    payable = object_proxy.execute(db, uid, password, 'account.account', 'search_read',
                                                   [('id', '=', partner[0]['property_account_payable_id'][0])])
                    code_payable = new_object_proxy.execute(new_db, new_uid, new_password, 'account.account', 'search_read',
                                                            [('code', '=', payable[0]['code'])]) if payable else False
                    payment_term_supp = new_object_proxy.execute(new_db, new_uid, new_password, 'account.payment.term', 'search',
                                                            [('name', 'ilike', str(partner[0]['property_supplier_payment_term_id'][1]))]) if partner[0]['property_supplier_payment_term_id'] else False
                    payment_term = new_object_proxy.execute(new_db, new_uid, new_password, 'account.payment.term', 'search',
                                                            [('name', 'ilike', str(partner[0]['property_payment_term_id'][1]))]) if partner[0]['property_payment_term_id'] else False
                    partner_activities = False
                    list_activities = []
                    if partner[0]['partner_activities_ids']:
                        for activity in partner[0]['partner_activities_ids']:
                            old_partner_activities = object_proxy.execute(db, uid, password, 'economical.activities', 'search_read',
                                                            [('id', '=', activity)])
                            print('activity old: ', old_partner_activities)
                            if old_partner_activities:
                                partner_activities = new_object_proxy.execute_kw(new_db, new_uid, new_password, 'sii.economic.activities', 'search',
                                                            [[['name', 'ilike', old_partner_activities[0]['name']]]], {'limit': 1})
                                list_activities.append(partner_activities)
                    vals['comment'] = id
                    vals['name'] = partner[0]['name']
                    vals['vat'] = partner[0]['document_number']
                    vals['giro'] = partner[0]['giro']
                    vals['customer_rank'] = partner[0]['customer']
                    vals['supplier_rank'] = partner[0]['supplier']
                    if partner[0]['type'] != 'default':
                        vals['type'] = partner[0]['type']
                    vals['street'] = partner[0]['street']
                    vals['street2'] = partner[0]['street2']
                    vals['zip'] = partner[0]['zip']
                    vals['city'] = partner[0]['city']
                    vals['email'] = partner[0]['email']
                    vals['dte_email'] = partner[0]['dte_email']
                    vals['email_payment'] = partner[0]['dte_payment']
                    vals['phone'] = partner[0]['phone']
                    vals['website'] = partner[0]['website']
                    vals['mobile'] = partner[0]['mobile']
                    vals['birthdate'] = partner[0]['birthdate']
                    vals['ref'] = partner[0]['ref']
                    vals['to_invoice'] = partner[0]['factura']
                    vals['auto_pay_inv'] = partner[0]['auto_pay_inv']
                    vals['property_account_receivable_id'] = code_receivable[0]['id']
                    vals['property_account_payable_id'] = code_payable[0]['id']
                    vals['property_payment_term_id'] = payment_term
                    vals['property_supplier_payment_term_id'] = payment_term_supp
                    vals['property_account_position_id'] = 10 if partner[0]['property_account_position_id'] else False
                    #vals['activities_ids'] = [(6, 0, list_activities)] if list_activities else False
                    if partner[0]['country_id'] != False:
                        vals['country_id'] = _find_country_id(partner[0]['country_id'])
                    if partner[0]['state_id'] != False:
                        vals['province_id'] = _find_state_id(partner[0]['state_id'])
                try:
                    vals['image_1920'] = partner[0]['image']
                except Exception:
                    pass
                if partner[0]['company_id']:
                    tmp = partner[0]['company_id']
                    vals['company_id'] = tmp[0]
                #print(vals)
                new_object_proxy.execute(new_db, new_uid, new_password, 'res.partner', 'create', vals)

            except Exception:
                errors_count = errors_count + 1
                errors_ids.append(id)
                pass
        if errors_count > 0:
            print("Errores ", errors_count)
            print("Ids no importados ", errors_ids)

    else:
        print("No Conectado en Partners")


def main():
    print('Ha comenzado el proceso modelos')
    _migrate_partners()
    print('Ha finalizado el proceso')


main()
