# Copyright (c) 2026, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today

class IncidentReport(Document):

	def on_update(self):
		'''
  			Auto set resolution date when status is Resolved 
'''
		if self.status == "Resolved" and not self.resolution_date:
			self.resolution_date = today()