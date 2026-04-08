# Copyright (c) 2026, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Room(Document):

    def validate(self):
        self.validate_time_range()

    def validate_time_range(self):
        """
        Ensure availability_from is earlier than availability_to.
        """
        if self.availability_from and self.availability_to:
            if self.availability_from >= self.availability_to:
                frappe.throw("Available From must be earlier than Available To")
