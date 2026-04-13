# Copyright (c) 2026, efeone and contributors
# For license information, please see license.txt
import frappe
from frappe.utils import get_url_to_form

def before_save(doc, method):
	'''
		Prevent self-approval of Travel Requests
	'''
	if doc.workflow_state == "Approved":

		if doc.owner == frappe.session.user:
			frappe.throw("You cannot approve your own Travel Request.")

		if doc.employee:
			user = frappe.db.get_value("Employee", doc.employee, "user_id")

			if user and user == frappe.session.user:
				frappe.throw("You cannot approve your own Travel Request.")

def on_update(doc, method):
	'''
		Send email notifications on Travel Request submission and status changes
  	'''
	if doc.workflow_state == "Submitted":
		emails = get_manager_emails()

		if emails:
			frappe.sendmail(
				recipients=emails,
				subject=f"Travel Request {doc.name} Submitted",
				message=get_submit_message(doc),
				now=True
			)

	if doc.workflow_state in ["Approved", "Rejected"]:
		email = get_employee_email(doc.employee)

		if email:
			frappe.sendmail(
				recipients=[email],
				subject=f"Travel Request {doc.workflow_state}: {doc.name}",
				message=get_status_message(doc),
				now=True
			)

def get_employee_email(employee):
	'''
		Get the email of the employee
	'''
	user = frappe.db.get_value("Employee", employee, "user_id")
	if user:
		return frappe.db.get_value("User", user, "email")
	return None

def get_manager_emails():
	'''
		Get the emails of all GAMS Managers
	'''
	managers = frappe.get_all(
		"Has Role",
		filters={"role": "GAMS Manager"},
		fields=["parent"]
	)

	emails = [frappe.db.get_value("User", m.parent, "email") for m in managers]
	return list(set(filter(None, emails)))

def get_submit_message(doc):
	'''
		Message to be sent to GAMS Managers when a Travel Request is submitted
	'''
	return f"""
	<p>Hello,</p>

	<p>A new <b>Travel Request</b> has been submitted for your approval.</p>

	<p><b>Request ID:</b> {doc.name}</p>
	<p><b>Employee:</b> {doc.employee_name}</p>
	<p><b>Purpose:</b> {doc.purpose_of_travel}</p>

	<p>
		<a href="{get_url_to_form(doc.doctype, doc.name)}">
			View Travel Request
		</a>
	</p>
	"""

def get_status_message(doc):
	'''
		Message to be sent to the employee when their Travel Request is approved or rejected
	'''
	return f"""
	<p>Hello,</p>

	<p>Your <b>Travel Request</b> has been 
	<b>{doc.workflow_state}</b>.</p>

	<p><b>Request ID:</b> {doc.name}</p>
	<p><b>Purpose:</b> {doc.purpose_of_travel}</p>

	<p>
		<a href="{get_url_to_form(doc.doctype, doc.name)}">
			View Travel Request
		</a>
	</p>
	"""
