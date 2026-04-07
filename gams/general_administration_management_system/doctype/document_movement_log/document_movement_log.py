# Copyright (c) 2026, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today

class DocumentMovementLog(Document):

	def validate(self):
		self.validate_departments()
		self.validate_date()

	def validate_departments(self):
		if self.from_department == self.to_department:
			frappe.throw("From Department and To Department cannot be the same")

	def validate_date(self):
		if self.date and getdate(self.date) < getdate(today()):
			frappe.throw("Date cannot be in the past")
