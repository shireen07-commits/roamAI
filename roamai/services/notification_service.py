"""
Notification service for RoamAI.
Handles sending emails and notifications to users.
"""

import logging
from datetime import datetime
from typing import Optional, List

from ..models.travel import TravelItinerary

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationService:
    """Service for sending notifications to users."""
    
    def __init__(self):
        """Initialize the notification service."""
        pass
    
    def send_booking_confirmation(self, itinerary: TravelItinerary, recipient_email: str) -> bool:
        """
        Send a booking confirmation email.
        
        Args:
            itinerary: The travel itinerary
            recipient_email: Email address to send to
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            logger.info(f"Sending booking confirmation to {recipient_email}")
            
            # Format dates for email
            start_date_str = itinerary.start_date.strftime("%b %d, %Y")
            end_date_str = itinerary.end_date.strftime("%b %d, %Y")
            
            # Construct email subject
            subject = f"Your Travel Booking Confirmation - {itinerary.destination.city}"
            
            # Construct email body
            body = f"""Dear Traveler,

Thank you for booking your trip to {itinerary.destination.city}, {itinerary.destination.country} with RoamAI. Your booking is confirmed!

Itinerary Summary:
-----------------
Destination: {itinerary.destination.city}, {itinerary.destination.country}
Dates: {start_date_str} to {end_date_str}
Travelers: {itinerary.user_preferences.travelers}
Total Cost: ${itinerary.total_cost:.2f}

Booking References:
-----------------"""

            # Add flights
            if itinerary.flights:
                body += "\nFlights:"
                for i, flight in enumerate(itinerary.flights):
                    direction = "Outbound" if i == 0 else "Return"
                    departure_date = flight.departure_time.strftime("%b %d, %Y at %H:%M")
                    body += f"""
- {direction}: {flight.airline} {flight.flight_number}
  {flight.departure_airport} to {flight.arrival_airport}
  Departing: {departure_date}
  Cabin: {flight.cabin_class}"""
            
            # Add accommodation
            if itinerary.accommodation:
                acc = itinerary.accommodation
                body += f"""

Accommodation:
- {acc.name}
  Room: {acc.room_type}
  Check-in: {start_date_str}
  Check-out: {end_date_str}"""
            
            # Add booking references
            body += "\n\nYour Booking References:"
            for booking in itinerary.bookings:
                body += f"\n- {booking.booking_type.capitalize()}: {booking.reference_number} ({booking.status})"
            
            # Add notes
            if itinerary.notes:
                body += f"\n\nNotes:\n{itinerary.notes}"
            
            # Add footer
            body += f"""

Thank you for choosing RoamAI for your travel needs.
For any questions, please contact our support team.

Safe travels!
The RoamAI Team
"""
            
            # Log email content for demo purposes
            logger.info(f"Email Subject: {subject}")
            logger.info(f"Email Body: {body[:500]}...") # Log first 500 chars
            
            # In a real application, we would actually send the email here
            # For this demo, we'll just pretend we did
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending booking confirmation: {e}")
            return False
    
    def send_travel_alert(self, recipient_email: str, alert_message: str) -> bool:
        """
        Send a travel alert notification.
        
        Args:
            recipient_email: Email address to send to
            alert_message: The alert message
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            logger.info(f"Sending travel alert to {recipient_email}")
            
            # Construct email subject
            subject = "Important Travel Alert from RoamAI"
            
            # Construct email body
            body = f"""Dear Traveler,

IMPORTANT TRAVEL ALERT:

{alert_message}

This alert is provided to help you stay informed about your upcoming or current travel.
Please take any necessary actions to ensure your safety and convenience.

If you have any questions, please contact our support team.

Safe travels!
The RoamAI Team
"""
            
            # Log email content for demo purposes
            logger.info(f"Email Subject: {subject}")
            logger.info(f"Email Body: {body}")
            
            # In a real application, we would actually send the email here
            # For this demo, we'll just pretend we did
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending travel alert: {e}")
            return False