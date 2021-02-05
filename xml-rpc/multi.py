# -- coding: utf-8 --
# ************#
# Importación Clientes y Proveedores #
# ************#
from xlrd import open_workbook
# import xmlrpclib
import xlrd
import csv
import xmlrpc.client

# new_url = 'http://%s:%d/xmlrpc/' % (new_host, new_port)

########  INSERTAR EN LOCALHOST #################
# new_host = '127.0.0.1'
# new_port = 8061
# new_db = 'db14_odoo'
# new_user = 'admin'
# new_password = 'love'
# new_url = 'http://%s:%d/xmlrpc/' % (new_host, new_port)

new_common_proxy = xmlrpc.client.ServerProxy(new_url + 'common')
new_object_proxy = xmlrpc.client.ServerProxy(new_url + 'object')
new_uid = new_common_proxy.login(new_db, new_user, new_password)

if new_uid:
	print('Conectado al servidor esclavo')


def _find_country_id(country_name):
	#print(country_name)
	if country_name[1] == 'Spain':
		country_name[1] = 'España'

	country_id = new_object_proxy.execute(new_db, new_uid, new_password, 'res.country', 'search', [('name', '=', country_name[1])])
	#print(country_id)
	if country_id:
		return country_id[0]
	else:
		return False

def _find_state_id(state_name):
	state_name = str(state_name)
	n_len = len(state_name)
	pos = 1
	name = state_name[0].upper()
	while pos < n_len:
		name += state_name[pos].lower()
		pos += 1
	state_id = new_object_proxy.execute(new_db, new_uid, new_password, 'res.country.state', 'search', [('name', '=', name)])
	if state_id:
		return state_id[0]
	else:
		return False


def _find_payment_term_id(term):
	term2 = term.split('.')
	if len(term2) > 0:
		term = term2[0]
	term_id = new_object_proxy.execute(new_db, new_uid, new_password, 'account.payment.term', 'search', [('extra_code', '=', term)])
	if term_id:
		term_id = sorted(term_id)
		return term_id[0]
	else:
		return False


def _find_periodicity(name):
	name2 = name.split('.')
	if len(name2) > 0:
		name = name2[0]
	if name != '0':
		periodicity_id = new_object_proxy.execute(new_db, new_uid, new_password, 'periodicity', 'search',
										  [('name', '=', name)])
	else:
		return False
	if periodicity_id:
		return periodicity_id[0]
	else:
		periodicity_id = new_object_proxy.execute(new_db, new_uid, new_password, 'periodicity', 'create', {'name': name})
		return periodicity_id

def _find_payment_days(day1, day2):
	days = []
	day_tmp = day1.split('.')
	if len(day1) > 0:
		day_tmp = day_tmp[0]
	if day_tmp != '0':
		day = new_object_proxy.execute(new_db, new_uid, new_password, 'payment.days', 'search',
										  [('day', '=', day_tmp)])
		if day:
			days.append(day[0])
	day_tmp = day2.split('.')
	if len(day2) > 0:
		day_tmp = day_tmp[0]
	if day_tmp != '0':
		day = new_object_proxy.execute(new_db, new_uid, new_password, 'payment.days', 'search',
									   [('day', '=', day_tmp)])
		if day:
			days.append(day[0])
	return days

def _create_dict_partner(val, cust_code):
	vals = {'name': val['NOMBRE FISCAL'],
			'ref': cust_code,
			}
	return vals

def _create_dict_customer(val, cust_code):
	street = ''
	if val['NOMBRE DE DIRECCIÓN'] != 0.0:
		street = val['NOMBRE DE DIRECCIÓN']
	if val['NÚMERO DE DIRECCIÓN'] != 0.0:
		tmp = str(val['NÚMERO DE DIRECCIÓN']).split('.')
		if len(tmp) > 0:
			street = str(street) + ' #' + str(tmp[0])
	vals = {
			'name': val['NOMBRE FISCAL'],
			'comercial_name': val['NOMBRE_COMERCIAL'],
			'vat': val['NIF'],
			'periodicity_id': _find_periodicity(str(val['PERIODO_FACTURACION'])),
			'property_payment_term_id': _find_payment_term_id(str(val['CODIGO FORMA DE PAGO'])),
			'sale_payment_days': _find_payment_days(str(val['PRIMER DÍA DE PAGO']), str(val['SEGUNDO DÍA DE PAGO'])),
			'email': val['E-MAIL'] if val['E-MAIL'] != 0.0 else '',
			'zip': str(val['CODIGO_POSTAL']).split('.')[0] if val['CODIGO_POSTAL'] != 0.0 else '',
			'phone': str(val['TELÉFONO 1']).split('.')[0] if val['TELÉFONO 1'] != 0.0 else '',
			'mobile': str(val['TELÉFONO 2']).split('.')[0] if val['TELÉFONO 2'] != 0.0 else '',
			 'fax': str(val['TELEFAX']).split('.')[0] if val['TELEFAX'] != 0.0 else '',
			 'website': val['WEB'] if val['WEB'] != 0.0 else '',
			 'street': street,
			 'customer_code_pro': cust_code,
			 'customer': True,
			 'customer_rank': True,
			 'city': str(val['TIT_LOCALIDAD'])
			}
	return vals

