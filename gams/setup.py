import frappe

def after_migrate():
	create_custom_roles(get_gams_roles())

def before_migrate():
	pass

def create_custom_roles(roles):
	for role in roles:
		if not frappe.db.exists("Role", role):
			role_doc = frappe.get_doc({
				"doctype": "Role",
				"role_name": role
			})
			role_doc.insert(ignore_permissions=True)

	frappe.db.commit()

def create_property_setters(property_setter_datas):
	for data in property_setter_datas:
		if frappe.db.exists("Property Setter", data):
			continue

		ps = frappe.new_doc("Property Setter")
		ps.update(data)
		ps.flags.ignore_permissions = True
		ps.insert()

def get_gams_roles():
	return [
		"GAMS Manager"
	]

