frappe.query_reports["RFQ Status"] = {
	"filters": [
		{
			"fieldname": "rfq",
			"label": __("Request for Quotation"),
			"fieldtype": "Link",
			"options": "Request for Quotation",
			"default": "",
			"get_query": function () {
				return { filters: { "docstatus": ["=", 1] } }
			}
		},
		{
			"fieldname": "supplier",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier",
			"default": "",
			"get_query": function () {
				var rfq = frappe.query_report_filters_by_name.rfq.get_value();
				if (rfq != "") {
					return {
						query: "erpnext.buying.report.rfq_status.rfq_status.supplier_query",
						filters: {
							"from": "Request for Quotation Supplier",
							"parent": rfq
						}
					}
				}
				return {
					filters: {}
				}
			}
		}
	]
}
	