def _create_dict_supplier(val,cust_code):
	street = ''
	if val['NOMBRE DE DIRECCIÓN'] != 0.0:
		street = val['NOMBRE DE DIRECCIÓN']
	if val['NÚMERO DE DIRECCIÓN'] != 0.0:
		tmp = str(val['NÚMERO DE DIRECCIÓN']).split('.')
		if len(tmp) > 0:
			street = str(street) + ' #' + str(tmp[0])
	vals = {'name': val['NOMBRE FISCAL'],
			'comercial_name': val['NOMBRE_COMERCIAL'],
			'vat': val['NIF'],
			'periodicity_id': _find_periodicity(str(val['PERIODO_FACTURACION'])),
			'property_supplier_payment_term_id': _find_payment_term_id(str(val['CODIGO FORMA DE PAGO'])),
			'purchase_payment_days': _find_payment_days(str(val['PRIMER DÍA DE PAGO']),
														str(val['SEGUNDO DÍA DE PAGO'])),
			'email': val['E-MAIL'] if val['E-MAIL'] != 0.0 else '',
			'zip': str(val['CODIGO_POSTAL']).split('.')[0] if val['CODIGO_POSTAL'] != 0.0 else '',
			'phone': str(val['TELÉFONO 1']).split('.')[0] if val['TELÉFONO 1'] != 0.0 else '',
			'mobile': str(val['TELÉFONO 2']).split('.')[0] if val['TELÉFONO 2'] != 0.0 else '',
			'fax': str(val['TELEFAX']).split('.')[0] if val['TELEFAX'] != 0.0 else '',
			'website': val['WEB'] if val['WEB'] != 0.0 else '',
			'street': street,
			'city': str(val['TIT_LOCALIDAD']),
			'supplier': True,
			'supplier_rank': True,
			'supplier_code_pro': cust_code,
			}
	return vals

def _create_dict_creditor(val, cust_code):
	street = ''
	if val['NOMBRE DE DIRECCIÓN'] != 0.0:
		street = val['NOMBRE DE DIRECCIÓN']
	if val['NÚMERO DE DIRECCIÓN'] != 0.0:
		tmp = str(val['NÚMERO DE DIRECCIÓN']).split('.')
		if len(tmp) > 0:
			street = str(street) + ' #' + str(tmp[0])
	vals = {'name': val['NOMBRE FISCAL'],
			'comercial_name': val['NOMBRE_COMERCIAL'],
			'vat': val['NIF'],
			'periodicity_id': _find_periodicity(str(val['PERIODO_FACTURACION'])),
			'property_supplier_payment_term_id': _find_payment_term_id(str(val['CODIGO FORMA DE PAGO'])),
			'purchase_payment_days': _find_payment_days(str(val['PRIMER DÍA DE PAGO']),
														str(val['SEGUNDO DÍA DE PAGO'])),
			'email': val['E-MAIL'] if val['E-MAIL'] != 0.0 else '',
			'zip': str(val['CODIGO_POSTAL']).split('.')[0] if val['CODIGO_POSTAL'] != 0.0 else '',
			'phone': str(val['TELÉFONO 1']).split('.')[0] if val['TELÉFONO 1'] != 0.0 else '',
			'mobile': str(val['TELÉFONO 2']).split('.')[0] if val['TELÉFONO 2'] != 0.0 else '',
			'fax': str(val['TELEFAX']).split('.')[0] if val['TELEFAX'] != 0.0 else '',
			'website': val['WEB'] if val['WEB'] != 0.0 else '',
			'street': street,
			'city': str(val['TIT_LOCALIDAD']),
			'creditor': True,
			'supplier_rank': True,
			'creditor_code_pro': cust_code,
			}
	return vals

