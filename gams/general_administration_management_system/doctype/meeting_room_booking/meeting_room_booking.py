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
		self.validate_duplicate_booking()

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

	def validate_duplicate_booking(self):
		"""
		Prevent overlapping bookings for the same room.

		Overlap condition:
			Existing.from_time < New.to_time AND
			Existing.to_time > New.from_time
		"""

		if not (self.meeting_room and self.booking_date and self.from_time and self.to_time):
			return

		from_time = get_time(self.from_time)
		to_time = get_time(self.to_time)

		overlapping_bookings = frappe.db.sql("""
			SELECT name, from_time, to_time
			FROM `tabMeeting Room Booking`
			WHERE
				meeting_room = %s
				AND booking_date = %s
				AND name != %s
				AND docstatus != 2
				AND from_time < %s
				AND to_time > %s
		""", (
			self.meeting_room,
			self.booking_date,
			self.name or "",
			to_time,
			from_time
		), as_dict=True)

		if overlapping_bookings:
			booking = overlapping_bookings[0]

			frappe.throw(
				f"Room already booked from {booking.from_time} to {booking.to_time} for this day"
			)

