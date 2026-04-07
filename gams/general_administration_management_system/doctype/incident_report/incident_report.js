// Copyright (c) 2026, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on('Incident Report', {
	onload: function(frm) {
		if (!frm.doc.reported_by) {
			frappe.db.get_value('Employee', 
				{ user_id: frappe.session.user }, 
				'name'
			).then(r => {
				if (r.message) {
					frm.set_value('reported_by', r.message.name);
				}
			});
		}
	}
});
