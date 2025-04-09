"""
Demonstration script for RoamAI.
This script runs a fixed demo without requiring interactive input.
"""

import logging
import json
from datetime import datetime, date, timedelta
import os
import sys

from roamai.models.travel import (
    UserPreferences, Location, TravelStyle, TravelInterest
)
from roamai.services.travel_planner import TravelPlannerService
from roamai.services.notification_service import NotificationService

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """Run a fixed demo of RoamAI functionality."""
    print("=" * 80)
    print(f"{'RoamAI - Travel Planning Assistant Demo':^80}")
    print("=" * 80)
    print()
    
    # Initialize services
    travel_planner = TravelPlannerService()
    notification_service = NotificationService()
    
    # Create sample user preferences
    preferences = UserPreferences(
        destination="Dubai",
        budget=5000.0,
        start_date=date.today() + timedelta(days=30),  # 30 days from today
        end_date=date.today() + timedelta(days=35),    # 35 days from today (5-day trip)
        travelers=2,
        travel_style=[TravelStyle.LUXURY],
        interests=[TravelInterest.FOOD, TravelInterest.SHOPPING, TravelInterest.CULTURE],
        is_flexible_dates=False,
        is_flexible_destination=False,
        special_requirements="We prefer hotels with spa facilities"
    )
    
    print(f"Sample User Preferences:")
    print(f"- Destination: {preferences.destination or 'No preference'}")
    print(f"- Budget: ${preferences.budget:.2f}")
    print(f"- Travel dates: {preferences.start_date} to {preferences.end_date}")
    print(f"- Travelers: {preferences.travelers}")
    print(f"- Travel style: {', '.join([s.value for s in preferences.travel_style])}")
    print(f"- Interests: {', '.join([i.value for i in preferences.interests])}")
    print(f"- Special requirements: {preferences.special_requirements or 'None'}")
    print()
    
    # Create destination location
    destination = Location(
        city="Dubai",
        country="United Arab Emirates",
        region="Middle East"
    )
    
    # Create traveler details
    traveler_details = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "departure_city": "New York"
    }
    
    print(f"Creating travel itinerary for {destination.city}, {destination.country}...")
    print()
    
    # Create itinerary
    try:
        itinerary = travel_planner.create_and_book_itinerary(
            preferences, destination, traveler_details
        )
        
        if itinerary:
            # Send confirmation email
            notification_service.send_booking_confirmation(
                itinerary, traveler_details["email"]
            )
            
            # Convert to dictionary for easier display
            itinerary_dict = json.loads(itinerary.model_dump_json())
            
            print("Itinerary created successfully!")
            print()
            
            print(f"Destination: {itinerary.destination.city}, {itinerary.destination.country}")
            print(f"Dates: {itinerary.start_date} to {itinerary.end_date}")
            print(f"Duration: {(itinerary.end_date - itinerary.start_date).days + 1} days")
            print(f"Total Cost: ${itinerary.total_cost:.2f}")
            print()
            
            # Display flights
            if itinerary.flights:
                print("Flights:")
                for i, flight in enumerate(itinerary.flights):
                    direction = "Outbound" if i == 0 else "Return"
                    print(f"  {direction}: {flight.airline} {flight.flight_number}")
                    print(f"    {flight.departure_airport} to {flight.arrival_airport}")
                    print(f"    Departure: {flight.departure_time}")
                    print(f"    Cabin: {flight.cabin_class}")
                    print(f"    Price: ${flight.price:.2f}")
                    print()
            
            # Display accommodation
            if itinerary.accommodation:
                acc = itinerary.accommodation
                print("Accommodation:")
                print(f"  {acc.name}")
                print(f"  {acc.type.capitalize()} - {acc.room_type}")
                print(f"  Rating: {acc.rating} / 5")
                print(f"  Price per night: ${acc.price_per_night:.2f}")
                print(f"  Total price: ${acc.total_price:.2f}")
                
                if acc.amenities:
                    print(f"  Amenities: {', '.join(acc.amenities[:5])}")
                print()
            
            # Display summary of daily itineraries
            if itinerary.daily_itineraries:
                print("Daily Itineraries (summary):")
                for day in itinerary.daily_itineraries:
                    print(f"  Day {day.day_number} - {day.date}:")
                    
                    if day.activities:
                        print(f"    Activities: {len(day.activities)} planned")
                    
                    if day.restaurants:
                        print(f"    Dining: {len(day.restaurants)} recommendations")
                    
                    print()
            
            # Display booking references
            if itinerary.bookings:
                print("Booking References:")
                for booking in itinerary.bookings:
                    print(f"  {booking.booking_type.capitalize()}: {booking.reference_number} ({booking.status})")
                print()
            
            # Display notes
            if itinerary.notes:
                print(f"Notes: {itinerary.notes}")
                print()
            
            print("Email confirmation sent to:", traveler_details["email"])
            print()
            
            print("=" * 80)
            print(f"{'Demo Completed Successfully':^80}")
            print("=" * 80)
        else:
            print("Error: Failed to create itinerary.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()