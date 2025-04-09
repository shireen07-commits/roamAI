"""
Service for flight search and booking.
This is a mock service for demonstration purposes.
"""

import logging
import uuid
import random
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any

from ..models.travel import Flight, UserPreferences, Booking
from ..core.config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FlightService:
    """Mock service for flight search and booking."""
    
    def __init__(self):
        """Initialize the flight service."""
        self.api_url = settings.FLIGHT_API_URL
        # Mock airline data
        self.airlines = [
            {"name": "Emirates", "rating": 5, "is_luxury": True},
            {"name": "Qatar Airways", "rating": 5, "is_luxury": True},
            {"name": "Etihad Airways", "rating": 5, "is_luxury": True},
            {"name": "Singapore Airlines", "rating": 5, "is_luxury": True},
            {"name": "Lufthansa", "rating": 4, "is_luxury": False},
            {"name": "British Airways", "rating": 4, "is_luxury": False},
            {"name": "Air France", "rating": 4, "is_luxury": False},
            {"name": "KLM", "rating": 4, "is_luxury": False},
            {"name": "Delta Airlines", "rating": 3, "is_luxury": False},
            {"name": "American Airlines", "rating": 3, "is_luxury": False},
            {"name": "United Airlines", "rating": 3, "is_luxury": False},
            {"name": "Saudia", "rating": 4, "is_luxury": False},
            {"name": "Turkish Airlines", "rating": 4, "is_luxury": False},
        ]
        # Common airport codes and the cities they serve
        self.airports = {
            "DXB": "Dubai",
            "AUH": "Abu Dhabi",
            "DOH": "Doha",
            "RUH": "Riyadh",
            "JED": "Jeddah",
            "CAI": "Cairo",
            "IST": "Istanbul",
            "LHR": "London",
            "CDG": "Paris",
            "JFK": "New York",
            "LAX": "Los Angeles",
            "SIN": "Singapore",
            "HKG": "Hong Kong",
            "SYD": "Sydney",
            "NRT": "Tokyo",
        }
        # Cabin classes
        self.cabin_classes = ["Economy", "Premium Economy", "Business", "First"]
    
    def search_flights(
        self, 
        origin: str, 
        destination: str, 
        departure_date: datetime, 
        return_date: Optional[datetime] = None,
        passengers: int = 1,
        cabin_class: str = "Economy",
        prioritize_luxury: bool = False
    ) -> List[Flight]:
        """
        Search for flights based on search criteria.
        
        Args:
            origin: Origin city or airport code
            destination: Destination city or airport code
            departure_date: Departure date
            return_date: Return date for round-trip flights (optional)
            passengers: Number of passengers
            cabin_class: Cabin class (Economy, Premium Economy, Business, First)
            prioritize_luxury: Whether to prioritize luxury airlines
            
        Returns:
            List of available flights
        """
        logger.info(f"Searching for flights from {origin} to {destination} on {departure_date}")
        
        # In a real implementation, this would call an external API
        # For now, let's generate mock flight data
        
        flights = []
        
        # Determine airport codes if cities were provided
        origin_code = self._get_airport_code(origin)
        destination_code = self._get_airport_code(destination)
        
        # Get airlines, with luxury prioritized if requested
        available_airlines = self._get_available_airlines(prioritize_luxury)
        
        # Generate outbound flights
        for _ in range(5):  # Generate 5 flight options
            airline_data = random.choice(available_airlines)
            airline = airline_data["name"]
            
            # Generate flight number
            airline_code = "".join([word[0] for word in airline.split()]).upper()
            flight_number = f"{airline_code}{random.randint(100, 999)}"
            
            # Generate times
            flight_duration_minutes = random.randint(180, 720)  # 3 to 12 hours
            departure_time = departure_date + timedelta(hours=random.randint(0, 23), minutes=random.choice([0, 15, 30, 45]))
            arrival_time = departure_time + timedelta(minutes=flight_duration_minutes)
            
            # Generate price based on cabin class and airline luxury status
            base_price = random.uniform(250, 500)  # Base price in USD
            cabin_multiplier = self._get_cabin_price_multiplier(cabin_class)
            luxury_multiplier = 1.5 if airline_data["is_luxury"] else 1.0
            price = base_price * cabin_multiplier * luxury_multiplier * passengers
            
            # Generate baggage allowance
            baggage_allowance = self._generate_baggage_allowance(cabin_class, airline_data["is_luxury"])
            
            # Generate amenities
            amenities = self._generate_amenities(cabin_class, airline_data["is_luxury"])
            
            # Create Flight object
            flight = Flight(
                flight_id=f"FL{uuid.uuid4().hex[:8].upper()}",
                airline=airline,
                flight_number=flight_number,
                departure_airport=origin_code,
                arrival_airport=destination_code,
                departure_time=departure_time,
                arrival_time=arrival_time,
                duration_minutes=flight_duration_minutes,
                stop_count=random.choice([0, 0, 0, 1, 1, 2]),  # Most flights are non-stop
                price=round(price, 2),
                cabin_class=cabin_class,
                available_seats=random.randint(1, 50),
                refundable=random.choice([True, False]),
                booking_url=f"https://example.com/book/flight/{uuid.uuid4().hex[:8]}",
                baggage_allowance=baggage_allowance,
                amenities=amenities
            )
            
            flights.append(flight)
        
        # Sort flights by preference (luxury if prioritized, otherwise price)
        if prioritize_luxury:
            flights.sort(key=lambda f: (-1 if any(a["name"] == f.airline and a["is_luxury"] for a in self.airlines) else 0, f.price))
        else:
            flights.sort(key=lambda f: (f.price, f.stop_count))
        
        return flights
    
    def book_flight(self, flight: Flight, traveler_details: Dict[str, Any]) -> Optional[Booking]:
        """
        Book a flight.
        
        Args:
            flight: Flight to book
            traveler_details: Dictionary with traveler information
            
        Returns:
            Booking information if successful, None otherwise
        """
        logger.info(f"Booking flight {flight.flight_number} with {flight.airline}")
        
        # In a real implementation, this would call an external API
        # For now, let's generate mock booking data
        try:
            # Generate a unique booking reference
            airline_code = "".join([word[0] for word in flight.airline.split()]).upper()
            reference_number = f"{airline_code}{uuid.uuid4().hex[:8].upper()}"
            
            booking = Booking(
                booking_id=f"B{uuid.uuid4().hex[:8].upper()}",
                booking_type="flight",
                provider=flight.airline,
                status="confirmed",
                booking_date=datetime.now(),
                reference_number=reference_number,
                confirmation_email=traveler_details.get("email"),
                payment_details={
                    "amount": flight.price,
                    "currency": "USD",
                    "payment_method": traveler_details.get("payment_method", "Credit Card"),
                    "is_paid": True
                },
                cancellation_policy="Cancellation available up to 24 hours before departure with a 20% fee."
            )
            
            return booking
        except Exception as e:
            logger.error(f"Error booking flight: {e}")
            return None
    
    def _get_airport_code(self, location: str) -> str:
        """
        Get airport code for a location, or return the input if it's already a code.
        
        Args:
            location: City name or airport code
            
        Returns:
            Airport code
        """
        # If input is already a code, return it
        if location in self.airports.keys():
            return location
        
        # Try to find a code for the city
        for code, city in self.airports.items():
            if city.lower() == location.lower():
                return code
        
        # If not found, generate a mock code
        return f"{location[:3].upper()}"
    
    def _get_available_airlines(self, prioritize_luxury: bool) -> List[Dict[str, Any]]:
        """
        Get a list of available airlines, optionally prioritizing luxury ones.
        
        Args:
            prioritize_luxury: Whether to prioritize luxury airlines
            
        Returns:
            List of airline data
        """
        if prioritize_luxury:
            # Put luxury airlines first, then others
            luxury_airlines = [a for a in self.airlines if a["is_luxury"]]
            other_airlines = [a for a in self.airlines if not a["is_luxury"]]
            return luxury_airlines + other_airlines
        return self.airlines
    
    def _get_cabin_price_multiplier(self, cabin_class: str) -> float:
        """
        Get price multiplier for a cabin class.
        
        Args:
            cabin_class: Cabin class name
            
        Returns:
            Price multiplier
        """
        multipliers = {
            "Economy": 1.0,
            "Premium Economy": 1.7,
            "Business": 3.5,
            "First": 6.0
        }
        return multipliers.get(cabin_class, 1.0)
    
    def _generate_baggage_allowance(self, cabin_class: str, is_luxury: bool) -> Dict[str, str]:
        """
        Generate baggage allowance based on cabin class and airline type.
        
        Args:
            cabin_class: Cabin class name
            is_luxury: Whether the airline is considered luxury
            
        Returns:
            Dictionary with baggage allowance details
        """
        baggage_allowance = {}
        
        # Cabin baggage
        if cabin_class in ["Economy", "Premium Economy"]:
            baggage_allowance["cabin"] = "1 x 7kg"
        else:
            baggage_allowance["cabin"] = "2 x 7kg"
        
        # Checked baggage
        if cabin_class == "Economy":
            if is_luxury:
                baggage_allowance["checked"] = "2 x 23kg"
            else:
                baggage_allowance["checked"] = "1 x 23kg"
        elif cabin_class == "Premium Economy":
            baggage_allowance["checked"] = "2 x 23kg"
        elif cabin_class == "Business":
            baggage_allowance["checked"] = "2 x 32kg"
        else:  # First class
            baggage_allowance["checked"] = "3 x 32kg"
        
        return baggage_allowance
    
    def _generate_amenities(self, cabin_class: str, is_luxury: bool) -> List[str]:
        """
        Generate amenities based on cabin class and airline type.
        
        Args:
            cabin_class: Cabin class name
            is_luxury: Whether the airline is considered luxury
            
        Returns:
            List of amenities
        """
        amenities = []
        
        # Common amenities
        if is_luxury or cabin_class in ["Business", "First"]:
            amenities.append("Priority Boarding")
            amenities.append("Lounge Access")
        
        if cabin_class == "Economy":
            amenities.append("Standard Seat")
            if is_luxury:
                amenities.append("Complimentary Meals")
                amenities.append("Personal Entertainment System")
                amenities.append("Wi-Fi (paid)")
        elif cabin_class == "Premium Economy":
            amenities.append("Extra Legroom")
            amenities.append("Complimentary Meals")
            amenities.append("Personal Entertainment System")
            amenities.append("Wi-Fi (paid)")
            amenities.append("Premium Headphones")
        elif cabin_class == "Business":
            amenities.append("Lie-flat Seat" if is_luxury else "Recliner Seat")
            amenities.append("Gourmet Meals")
            amenities.append("Premium Entertainment System")
            amenities.append("Wi-Fi (complimentary)")
            amenities.append("Noise-Cancelling Headphones")
            amenities.append("Amenity Kit")
            if is_luxury:
                amenities.append("Dedicated Cabin Crew")
                amenities.append("Premium Bedding")
        else:  # First class
            amenities.append("Private Suite" if is_luxury else "Lie-flat Seat")
            amenities.append("On-demand Dining")
            amenities.append("Premium Entertainment System")
            amenities.append("Wi-Fi (complimentary)")
            amenities.append("Luxury Amenity Kit")
            amenities.append("Chauffeur Service")
            if is_luxury:
                amenities.append("Shower Facilities (select aircraft)")
                amenities.append("Personal Butler")
        
        return amenities