"""
Service for accommodation search and booking.
This is a mock service for demonstration purposes.
"""

import logging
import uuid
import random
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any

from ..models.travel import Accommodation, Location, UserPreferences, Booking
from ..core.config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AccommodationService:
    """Mock service for accommodation search and booking."""
    
    def __init__(self):
        """Initialize the accommodation service."""
        self.api_url = settings.HOTEL_API_URL
        # Mock hotel chains
        self.hotel_chains = [
            {"name": "Ritz-Carlton", "rating": 5, "is_luxury": True},
            {"name": "Four Seasons", "rating": 5, "is_luxury": True},
            {"name": "St. Regis", "rating": 5, "is_luxury": True},
            {"name": "Waldorf Astoria", "rating": 5, "is_luxury": True},
            {"name": "Mandarin Oriental", "rating": 5, "is_luxury": True},
            {"name": "Marriott", "rating": 4, "is_luxury": False},
            {"name": "Hilton", "rating": 4, "is_luxury": False},
            {"name": "Hyatt", "rating": 4, "is_luxury": False},
            {"name": "InterContinental", "rating": 4, "is_luxury": False},
            {"name": "Sheraton", "rating": 3.5, "is_luxury": False},
            {"name": "Holiday Inn", "rating": 3, "is_luxury": False},
            {"name": "Ibis", "rating": 2.5, "is_luxury": False},
        ]
        # Hotel types
        self.hotel_types = ["Hotel", "Resort", "Boutique Hotel", "Apartment", "Villa"]
        # Room types by luxury level
        self.room_types = {
            "luxury": ["Presidential Suite", "Royal Suite", "Executive Suite", "Luxury Suite", "Penthouse"],
            "moderate": ["Junior Suite", "Deluxe Room", "Executive Room", "Premium Room"],
            "budget": ["Standard Room", "Economy Room", "Twin Room", "Single Room"]
        }
        # Common amenities by hotel rating
        self.amenities = {
            5: ["Swimming Pool", "Spa", "Fitness Center", "Multiple Restaurants", "Concierge", "Room Service", 
                "Business Center", "Valet Parking", "Airport Transfer", "Butler Service", "Private Beach"],
            4: ["Swimming Pool", "Spa", "Fitness Center", "Restaurant", "Concierge", "Room Service", 
                "Business Center", "Parking"],
            3: ["Restaurant", "Fitness Center", "Parking", "Wi-Fi"],
            2: ["Wi-Fi", "Breakfast", "Parking"]
        }
    
    def search_accommodations(
        self, 
        destination: Location, 
        check_in_date: date, 
        check_out_date: date,
        guests: int = 2,
        room_count: int = 1,
        min_rating: float = 0,
        max_price: Optional[float] = None,
        amenities: Optional[List[str]] = None,
        prioritize_luxury: bool = False
    ) -> List[Accommodation]:
        """
        Search for accommodations based on search criteria.
        
        Args:
            destination: Destination location
            check_in_date: Check-in date
            check_out_date: Check-out date
            guests: Number of guests
            room_count: Number of rooms
            min_rating: Minimum rating (0-5)
            max_price: Maximum price per night
            amenities: Required amenities
            prioritize_luxury: Whether to prioritize luxury accommodations
            
        Returns:
            List of available accommodations
        """
        logger.info(f"Searching for accommodations in {destination.city} from {check_in_date} to {check_out_date}")
        
        # In a real implementation, this would call an external API
        # For now, let's generate mock accommodation data
        
        accommodations = []
        
        # Get available hotel chains, with luxury prioritized if requested
        available_chains = self._get_available_chains(prioritize_luxury)
        
        # Generate accommodations
        for _ in range(8):  # Generate 8 accommodation options
            chain_data = random.choice(available_chains)
            chain = chain_data["name"]
            rating = chain_data["rating"]
            is_luxury = chain_data["is_luxury"]
            
            # Generate hotel type
            if is_luxury:
                hotel_type = random.choice(self.hotel_types[:3])  # Luxury hotels are usually hotels or resorts
            else:
                hotel_type = random.choice(self.hotel_types)
            
            # Generate hotel name
            hotel_name = f"{chain} {destination.city} {hotel_type if hotel_type != 'Hotel' else ''}"
            hotel_name = hotel_name.strip()
            
            # Generate room type based on luxury level
            if is_luxury:
                room_type = random.choice(self.room_types["luxury"])
            elif rating >= 4:
                room_type = random.choice(self.room_types["moderate"])
            else:
                room_type = random.choice(self.room_types["budget"])
            
            # Generate price based on rating, luxury status, and room type
            base_price = random.uniform(50, 150)  # Base price in USD
            rating_multiplier = rating / 2.5  # 5-star is 2x the base price
            luxury_multiplier = 2.0 if is_luxury else 1.0
            room_multiplier = 1.0
            if room_type in self.room_types["luxury"]:
                room_multiplier = 2.5
            elif room_type in self.room_types["moderate"]:
                room_multiplier = 1.5
            
            price_per_night = base_price * rating_multiplier * luxury_multiplier * room_multiplier
            
            # Apply max price filter if specified
            if max_price and price_per_night > max_price:
                continue
            
            # Calculate total price for the stay
            stay_duration = (check_out_date - check_in_date).days
            total_price = price_per_night * stay_duration * room_count
            
            # Generate amenities based on rating
            available_amenities = self.amenities.get(int(rating), [])
            if amenities:
                # Skip this accommodation if it doesn't have all required amenities
                if not all(a in available_amenities for a in amenities):
                    continue
            
            # Generate mock location within the destination city
            location = Location(
                city=destination.city,
                country=destination.country,
                region=destination.region,
                latitude=destination.latitude + random.uniform(-0.05, 0.05) if destination.latitude else None,
                longitude=destination.longitude + random.uniform(-0.05, 0.05) if destination.longitude else None
            )
            
            # Create Accommodation object
            accommodation = Accommodation(
                accommodation_id=f"H{uuid.uuid4().hex[:8].upper()}",
                name=hotel_name,
                type=hotel_type.lower(),
                location=location,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                rating=rating,
                price_per_night=round(price_per_night, 2),
                total_price=round(total_price, 2),
                amenities=available_amenities,
                room_type=room_type,
                refundable=random.choice([True, False]),
                booking_url=f"https://example.com/book/hotel/{uuid.uuid4().hex[:8]}",
                images=[f"https://example.com/images/hotel{i+1}.jpg" for i in range(3)]
            )
            
            accommodations.append(accommodation)
        
        # Sort accommodations by preference (rating if prioritize_luxury, otherwise price)
        if prioritize_luxury:
            accommodations.sort(key=lambda a: (-a.rating, a.price_per_night))
        else:
            accommodations.sort(key=lambda a: (a.price_per_night, -a.rating))
        
        return accommodations
    
    def book_accommodation(self, accommodation: Accommodation, guest_details: Dict[str, Any]) -> Optional[Booking]:
        """
        Book an accommodation.
        
        Args:
            accommodation: Accommodation to book
            guest_details: Dictionary with guest information
            
        Returns:
            Booking information if successful, None otherwise
        """
        logger.info(f"Booking accommodation at {accommodation.name}")
        
        # In a real implementation, this would call an external API
        # For now, let's generate mock booking data
        try:
            # Generate a unique booking reference
            hotel_code = "".join([word[0] for word in accommodation.name.split()[:2]]).upper()
            reference_number = f"{hotel_code}{uuid.uuid4().hex[:8].upper()}"
            
            booking = Booking(
                booking_id=f"B{uuid.uuid4().hex[:8].upper()}",
                booking_type="accommodation",
                provider=accommodation.name,
                status="confirmed",
                booking_date=datetime.now(),
                reference_number=reference_number,
                confirmation_email=guest_details.get("email"),
                payment_details={
                    "amount": accommodation.total_price,
                    "currency": "USD",
                    "payment_method": guest_details.get("payment_method", "Credit Card"),
                    "is_paid": True
                },
                cancellation_policy="Free cancellation up to 24 hours before check-in." if accommodation.refundable else "Non-refundable booking."
            )
            
            return booking
        except Exception as e:
            logger.error(f"Error booking accommodation: {e}")
            return None
    
    def _get_available_chains(self, prioritize_luxury: bool) -> List[Dict[str, Any]]:
        """
        Get a list of available hotel chains, optionally prioritizing luxury ones.
        
        Args:
            prioritize_luxury: Whether to prioritize luxury hotel chains
            
        Returns:
            List of hotel chain data
        """
        if prioritize_luxury:
            # Put luxury chains first, then others
            luxury_chains = [c for c in self.hotel_chains if c["is_luxury"]]
            other_chains = [c for c in self.hotel_chains if not c["is_luxury"]]
            return luxury_chains + other_chains
        return self.hotel_chains