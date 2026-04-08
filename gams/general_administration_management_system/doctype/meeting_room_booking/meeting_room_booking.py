# Copyright (c) 2026, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate, get_time

class MeetingRoomBooking(Document):

	def validate(self):
		self.validate_time()
		self.validate_date()
		self.validate_room_availability()

	def validate_time(self):
		if self.from_time and self.to_time:
			if self.to_time <= self.from_time:
				frappe.throw("To Time must be greater than From Time")

	def validate_date(self):
		if self.booking_date:
			if getdate(self.booking_date) < getdate(nowdate()):
				frappe.throw("Booking Date cannot be in the past")

	def validate_room_availability(self):
		"""
		Ensure booking is within room's available time window
		"""

		if not self.meeting_room:
			return

		room = frappe.get_doc("Room", self.meeting_room)

		from_time = get_time(self.from_time)
		to_time = get_time(self.to_time)
		available_from = get_time(room.availability_from)
		available_to = get_time(room.availability_to)

		if from_time < available_from or to_time > available_to:
			frappe.throw(
				f"Booking not permitted outside room availability hours "
				f"({available_from} - {available_to})"
			)
