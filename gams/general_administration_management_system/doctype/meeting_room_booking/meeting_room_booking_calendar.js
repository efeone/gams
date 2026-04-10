frappe.views.calendar["Meeting Room Booking"] = {

    field_map: {
        start: "start",
        end: "end",
        id: "name",
        title: "title",
        status: "status"
    },

    style_map: {
        "Pending": "warning",
        "Approved": "success",
        "Rejected": "danger",
        "Cancelled": "secondary"
    },

    filters: [
        {
            fieldtype: "Link",
            fieldname: "meeting_room",
            options: "Room",
            label: "Room"
        }
    ],


    get_events_method: "gams.general_administration_management_system.doctype.meeting_room_booking.meeting_room_booking.get_meeting_room_events"
};