def update_partner_from_excel(companies):
	workbook = xlrd.open_workbook('prolase.xlsx')
	worksheet = workbook.sheet_by_index(0)
	first_row = []

	for col in range(worksheet.ncols):
		first_row.append(worksheet.cell_value(0, col))
	print('Documento leido')
	for count, row in enumerate(range(1, worksheet.nrows), 2):
		val = {}
		for col in range(worksheet.ncols):
			val[first_row[col]] = worksheet.cell_value(row, col)
		msg = ''
		if val['Partner'] == 'Cliente' and int(val['COD. CLIENTE']) > 0:
			if val['ID'] != '':
				cust_code = str(val['COD. CLIENTE']).split('.')
				if len(cust_code) > 1:
					cust_code = cust_code[0]
				else:
					cust_code = str(val['COD. CLIENTE'])
				client_id = str(val['ID']).split('.')
				if len(client_id) > 1:
					client_id = client_id[0]
				else:
					client_id = str(val['ID'])
				partner_id = new_object_proxy.execute(new_db, new_uid, new_password, 'res.partner', 'search',
														   [('id', '=', client_id)])
				if partner_id:
					vals = _create_dict_customer(val, cust_code)
					for company_id in companies:
						new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.users', 'write',
													[new_uid, {'company_id': company_id}])
						try:
							new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.partner', 'write',[partner_id[0], vals])
						except Exception as exp:
							if 'res.partner' in str(exp):
								print(exp)
							pass
					print("Actualizado partner ",partner_id[0])

		# CODIGOS DE PROVEEDOR
		if val['Partner'] == 'Proveedor' and int(val['COD. CLIENTE']) > 0:
			if val['ID'] != '':
				cust_code = str(val['COD. CLIENTE']).split('.')
				if len(cust_code) > 1:
					cust_code = cust_code[0]
				else:
					cust_code = str(val['COD. CLIENTE'])
				client_id = str(val['ID']).split('.')
				if len(client_id) > 1:
					client_id = client_id[0]
				else:
					client_id = str(val['ID'])
				partner_id = new_object_proxy.execute(new_db, new_uid, new_password, 'res.partner', 'search',
													  [('id', '=', client_id)])
				if partner_id:
					vals = _create_dict_supplier(val, cust_code)
					for company_id in companies:
						new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.users', 'write',
													[new_uid, {'company_id': company_id}])
						try:
							new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.partner', 'write',[partner_id[0], vals])
						except Exception as exp:
							if 'res.partner' in str(exp):
								print(exp)
						pass
					print("Actualizado partner",partner_id[0])

		# CODIGO PARA ACCREDORES
		if val['Partner'] == 'acreedor' and int(val['COD. CLIENTE']) > 0:
			if val['ID'] != '':
				cust_code = str(val['COD. CLIENTE']).split('.')
				if len(cust_code) > 1:
					cust_code = cust_code[0]
				else:
					cust_code = str(val['COD. CLIENTE'])
				client_id = str(val['ID']).split('.')
				if len(client_id) > 1:
					client_id = client_id[0]
				else:
					client_id = str(val['ID'])
				partner_id = new_object_proxy.execute(new_db, new_uid, new_password, 'res.partner', 'search',
													  [('id', '=', client_id)])
				if partner_id:
					vals = _create_dict_creditor(val, cust_code)
					for company_id in companies:
						new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.users', 'write',
													[new_uid, {'company_id': company_id}])
						try:
							new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.partner', 'write',[partner_id[0], vals])
						except Exception as exp:
							if 'res.partner' in str(exp):
								print(exp)
							pass
					print("Actualizado partner",partner_id[0])

