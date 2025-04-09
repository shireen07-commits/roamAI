"""
Script to test the notification service and show a full sample email.
"""

import os
import sys
from datetime import datetime, date, timedelta

# Ensure PYTHONPATH includes the current directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roamai.services.notification_service import NotificationService
from roamai.models.travel import (
    UserPreferences, TravelStyle, TravelInterest, Location, 
    TravelItinerary, Flight, Accommodation, Booking
)

def create_sample_itinerary():
    """Create a sample itinerary for testing."""
    # Create user preferences
    preferences = UserPreferences(
        destination="Dubai",
        budget=5000.0,
        start_date=date.today() + timedelta(days=30),
        end_date=date.today() + timedelta(days=35),
        travelers=2,
        travel_style=[TravelStyle.LUXURY],
        interests=[TravelInterest.FOOD, TravelInterest.SHOPPING, TravelInterest.CULTURE],
        is_flexible_dates=False,
        is_flexible_destination=False,
        special_requirements="We prefer hotels with spa facilities"
    )
    
    # Create destination
    destination = Location(
        city="Dubai",
        country="United Arab Emirates",
        region="Middle East"
    )
    
    # Create outbound flight
    outbound_flight = Flight(
        flight_id="F001",
        airline="Emirates",
        flight_number="EK203",
        departure_airport="JFK",
        arrival_airport="DXB",
        departure_time=datetime.combine(preferences.start_date, datetime.min.time()) + timedelta(hours=10),
        arrival_time=datetime.combine(preferences.start_date, datetime.min.time()) + timedelta(hours=22),
        duration_minutes=720,
        cabin_class="Business",
        price=1200.50,
        booking_url="https://emirates.com/booking/123",
        stops=0,
        available_seats=120
    )
    
    # Create return flight
    return_flight = Flight(
        flight_id="F002",
        airline="Emirates",
        flight_number="EK204",
        departure_airport="DXB",
        arrival_airport="JFK",
        departure_time=datetime.combine(preferences.end_date, datetime.min.time()) + timedelta(hours=14),
        arrival_time=datetime.combine(preferences.end_date, datetime.min.time()) + timedelta(hours=20),
        duration_minutes=840,
        cabin_class="Business",
        price=1300.75,
        booking_url="https://emirates.com/booking/456",
        stops=0,
        available_seats=150
    )
    
    # Create accommodation
    accommodation = Accommodation(
        accommodation_id="A001",
        name="Burj Al Arab",
        type="Luxury Hotel",
        address="Jumeirah Beach Road",
        location=destination,
        room_type="Suite",
        price_per_night=1200.00,
        total_price=6000.00,
        check_in_date=preferences.start_date,
        check_out_date=preferences.end_date,
        rating=5.0,
        amenities=["Pool", "Spa", "Private Beach", "24/7 Butler", "Helipad"],
        booking_url="https://burjalarab.com/booking/789",
        images=["https://example.com/burj1.jpg", "https://example.com/burj2.jpg"],
        availability=True
    )
    
    # Create bookings
    flight_booking1 = Booking(
        booking_id="B001",
        booking_type="flight",
        reference_number="EK123456",
        status="confirmed",
        booking_date=datetime.now(),
        total_price=outbound_flight.price,
        currency="USD",
        payment_method="Credit Card",
        provider="Emirates"
    )
    
    flight_booking2 = Booking(
        booking_id="B002",
        booking_type="flight",
        reference_number="EK789012",
        status="confirmed",
        booking_date=datetime.now(),
        total_price=return_flight.price,
        currency="USD",
        payment_method="Credit Card",
        provider="Emirates"
    )
    
    accommodation_booking = Booking(
        booking_id="B003",
        booking_type="accommodation",
        reference_number="BJ345678",
        status="confirmed",
        booking_date=datetime.now(),
        total_price=accommodation.total_price,
        currency="USD",
        payment_method="Credit Card",
        provider="Jumeirah"
    )
    
    # Create the itinerary
    itinerary = TravelItinerary(
        itinerary_id="ITN12345",
        user_preferences=preferences,
        destination=destination,
        start_date=preferences.start_date,
        end_date=preferences.end_date,
        flights=[outbound_flight, return_flight],
        accommodation=accommodation,
        daily_itineraries=[],  # Empty for this test
        bookings=[flight_booking1, flight_booking2, accommodation_booking],
        total_cost=outbound_flight.price + return_flight.price + accommodation.total_price,
        notes="This is a luxury trip to Dubai with a stay at the iconic Burj Al Arab.",
        created_at=datetime.now(),
        modified_at=datetime.now()
    )
    
    return itinerary

def main():
    """Test the notification service."""
    # Create a sample itinerary
    itinerary = create_sample_itinerary()
    
    # Create the notification service
    notification_service = NotificationService()
    
    # Send a booking confirmation
    notification_service.send_booking_confirmation(itinerary, "john.doe@example.com")
    
    # Send a travel alert
    notification_service.send_travel_alert(
        "john.doe@example.com",
        "Your flight EK203 is delayed by 1 hour due to weather conditions. New departure time is 11:00 AM."
    )

if __name__ == "__main__":
    main()