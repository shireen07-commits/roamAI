"""
Interactive CLI client for RoamAI.
"""

import logging
import json
import os
import sys
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional

from roamai.models.travel import (
    UserPreferences, Location, TravelStyle, TravelInterest
)
from roamai.services.travel_planner import TravelPlannerService
from roamai.services.notification_service import NotificationService
from roamai.utils.helpers import format_currency, format_date

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header."""
    clear_screen()
    print("=" * 80)
    print(f"{'RoamAI - Travel Planning Assistant':^80}")
    print("=" * 80)
    print()

def get_user_preferences() -> UserPreferences:
    """
    Collect user preferences interactively.
    
    Returns:
        UserPreferences object
    """
    print("Let's plan your trip! Please provide some details about your preferences.")
    print()
    
    # Destination
    destination = input("Where would you like to go? (leave blank to get recommendations): ").strip()
    
    # Budget
    while True:
        try:
            budget_str = input("What is your budget for this trip (in USD)? ")
            budget = float(budget_str)
            if budget <= 0:
                print("Budget must be greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    # Travel dates
    while True:
        try:
            start_date_str = input("When do you want to start your trip (YYYY-MM-DD)? ")
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            
            end_date_str = input("When do you want to end your trip (YYYY-MM-DD)? ")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            
            if end_date < start_date:
                print("End date cannot be before start date.")
                continue
            
            break
        except ValueError:
            print("Please enter dates in the format YYYY-MM-DD.")
    
    # Number of travelers
    while True:
        try:
            travelers_str = input("How many travelers? ")
            travelers = int(travelers_str)
            if travelers <= 0:
                print("Number of travelers must be greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    # Travel style
    print("\nTravel Style (select one or more):")
    for i, style in enumerate(TravelStyle, 1):
        print(f"{i}. {style.value.capitalize()}")
    
    while True:
        try:
            style_indices_str = input("Enter the numbers of your preferred travel styles (comma-separated): ")
            style_indices = [int(idx.strip()) for idx in style_indices_str.split(",")]
            
            if not style_indices or any(idx < 1 or idx > len(TravelStyle) for idx in style_indices):
                print(f"Please enter valid numbers between 1 and {len(TravelStyle)}.")
                continue
            
            travel_style = [list(TravelStyle)[idx - 1] for idx in style_indices]
            break
        except ValueError:
            print("Please enter valid numbers.")
    
    # Interests
    print("\nInterests (select one or more):")
    for i, interest in enumerate(TravelInterest, 1):
        print(f"{i}. {interest.value.capitalize()}")
    
    while True:
        try:
            interest_indices_str = input("Enter the numbers of your interests (comma-separated): ")
            interest_indices = [int(idx.strip()) for idx in interest_indices_str.split(",")]
            
            if not interest_indices or any(idx < 1 or idx > len(TravelInterest) for idx in interest_indices):
                print(f"Please enter valid numbers between 1 and {len(TravelInterest)}.")
                continue
            
            interests = [list(TravelInterest)[idx - 1] for idx in interest_indices]
            break
        except ValueError:
            print("Please enter valid numbers.")
    
    # Flexibility
    flexible_dates = input("Are your travel dates flexible? (y/n): ").lower() == 'y'
    flexible_destination = input("Are you flexible with your destination? (y/n): ").lower() == 'y'
    
    # Special requirements
    special_requirements = input("Any special requirements or preferences? ")
    
    # Create UserPreferences object
    preferences = UserPreferences(
        destination=destination if destination else None,
        budget=budget,
        start_date=start_date,
        end_date=end_date,
        travelers=travelers,
        travel_style=travel_style,
        interests=interests,
        is_flexible_dates=flexible_dates,
        is_flexible_destination=flexible_destination,
        special_requirements=special_requirements if special_requirements else None
    )
    
    return preferences

def select_destination(recommendations: List[Location]) -> Optional[Location]:
    """
    Let the user select a destination from recommendations.
    
    Args:
        recommendations: List of recommended destinations
    
    Returns:
        Selected destination or None if canceled
    """
    print("\nRecommended Destinations:")
    for i, location in enumerate(recommendations, 1):
        print(f"{i}. {location.city}, {location.country}")
    
    while True:
        try:
            choice = input("\nSelect a destination (number) or 'q' to quit: ")
            
            if choice.lower() == 'q':
                return None
            
            idx = int(choice) - 1
            if idx < 0 or idx >= len(recommendations):
                print(f"Please enter a number between 1 and {len(recommendations)}.")
                continue
            
            return recommendations[idx]
        except ValueError:
            print("Please enter a valid number.")

def get_traveler_details() -> Dict[str, Any]:
    """
    Collect traveler details.
    
    Returns:
        Dictionary with traveler details
    """
    print("\nPlease provide your contact information:")
    
    name = input("Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    departure_city = input("Departure City: ")
    
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "departure_city": departure_city
    }

def display_itinerary(itinerary: Dict[str, Any]):
    """
    Display an itinerary.
    
    Args:
        itinerary: Travel itinerary data
    """
    clear_screen()
    print("=" * 80)
    print(f"{'Your Travel Itinerary':^80}")
    print("=" * 80)
    print()
    
    # Destination and dates
    destination = itinerary["destination"]
    print(f"Destination: {destination['city']}, {destination['country']}")
    print(f"Dates: {itinerary['start_date']} to {itinerary['end_date']}")
    print(f"Duration: {(datetime.fromisoformat(itinerary['end_date']).date() - datetime.fromisoformat(itinerary['start_date']).date()).days + 1} days")
    print(f"Travelers: {itinerary['user_preferences']['travelers']}")
    print(f"Total Cost: ${itinerary['total_cost']:.2f}")
    print()
    
    # Flights
    if itinerary["flights"]:
        print("Flights:")
        for i, flight in enumerate(itinerary["flights"]):
            direction = "Outbound" if i == 0 else "Return"
            print(f"  {direction}: {flight['airline']} {flight['flight_number']}")
            print(f"    {flight['departure_airport']} to {flight['arrival_airport']}")
            print(f"    Departure: {flight['departure_time']}")
            print(f"    Arrival: {flight['arrival_time']}")
            print(f"    Cabin: {flight['cabin_class']}")
            print(f"    Price: ${flight['price']:.2f}")
            print()
    
    # Accommodation
    if itinerary["accommodation"]:
        acc = itinerary["accommodation"]
        print("Accommodation:")
        print(f"  {acc['name']}")
        print(f"  {acc['type'].capitalize()} - {acc['room_type']}")
        print(f"  Check-in: {acc['check_in_date']}")
        print(f"  Check-out: {acc['check_out_date']}")
        print(f"  Rating: {acc['rating']} / 5")
        print(f"  Price per night: ${acc['price_per_night']:.2f}")
        print(f"  Total price: ${acc['total_price']:.2f}")
        
        if acc["amenities"]:
            print(f"  Amenities: {', '.join(acc['amenities'])}")
        print()
    
    # Daily itineraries
    if itinerary["daily_itineraries"]:
        print("Daily Itineraries:")
        for day in itinerary["daily_itineraries"]:
            print(f"  Day {day['day_number']} - {day['date']}:")
            
            if day["activities"]:
                print("    Activities:")
                for activity in day["activities"]:
                    print(f"      - {activity['name']} (${activity['price_per_person']:.2f} per person)")
                    print(f"        {activity['description']}")
                    if activity["start_time"]:
                        print(f"        Time: {activity['start_time']}")
                    print()
            
            if day["restaurants"]:
                print("    Dining:")
                for restaurant in day["restaurants"]:
                    print(f"      - {restaurant['name']} ({restaurant['price_range']})")
                    print(f"        {restaurant['description']}")
                    print()
            
            if day["notes"]:
                print(f"    Notes: {day['notes']}")
            
            print()
    
    # Bookings
    if itinerary["bookings"]:
        print("Booking References:")
        for booking in itinerary["bookings"]:
            print(f"  {booking['booking_type'].capitalize()}: {booking['reference_number']} ({booking['status']})")
        print()
    
    print("=" * 80)
    input("Press Enter to continue...")

def main():
    """Main function."""
    # Initialize services
    travel_planner = TravelPlannerService()
    notification_service = NotificationService()
    
    # Main menu loop
    while True:
        print_header()
        print("1. Plan a new trip")
        print("2. View trending destinations")
        print("3. Exit")
        print()
        
        choice = input("Select an option: ")
        
        if choice == "1":
            # Plan a new trip
            print_header()
            preferences = get_user_preferences()
            
            # If no destination specified, get recommendations
            if not preferences.destination:
                print("\nGenerating destination recommendations based on your preferences...")
                recommendations = travel_planner.recommend_destinations(preferences)
                
                if not recommendations:
                    print("Sorry, no destinations found matching your preferences.")
                    input("Press Enter to continue...")
                    continue
                
                selected_destination = select_destination(recommendations)
                if not selected_destination:
                    continue
            else:
                # Create a location object for the specified destination
                selected_destination = Location(
                    city=preferences.destination,
                    country="Unknown"  # In a real app, this would be looked up
                )
            
            # Get traveler details
            traveler_details = get_traveler_details()
            
            print("\nCreating your personalized travel itinerary...")
            try:
                itinerary = travel_planner.create_and_book_itinerary(
                    preferences, selected_destination, traveler_details
                )
                
                if itinerary:
                    # Convert to dictionary for easier display
                    itinerary_dict = json.loads(itinerary.model_dump_json())
                    
                    # Send confirmation email
                    notification_service.send_booking_confirmation(
                        itinerary, traveler_details["email"]
                    )
                    
                    # Display itinerary
                    display_itinerary(itinerary_dict)
                else:
                    print("Sorry, there was an error creating your itinerary.")
                    input("Press Enter to continue...")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                input("Press Enter to continue...")
        
        elif choice == "2":
            # View trending destinations
            print_header()
            
            region = input("Enter a region to focus on (leave blank for global): ").strip()
            region = region if region else None
            
            print(f"\nFetching trending destinations{'for ' + region if region else ''}...")
            
            try:
                trending = travel_planner.get_trending_destinations(region)
                
                clear_screen()
                print("=" * 80)
                print(f"{'Trending Destinations':^80}")
                print("=" * 80)
                print()
                
                if "destinations" in trending:
                    for i, dest in enumerate(trending["destinations"], 1):
                        print(f"{i}. {dest.get('city', 'Unknown')}, {dest.get('country', 'Unknown')}")
                        print(f"   {dest.get('description', '')}")
                        
                        if "key_attractions" in dest and dest["key_attractions"]:
                            print(f"   Key attractions: {', '.join(dest['key_attractions'])}")
                        
                        if "estimated_daily_cost" in dest:
                            print(f"   Estimated daily cost: ${dest['estimated_daily_cost']:.2f}")
                        
                        print()
                
                input("Press Enter to continue...")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                input("Press Enter to continue...")
        
        elif choice == "3":
            # Exit
            print_header()
            print("Thank you for using RoamAI!")
            print("Goodbye!")
            sys.exit(0)
        
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_header()
        print("Operation cancelled by user.")
        print("Thank you for using RoamAI!")
        print("Goodbye!")
        sys.exit(0)