def create_partner_from(companies):
	workbook = xlrd.open_workbook('prolase2.xlsx')
	worksheet = workbook.sheet_by_index(0)
	first_row = []
	for col in range(worksheet.ncols):
		first_row.append(worksheet.cell_value(0, col))

	for count, row in enumerate(range(1, worksheet.nrows), 2):
		val = {}
		for col in range(worksheet.ncols):
			val[first_row[col]] = worksheet.cell_value(row, col)
		if val['Partner'] == 'Cliente' and int(val['COD. CLIENTE']) > 0:
			if val['ID'] != '':
				cust_code = str(val['COD. CLIENTE']).split('.')
				if len(cust_code) > 1:
					cust_code = cust_code[0]
				else:
					cust_code = str(val['COD. CLIENTE'])
				client_id = str(val['ID']).split('.')
				if len(client_id) > 1:
					client_id = client_id[0]
				else:
					client_id = str(val['ID'])
				partner_id = new_object_proxy.execute(new_db, new_uid, new_password, 'res.partner', 'search',
														   [('id', '=', client_id)])
				if not partner_id:
					vals = _create_dict_partner(val, cust_code)
					new_partner = new_object_proxy.execute(new_db, new_uid, new_password, 'res.partner', 'create', vals)
					vals = _create_dict_customer(val, cust_code)
					for company_id in companies:
						new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.users', 'write',
													[new_uid, {'company_id': company_id}])
						try:
							new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.partner', 'write',
														[new_partner, vals])
						except:
							pass
						if new_partner:
							print("Creando cliente con id ", new_partner)
			else:
				cust_code = str(val['COD. CLIENTE']).split('.')
				if len(cust_code) > 1:
					cust_code = cust_code[0]
				else:
					cust_code = str(val['COD. CLIENTE'])
				vals = _create_dict_partner(val, cust_code)
				new_partner = new_object_proxy.execute(new_db, new_uid, new_password, 'res.partner', 'create', vals)
				vals = _create_dict_customer(val, cust_code)
				for company_id in companies:
					new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.users', 'write',
												[new_uid, {'company_id': company_id}])
					try:
						new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.partner', 'write',
													[new_partner, vals])
					except:
						pass
				if new_partner:
					print("Creando cliente con id ", new_partner)

		# CODIGOS DE PROVEEDOR
		if val['Partner'] == 'Proveedor' and int(val['COD. CLIENTE']) > 0:
			if val['ID'] != '':
				cust_code = str(val['COD. CLIENTE']).split('.')
				if len(cust_code) > 1:
					cust_code = cust_code[0]
				else:
					cust_code = str(val['COD. CLIENTE'])
				client_id = str(val['ID']).split('.')
				if len(client_id) > 1:
					client_id = client_id[0]
				else:
					client_id = str(val['ID'])
				partner_id = new_object_proxy.execute(new_db, new_uid, new_password, 'res.partner', 'search',
													  [('id', '=', client_id)])
				if not partner_id:
					vals = _create_dict_partner(val, cust_code)
					new_partner = new_object_proxy.execute(new_db, new_uid, new_password, 'res.partner', 'create', vals)
					vals = _create_dict_supplier(val, cust_code)
					for company_id in companies:
						new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.users', 'write',
													[new_uid, {'company_id': company_id}])
						try:
							new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.partner', 'write',
														[new_partner, vals])
						except:
							pass
					if new_partner:
						print("Creando proveedor con id ", new_partner)
			else:
				cust_code = str(val['COD. CLIENTE']).split('.')
				if len(cust_code) > 1:
					cust_code = cust_code[0]
				else:
					cust_code = str(val['COD. CLIENTE'])
				vals = _create_dict_partner(val, cust_code)
				new_partner = new_object_proxy.execute(new_db, new_uid, new_password, 'res.partner', 'create', vals)
				vals = _create_dict_supplier(val, cust_code)
				for company_id in companies:
					new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.users', 'write',
												[new_uid, {'company_id': company_id}])
					try:
						new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.partner', 'write',
													[new_partner, vals])
					except:
						pass
				if new_partner:
					print("Creando proveedor con id ", new_partner)

		# CODIGO PARA ACCREDORES
		if val['Partner'] == 'acreedor' and int(val['COD. CLIENTE']) > 0:
			if val['ID'] != '':
				cust_code = str(val['COD. CLIENTE']).split('.')
				if len(cust_code) > 1:
					cust_code = cust_code[0]
				else:
					cust_code = str(val['COD. CLIENTE'])
				client_id = str(val['ID']).split('.')
				if len(client_id) > 1:
					client_id = client_id[0]
				else:
					client_id = str(val['ID'])
				partner_id = new_object_proxy.execute(new_db, new_uid, new_password, 'res.partner', 'search',
													  [('id', '=', client_id)])
				if not partner_id:
					vals = _create_dict_partner(val, cust_code)
					new_partner = new_object_proxy.execute(new_db, new_uid, new_password, 'res.partner', 'create', vals)
					vals = _create_dict_creditor(val, cust_code)
					for company_id in companies:
						new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.users', 'write',
													[new_uid, {'company_id': company_id}])
						try:
							new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.partner', 'write',
														[new_partner, vals])
						except:
							pass
					if new_partner:
						print("Creando acreedor con id ", new_partner)
			else:
				cust_code = str(val['COD. CLIENTE']).split('.')
				if len(cust_code) > 1:
					cust_code = cust_code[0]
				else:
					cust_code = str(val['COD. CLIENTE'])
				vals = _create_dict_partner(val, cust_code)
				new_partner = new_object_proxy.execute(new_db, new_uid, new_password, 'res.partner', 'create', vals)
				vals = _create_dict_creditor(val, cust_code)
				for company_id in companies:
					new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.users', 'write',
												[new_uid, {'company_id': company_id}])
					try:
						new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.partner', 'write',
													[new_partner, vals])
					except:
						pass
				if new_partner:
					print("Creando acreedor con id ", new_partner)

