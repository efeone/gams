// Copyright (c) 2026, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on('Communication Log', {
    onload: function(frm) {
        set_logged_in_employee(frm);
    }
});

/*
 * Populate the "Logged By" field with the Employee linked to the current session user.
*/
function set_logged_in_employee(frm) {
    if (!frm.doc.logged_by) {
        frappe.db.get_value('Employee', {
            user_id: frappe.session.user
        }, 'name').then(r => {
            if (r.message && r.message.name) {
                frm.set_value('logged_by', r.message.name);
            }
        });
    }
}
