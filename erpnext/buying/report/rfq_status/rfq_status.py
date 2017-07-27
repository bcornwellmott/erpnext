# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_data(filters):
	if not 'rfq' in filters:
		filters.rfq = ""
	if not 'supplier' in filters:
		filters.supplier = ""

	return frappe.db.sql("""SELECT
			rfq.name as rfq_name,
			rfq_sup.supplier as supplier,
			rfq.transaction_date as transaction_date,
			rfq_sup.quote_status as quote_status
		FROM
			`tabRequest for Quotation` as rfq,
			`tabRequest for Quotation Supplier` as rfq_sup
		WHERE
			rfq.docstatus=1
			AND (rfq.name= %(rfq)s OR %(rfq)s = "")
			AND (rfq_sup.supplier = %(supplier)s OR %(supplier)s = "")
			AND rfq.name = rfq_sup.parent""", filters,as_dict=0)

def get_columns():
	columns = [{
		"fieldname": "rfq_name",
		"label": "Request for Quotation",
		"fieldtype": "Link",
		"options": "Request for Quotation",
		"width": 200
	},{
		"fieldname": "supplier",
		"label": "Supplier",
		"fieldtype": "Link",
		"options": "Supplier",
		"width": 200
	},{
		"fieldname": "transaction_date",
		"label": "Date",
		"fieldtype": "Date",
		"width": 120
	},{
		"fieldname": "quote_status",
		"label": "Quote Status",
		"fieldtype": "Data",
		"width": 200
	}]
	return columns

def supplier_query(doctype, txt, searchfield, start, page_len, filters):
	if filters.get("from"):
		from frappe.desk.reportview import get_match_cond
		filters.update({
			"txt": txt,
			"mcond": get_match_cond(filters["from"]),
			"start": start,
			"page_len": page_len
		})
		return frappe.db.sql("""select supplier from `tab%(from)s`
			where parent='%(parent)s' and docstatus < 2 and supplier like '%%%(txt)s%%' %(mcond)s
			order by supplier limit %(start)s, %(page_len)s""" % filters)