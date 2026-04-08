# Copyright (c) 2026, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today, get_url_to_form


class IncidentReport(Document):

	def on_update(self):
		'''
			Handle resolution date + email notification on Assign and Resolve actions
		'''
		if not self.has_value_changed("status"):
			return

		if self.status == "Resolved":
			if not self.resolution_date:
				self.db_set("resolution_date", today())

		if self.status == "In Progress":
			if self.resolution_date:
				self.db_set("resolution_date", None)

		if self.status == "In Progress" and self.assigned_to:
			email = self.get_employee_email(self.assigned_to)

			if email:
				frappe.sendmail(
					recipients=[email],
					subject=f"Incident {self.name} Assigned to You",
					message=self.get_assign_message(),
					now=True
				)

		if self.status == "Resolved" and self.reported_by:
			email = self.get_employee_email(self.reported_by)

			if email:
				frappe.sendmail(
					recipients=[email],
					subject=f"Incident {self.name} Resolved",
					message=self.get_resolve_message(),
					now=True
				)

	def get_employee_email(self, employee):
		'''
			Get the email of the employee
		'''
		user = frappe.db.get_value("Employee", employee, "user_id")
		if user:
			return frappe.db.get_value("User", user, "email")
		return None

	def get_assign_message(self):
		'''
			Message to be sent to the assignee when the incident is assigned to them
		'''
		return f"""
		<p>Hello,</p>
		<p>An incident has been <b>assigned</b> to you.</p>

		<p><b>ID:</b> {self.name}</p>
		<p><b>Title:</b> {self.incident_title}</p>

		<p>
			<a href="{get_url_to_form(self.doctype, self.name)}">
				View Incident
			</a>
		</p>
		"""

	def get_resolve_message(self):
		'''
			Message to be sent to the reporter when the incident is resolved
	'''
		return f"""
		<p>Hello,</p>
		<p>Your reported incident has been <b>resolved</b>.</p>

		<p><b>ID:</b> {self.name}</p>
		<p><b>Resolution:</b> {self.resolution_notes or "N/A"}</p>

		<p>
			<a href="{get_url_to_form(self.doctype, self.name)}">
				View Incident
			</a>
		</p>
		"""