def unmark_secondary_contacts_as_cust_supp_cred():
	all_partners = new_object_proxy.execute(new_db, new_uid, new_password, 'res.partner', 'search',[('parent_id','!=',False)])
	count = 0
	total_count = len(all_partners)
	print("A borrar ",str(total_count))
	for partner in all_partners:
		count += 1
		print("A borrar ", str(count), " valores de " + str(total_count))
		try:
			new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.partner', 'write',
										[partner, {'customer': False, 'property_payment_term_id': False,
												   'supplier': False, 'property_supplier_payment_term_id': False,
												   'creditor': False, 'property_account_creditor_id': False,
												   'customer_rank': False,
												   'supplier_rank': False,
												   'customer_code_pro': 0,
												   'supplier_code_pro':0,
												   'creditor_code_pro': 0
												   }])
		except:
			pass

def delete_contacts(last_id):
	all_partners = new_object_proxy.execute(new_db, new_uid, new_password, 'res.partner', 'search',[('parent_id','!=',False),('id','>',last_id)])
	count = 0
	total_count = len(all_partners)
	print("A borrar ",str(total_count))
	for partner in all_partners:
		count += 1
		print("A borrar ", str(count), " valores de " + str(total_count))
		try:
			new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.partner', 'unlink',
										[partner])
		except:
			pass

def _create_dict_contact(val):
	zip = ''
	if val['CODIGO_POSTAL'] != 0.0:
		if len(str(val['CODIGO_POSTAL'])) < 7:
			zip = '0'+str(val['CODIGO_POSTAL'])
		else:
			zip = str(val['CODIGO_POSTAL'])
		zip = zip.split('.')[0]

	if val['TIPOS de DIRECCIONES'] == 'Dirección Envío' or val['TIPOS de DIRECCIONES'] == 'Dirección ENVÍO POR DEFECTO' :
		type = 'delivery'
	elif val['TIPOS de DIRECCIONES'] == 'Dirección CORRESPONDENCIA':
		type = 'invoice'
	else:
		type = 'contact'

	vals = {'name': val['NOMBRE_R_SOCIAL'],
			'email': val['EMAIL'] if val['EMAIL'] != 0.0 else '',
			'zip': zip,
			'type': type,
			'phone': str(val['DIR_TELEFONO01']).split('.')[0] if val['DIR_TELEFONO01'] != 0.0 else '',
			'mobile': str(val['DIR_TELEFONO02']).split('.')[0] if val['DIR_TELEFONO02'] != 0.0 else '',
			'website': val['WEB'] if val['WEB'] != 0.0 else '',
			'city': val['LOCALIDAD'] if val['LOCALIDAD'] != 0.0 else '',
			'street': str(val['DIR_COMPLETA_N']),
			'state_id': _find_state_id(val['PROVINCIA']),
			'country_id': 68,
			}
	return vals


