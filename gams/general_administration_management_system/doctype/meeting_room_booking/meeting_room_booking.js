// Copyright (c) 2026, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on('Meeting Room Booking', {
    onload: function(frm) {
        set_meeting_room_filter(frm);
        set_logged_in_employee(frm);
    }
});

/**
 * Ensures only rooms with status = "Active"
 * are available for selection
 */
function set_meeting_room_filter(frm) {
    frm.set_query('meeting_room', function() {
        return {
            filters: {
                status: 'Active'
            }
        };
    });
}

/*
 * Populate the "booked_by" field with the Employee linked to the current session user.
*/
function set_logged_in_employee(frm) {
    if (!frm.doc.booked_by) {

        // Get current logged-in user
        const user = frappe.session.user;

        if (!user) {
            console.log("Session user not found");
            return;
        }

        // Fetch Employee linked to user
        frappe.db.get_value('Employee', {
            user_id: user
        }, 'name').then(r => {
            if (r.message && r.message.name) {
                frm.set_value('booked_by', r.message.name);
            } else {
                frappe.msgprint("No Employee linked to this user");
            }
        });
    }
}
