"""
Travel planner service that coordinates all the other services.
"""

import logging
import uuid
import random
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any, Tuple

from ..models.travel import (
    UserPreferences, TravelItinerary, Location, Flight, Accommodation, 
    Activity, Restaurant, DailyItinerary, Booking, Transportation
)
from ..core.config import settings
from .openai_service import OpenAIService
from .flight_service import FlightService
from .accommodation_service import AccommodationService
from .activity_service import ActivityService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TravelPlannerService:
    """Service for planning and booking complete travel itineraries."""
    
    def __init__(self):
        """Initialize the travel planner service."""
        self.openai_service = OpenAIService()
        self.flight_service = FlightService()
        self.accommodation_service = AccommodationService()
        self.activity_service = ActivityService()
    
    def recommend_destinations(self, preferences: UserPreferences) -> List[Location]:
        """
        Recommend destinations based on user preferences.
        
        Args:
            preferences: User preferences
            
        Returns:
            List of recommended destinations
        """
        logger.info("Generating destination recommendations")
        
        # Use OpenAI to generate destination recommendations
        return self.openai_service.generate_travel_recommendations(preferences)
    
    def create_and_book_itinerary(
        self, 
        preferences: UserPreferences, 
        destination: Location,
        traveler_details: Dict[str, Any]
    ) -> Optional[TravelItinerary]:
        """
        Create and book a complete travel itinerary.
        
        Args:
            preferences: User preferences
            destination: Selected destination
            traveler_details: Dictionary with traveler information
            
        Returns:
            Complete travel itinerary with bookings
        """
        logger.info(f"Creating and booking itinerary for {destination.city}, {destination.country}")
        
        try:
            # 1. Create itinerary ID
            itinerary_id = f"ITN{uuid.uuid4().hex[:8].upper()}"
            
            # 2. Search and book flights
            flights, flight_bookings = self._handle_flights(preferences, destination, traveler_details)
            
            # 3. Search and book accommodation
            accommodation, accommodation_booking = self._handle_accommodation(preferences, destination, traveler_details)
            
            # 4. Search activities and create daily itineraries
            daily_itineraries, activity_bookings = self._handle_activities(preferences, destination, traveler_details)
            
            # 5. Combine all bookings
            bookings = []
            bookings.extend(flight_bookings)
            if accommodation_booking:
                bookings.append(accommodation_booking)
            bookings.extend(activity_bookings)
            
            # 6. Calculate total cost
            total_cost = self._calculate_total_cost(flights, accommodation, daily_itineraries)
            
            # 7. Create and return the complete itinerary
            itinerary = TravelItinerary(
                itinerary_id=itinerary_id,
                user_preferences=preferences,
                destination=destination,
                start_date=preferences.start_date,
                end_date=preferences.end_date,
                flights=flights,
                accommodation=accommodation,
                daily_itineraries=daily_itineraries,
                bookings=bookings,
                total_cost=total_cost,
                notes=self._generate_itinerary_notes(preferences, destination),
                created_at=datetime.now(),
                modified_at=datetime.now()
            )
            
            return itinerary
            
        except Exception as e:
            logger.error(f"Error creating and booking itinerary: {e}")
            return None
    
    def get_trending_destinations(self, region: Optional[str] = None) -> Dict[str, Any]:
        """
        Get trending destinations.
        
        Args:
            region: Optional region to focus on
            
        Returns:
            Dictionary with trending destinations
        """
        return self.openai_service.analyze_destination_trends(region)
    
    def get_destination_social_content(self, destination: str) -> Dict[str, Any]:
        """
        Get social media content for a destination.
        
        Args:
            destination: Destination name
            
        Returns:
            Dictionary with social media content
        """
        return self.openai_service.get_social_media_content(destination)
    
    def get_pilgrimage_info(self, preferences: UserPreferences) -> Dict[str, Any]:
        """
        Get pilgrimage-specific information and recommendations.
        
        Args:
            preferences: User preferences
            
        Returns:
            Dictionary with pilgrimage information
        """
        return self.openai_service.process_pilgrimage_requirements(preferences)
    
    def _handle_flights(
        self, 
        preferences: UserPreferences, 
        destination: Location,
        traveler_details: Dict[str, Any]
    ) -> Tuple[List[Flight], List[Booking]]:
        """
        Search and book flights.
        
        Args:
            preferences: User preferences
            destination: Selected destination
            traveler_details: Dictionary with traveler information
            
        Returns:
            Tuple of (list of flights, list of flight bookings)
        """
        origin = traveler_details.get("departure_city", "New York")  # Default origin
        dest_city = destination.city
        
        # Determine if luxury should be prioritized
        prioritize_luxury = settings.PRIORITIZE_LUXURY and "LUXURY" in [s.value for s in preferences.travel_style]
        
        # Search for outbound flight
        outbound_flights = self.flight_service.search_flights(
            origin=origin,
            destination=dest_city,
            departure_date=datetime.combine(preferences.start_date, datetime.min.time()),
            passengers=preferences.travelers,
            cabin_class="Business" if prioritize_luxury else "Economy",
            prioritize_luxury=prioritize_luxury
        )
        
        # Search for return flight
        return_flights = self.flight_service.search_flights(
            origin=dest_city,
            destination=origin,
            departure_date=datetime.combine(preferences.end_date, datetime.min.time()),
            passengers=preferences.travelers,
            cabin_class="Business" if prioritize_luxury else "Economy",
            prioritize_luxury=prioritize_luxury
        )
        
        selected_flights = []
        flight_bookings = []
        
        # Book outbound flight (select the first one for simplicity)
        if outbound_flights:
            selected_flight = outbound_flights[0]
            selected_flights.append(selected_flight)
            booking = self.flight_service.book_flight(selected_flight, traveler_details)
            if booking:
                flight_bookings.append(booking)
        
        # Book return flight (select the first one for simplicity)
        if return_flights:
            selected_flight = return_flights[0]
            selected_flights.append(selected_flight)
            booking = self.flight_service.book_flight(selected_flight, traveler_details)
            if booking:
                flight_bookings.append(booking)
        
        return selected_flights, flight_bookings
    
    def _handle_accommodation(
        self, 
        preferences: UserPreferences, 
        destination: Location,
        traveler_details: Dict[str, Any]
    ) -> Tuple[Optional[Accommodation], Optional[Booking]]:
        """
        Search and book accommodation.
        
        Args:
            preferences: User preferences
            destination: Selected destination
            traveler_details: Dictionary with traveler information
            
        Returns:
            Tuple of (accommodation, accommodation booking)
        """
        # Determine if luxury should be prioritized
        prioritize_luxury = settings.PRIORITIZE_LUXURY and "LUXURY" in [s.value for s in preferences.travel_style]
        
        # Calculate room count (assume 1 room for up to 2 travelers, then additional rooms as needed)
        room_count = max(1, (preferences.travelers + 1) // 2)
        
        # Search for accommodations
        accommodations = self.accommodation_service.search_accommodations(
            destination=destination,
            check_in_date=preferences.start_date,
            check_out_date=preferences.end_date,
            guests=preferences.travelers,
            room_count=room_count,
            min_rating=4 if prioritize_luxury else 0,
            max_price=preferences.budget * 0.4,  # Allocate up to 40% of the budget for accommodation
            prioritize_luxury=prioritize_luxury
        )
        
        if not accommodations:
            logger.warning("No accommodations found within the budget")
            return None, None
        
        # Select the first accommodation for simplicity
        selected_accommodation = accommodations[0]
        
        # Book the accommodation
        booking = self.accommodation_service.book_accommodation(selected_accommodation, traveler_details)
        
        return selected_accommodation, booking
    
    def _handle_activities(
        self, 
        preferences: UserPreferences, 
        destination: Location,
        traveler_details: Dict[str, Any]
    ) -> Tuple[List[DailyItinerary], List[Booking]]:
        """
        Search for activities and create daily itineraries.
        
        Args:
            preferences: User preferences
            destination: Selected destination
            traveler_details: Dictionary with traveler information
            
        Returns:
            Tuple of (list of daily itineraries, list of activity bookings)
        """
        daily_itineraries = []
        all_bookings = []
        
        # Calculate trip duration
        trip_duration = (preferences.end_date - preferences.start_date).days + 1
        
        # For each day of the trip
        current_date = preferences.start_date
        for day_number in range(1, trip_duration + 1):
            # Skip activity planning for the first and last day if there are flights
            # (assuming travelers will be busy with travel on these days)
            if (day_number == 1 or day_number == trip_duration) and trip_duration > 3:
                # Add a simple itinerary for travel days
                daily_itinerary = DailyItinerary(
                    date=current_date,
                    day_number=day_number,
                    activities=[],
                    restaurants=[],
                    transportation=[],
                    notes="Travel day. No activities planned."
                )
                daily_itineraries.append(daily_itinerary)
                current_date += timedelta(days=1)
                continue
            
            # Search for activities for this day based on user interests
            activities = self.activity_service.search_activities(
                destination=destination,
                date=current_date,
                interests=preferences.interests,
                travelers=preferences.travelers,
                max_price_per_person=preferences.budget * 0.1  # Allocate up to 10% of the budget per activity per person
            )
            
            # Select 2-3 activities for the day
            selected_activities = activities[:min(3, len(activities))]
            
            # Book each selected activity
            booked_activities = []
            for activity in selected_activities:
                booking = self.activity_service.book_activity(activity, traveler_details)
                if booking:
                    all_bookings.append(booking)
                    booked_activities.append(activity)
            
            # Generate mock restaurant recommendations
            restaurants = self._generate_mock_restaurants(destination, preferences, current_date)
            
            # Generate mock transportation options
            transportation = self._generate_mock_transportation(destination, booked_activities, current_date)
            
            # Create daily itinerary
            daily_itinerary = DailyItinerary(
                date=current_date,
                day_number=day_number,
                activities=booked_activities,
                restaurants=restaurants,
                transportation=transportation,
                notes=f"Day {day_number} of your {destination.city} adventure."
            )
            
            daily_itineraries.append(daily_itinerary)
            current_date += timedelta(days=1)
        
        return daily_itineraries, all_bookings
    
    def _generate_mock_restaurants(
        self, 
        destination: Location, 
        preferences: UserPreferences,
        date: date
    ) -> List[Restaurant]:
        """
        Generate mock restaurant recommendations.
        
        Args:
            destination: Destination location
            preferences: User preferences
            date: Day of the trip
            
        Returns:
            List of restaurant recommendations
        """
        restaurants = []
        
        # Restaurant types
        restaurant_types = ["Local Cuisine", "Fine Dining", "Casual Dining", "Street Food", "Cafe"]
        
        # Determine if luxury should be prioritized
        prioritize_luxury = settings.PRIORITIZE_LUXURY and "LUXURY" in [s.value for s in preferences.travel_style]
        
        # Generate 1-2 restaurant recommendations
        for _ in range(random.randint(1, 2)):
            restaurant_type = "Fine Dining" if prioritize_luxury else random.choice(restaurant_types)
            
            # Generate restaurant name based on type
            if restaurant_type == "Local Cuisine":
                name = f"Authentic {destination.city} Kitchen"
                cuisine = ["Local", destination.country + " Cuisine"]
                price_range = "$$" if prioritize_luxury else "$"
                rating = random.uniform(4.0, 4.5)
            elif restaurant_type == "Fine Dining":
                name = f"The {random.choice(['Grand', 'Royal', 'Luxe', 'Elite'])} {random.choice(['Table', 'Bistro', 'Brasserie', 'Garden'])}"
                cuisine = ["Fine Dining", "International", random.choice(["French", "Italian", "Japanese", "Fusion"])]
                price_range = "$$$$" if prioritize_luxury else "$$$"
                rating = random.uniform(4.5, 5.0)
            elif restaurant_type == "Casual Dining":
                name = f"{random.choice(['Sunny', 'Happy', 'Urban', 'Village'])} {random.choice(['Kitchen', 'Grill', 'Diner', 'Cafe'])}"
                cuisine = ["Casual", "International", random.choice(["American", "Mediterranean", "Asian", "Fusion"])]
                price_range = "$$"
                rating = random.uniform(3.5, 4.5)
            elif restaurant_type == "Street Food":
                name = f"{destination.city} Street Food Market"
                cuisine = ["Street Food", "Local", "Fast Food"]
                price_range = "$"
                rating = random.uniform(4.0, 4.8)
            else:  # Cafe
                name = f"{random.choice(['Morning', 'Sunny', 'City', 'Artisan'])} {random.choice(['Cafe', 'Coffee', 'Bakery', 'Patisserie'])}"
                cuisine = ["Cafe", "Coffee", "Bakery"]
                price_range = "$" if not prioritize_luxury else "$$"
                rating = random.uniform(4.0, 4.6)
            
            restaurant = Restaurant(
                restaurant_id=f"R{uuid.uuid4().hex[:8].upper()}",
                name=name,
                description=f"A {restaurant_type.lower()} restaurant offering {', '.join(cuisine).lower()} in a charming setting.",
                location=destination,
                cuisine=cuisine,
                price_range=price_range,
                rating=round(rating, 1),
                reservation_url=f"https://example.com/reserve/{uuid.uuid4().hex[:8]}",
                opening_hours={
                    "Monday": "11:00-22:00",
                    "Tuesday": "11:00-22:00",
                    "Wednesday": "11:00-22:00",
                    "Thursday": "11:00-22:00",
                    "Friday": "11:00-23:00",
                    "Saturday": "11:00-23:00",
                    "Sunday": "11:00-22:00"
                },
                images=[f"https://example.com/images/restaurant{i+1}.jpg" for i in range(2)]
            )
            
            restaurants.append(restaurant)
        
        return restaurants
    
    def _generate_mock_transportation(
        self, 
        destination: Location, 
        activities: List[Activity],
        date: date
    ) -> List[Transportation]:
        """
        Generate mock transportation options between activities.
        
        Args:
            destination: Destination location
            activities: List of activities for the day
            date: Day of the trip
            
        Returns:
            List of transportation options
        """
        transportation = []
        
        # Transportation types
        transport_types = ["Taxi", "Public Transport", "Rideshare", "Walking", "Rental Car"]
        
        # If there are activities, create transportation between them
        if activities:
            prev_location = "Hotel"
            
            for activity in activities:
                transport_type = random.choice(transport_types)
                
                # Estimate price based on type
                if transport_type == "Taxi":
                    price = random.uniform(15, 30)
                elif transport_type == "Public Transport":
                    price = random.uniform(1, 5)
                elif transport_type == "Rideshare":
                    price = random.uniform(10, 25)
                elif transport_type == "Walking":
                    price = 0
                else:  # Rental Car
                    price = random.uniform(30, 60)
                
                # Create transportation object
                transport = Transportation(
                    type=transport_type,
                    from_location=prev_location,
                    to_location=activity.name,
                    date=date,
                    time=activity.start_time,
                    price=round(price, 2),
                    booking_url=f"https://example.com/transportation/{uuid.uuid4().hex[:8]}" if transport_type in ["Taxi", "Rideshare", "Rental Car"] else None,
                    details=self._generate_transport_details(transport_type)
                )
                
                transportation.append(transport)
                prev_location = activity.name
            
            # Add return transportation to hotel
            transport_type = random.choice(transport_types)
            
            # Estimate price based on type
            if transport_type == "Taxi":
                price = random.uniform(15, 30)
            elif transport_type == "Public Transport":
                price = random.uniform(1, 5)
            elif transport_type == "Rideshare":
                price = random.uniform(10, 25)
            elif transport_type == "Walking":
                price = 0
            else:  # Rental Car
                price = random.uniform(30, 60)
            
            # Create transportation object
            transport = Transportation(
                type=transport_type,
                from_location=prev_location,
                to_location="Hotel",
                date=date,
                time=None,  # Time depends on the last activity's duration
                price=round(price, 2),
                booking_url=f"https://example.com/transportation/{uuid.uuid4().hex[:8]}" if transport_type in ["Taxi", "Rideshare", "Rental Car"] else None,
                details=self._generate_transport_details(transport_type)
            )
            
            transportation.append(transport)
        
        return transportation
    
    def _generate_transport_details(self, transport_type: str) -> Dict[str, Any]:
        """
        Generate details for a transportation option.
        
        Args:
            transport_type: Type of transportation
            
        Returns:
            Dictionary with transportation details
        """
        details = {}
        
        if transport_type == "Taxi":
            details["company"] = random.choice(["City Taxi", "Metro Cab", "Express Taxi"])
            details["contact"] = f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        elif transport_type == "Public Transport":
            details["line"] = f"Line {random.choice(['A', 'B', 'C', '1', '2', '3'])}"
            details["stops"] = random.randint(2, 6)
            details["frequency"] = f"Every {random.randint(5, 15)} minutes"
        elif transport_type == "Rideshare":
            details["company"] = random.choice(["Uber", "Lyft", "Careem", "Bolt"])
            details["estimated_wait"] = f"{random.randint(3, 10)} minutes"
        elif transport_type == "Walking":
            details["distance"] = f"{random.uniform(0.5, 2.0):.1f} km"
            details["estimated_time"] = f"{random.randint(10, 30)} minutes"
        else:  # Rental Car
            details["company"] = random.choice(["Hertz", "Avis", "Enterprise", "Budget"])
            details["car_type"] = random.choice(["Economy", "Compact", "Mid-size", "SUV", "Luxury"])
            details["pickup_location"] = "Hotel"
        
        return details
    
    def _calculate_total_cost(
        self, 
        flights: List[Flight], 
        accommodation: Optional[Accommodation], 
        daily_itineraries: List[DailyItinerary]
    ) -> float:
        """
        Calculate the total cost of the itinerary.
        
        Args:
            flights: List of flights
            accommodation: Accommodation
            daily_itineraries: List of daily itineraries
            
        Returns:
            Total cost
        """
        total_cost = 0
        
        # Add flight costs
        for flight in flights:
            total_cost += flight.price
        
        # Add accommodation cost
        if accommodation:
            total_cost += accommodation.total_price
        
        # Add activity costs
        for day in daily_itineraries:
            for activity in day.activities:
                total_cost += activity.total_price
            
            # Add transportation costs
            for transport in day.transportation:
                total_cost += transport.price
        
        return round(total_cost, 2)
    
    def _generate_itinerary_notes(self, preferences: UserPreferences, destination: Location) -> str:
        """
        Generate notes for the itinerary.
        
        Args:
            preferences: User preferences
            destination: Selected destination
            
        Returns:
            Notes string
        """
        # Calculate trip duration
        trip_duration = (preferences.end_date - preferences.start_date).days + 1
        
        # Determine travel style description
        travel_style = []
        for style in preferences.travel_style:
            if style == "LUXURY":
                travel_style.append("luxurious")
            elif style == "BUDGET":
                travel_style.append("budget-friendly")
            elif style == "FAMILY":
                travel_style.append("family-oriented")
            elif style == "SOLO":
                travel_style.append("solo traveler")
            elif style == "COUPLE":
                travel_style.append("couple's getaway")
            elif style == "GROUP":
                travel_style.append("group travel")
            elif style == "BUSINESS":
                travel_style.append("business traveler")
        
        # Determine interests description
        interest_list = [i.value for i in preferences.interests]
        
        # Generate notes
        notes = f"This {'-'.join(travel_style)} {trip_duration}-day {destination.city} itinerary focuses on "
        
        if len(interest_list) > 2:
            notes += f"{', '.join(interest_list[:-1])}, and {interest_list[-1]}"
        elif len(interest_list) == 2:
            notes += f"{interest_list[0]} and {interest_list[1]}"
        else:
            notes += f"{interest_list[0]}"
        
        notes += " as requested."
        
        # Add note about Almosafer's value
        if settings.PRIORITIZE_LUXURY and "LUXURY" in [s.value for s in preferences.travel_style]:
            notes += " We've prioritized premium experiences and luxury accommodations to ensure an exceptional journey."
        
        # Add note about pilgrimage if applicable
        if "PILGRIMAGE" in [i.value for i in preferences.interests] and settings.PARTNER_WITH_NUSUK:
            notes += f" As part of our partnership with Nusuk, we've included access to religious sites and activities to enhance your pilgrimage experience with flights from our network of {settings.AIRLINES_COUNT}+ airline partners."
        
        return notes