def update_partner_contacts_from_excel():
	workbook = xlrd.open_workbook('contacts.xls')
	worksheet = workbook.sheet_by_index(0)
	first_row = []
	for col in range(worksheet.ncols):
		first_row.append(worksheet.cell_value(0, col))
	print('Documento leido')
	count = 1
	created = 0
	updated = 0
	for count, row in enumerate(range(1, worksheet.nrows), 2):
		print('Document Fila',count)
		count += 1
		val = {}
		for col in range(worksheet.ncols):
			val[first_row[col]] = worksheet.cell_value(row, col)
		# AQUI PROCESAMOS LOS REGISTROS QUE VIENEN CON ID

		if val['ID'] != '':
			client_id = str(val['ID']).replace("'","")
			client_id = client_id.replace(" ","")
			client_id = client_id.replace("º","")
			client_id = client_id.split('.')
			client_id = client_id[0]
			partner_id = False
			if client_id != ' ' and client_id != '':
				partner_id = new_object_proxy.execute(new_db, new_uid, new_password, 'res.partner', 'search',
													   [('id', '=', client_id)])
			if partner_id:
				vals = _create_dict_contact(val)
				try:
					new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.partner', 'write',[partner_id[0], vals])

				except Exception as exp:
					if 'res.partner' in str(exp):
						print(exp)
					pass
				try:
					if val['TIPOS de DIRECCIONES'] == 'Dirección ENVÍO POR DEFECTO':
						partner = new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.partner', 'read', [partner_id])
						parent_id = partner[0]['parent_id']
						if len(parent_id) > 1:
							parent_id = parent_id[0]
							partner_partner = new_object_proxy.execute(new_db, new_uid, new_password, 'res.partner', 'search', [('id', '=', parent_id)])
							new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.partner', 'write',
														[partner_partner[0],{'address_shipping_default': partner[0]['id']}])
				except Exception as exp:
						if 'res.partner' in str(exp):
							print(exp)
						pass
				try:
					if val['TIPOS de DIRECCIONES'] == 'Dirección CORRESPONDENCIA':
						partner = new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.partner', 'read', [partner_id])
						parent_id = partner[0]['parent_id']
						if len(parent_id) > 1:
							parent_id = parent_id[0]
							partner_partner = new_object_proxy.execute(new_db, new_uid, new_password, 'res.partner', 'search', [('id', '=', parent_id)])
							new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.partner', 'write',
														[partner_partner[0],{'correspondence_address': partner[0]['id']}])
				except Exception as exp:
						if 'res.partner' in str(exp):
							print(exp)
						pass
				print("Actualizado partner ",partner_id[0])
				updated += 1

		else:
			client_id = str(val['CLIENTE']).split('.')[0]
			parent_id = new_object_proxy.execute(new_db, new_uid, new_password, 'res.partner', 'search',
												  [('customer_code_pro', '=', client_id)])
			if parent_id:
				vals = _create_dict_contact(val)
				vals.update({'parent_id': parent_id[0]})
				try:
					new_contact = new_object_proxy.execute(new_db, new_uid, new_password, 'res.partner', 'create', vals)
					print('Creado contact ',new_contact)
				except Exception as exp:
					if 'res.partner' in str(exp):
						print(exp)
					pass
				try:
					if val['TIPOS de DIRECCIONES'] == 'Dirección ENVÍO POR DEFECTO':
						new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.partner', 'write',
														[parent_id,
														 {'address_shipping_default': new_contact}])
				except Exception as exp:
					if 'res.partner' in str(exp):
						print(exp)
					pass
				try:
					if val['TIPOS de DIRECCIONES'] == 'Dirección CORRESPONDENCIA':
						new_object_proxy.execute_kw(new_db, new_uid, new_password, 'res.partner', 'write',
												   [parent_id,{'correspondence_address': new_contact}])
				except Exception as exp:
					if 'res.partner' in str(exp):
						print(exp)
					pass
				created +=1
	print("Parter actualizados ", updated)
	print("Parter creados ", created)


def main():
	print('Ha comenzado el proceso modelos')
	#_migrate_partner_categories(True)
	#_migrate_partner_companies(True)
	#_migrate_partners(True)
	#_migrate_banks(True)
	#_migrate_partner_account_banks(True)
	#_migrate_payment_terms(True)
	#_update_partner_payment_term(True)
	#_update_partner_from_csv(True)
	#_migrate_portal_user(True)
	#_migrate_internal_user(True)
	#_migrate_machine_vending(True)
	#_migrate_locations(True)
	#_update_machine_vending_id(True)
	# _update_account_partners()
	# update_pricelist_partner()
	# update_partner_from_excel([1,2])
	# unmark_secondary_contacts_as_cust_supp_cred()
	# delete_contacts(6258)
	# update_partner_contacts_from_excel()
	print('Ha finalizado el proceso')
main()
