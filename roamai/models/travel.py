"""
Travel-related data models.
"""

from enum import Enum
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr


class TravelStyle(str, Enum):
    """Travel style options."""
    
    LUXURY = "luxury"
    BUDGET = "budget"
    FAMILY = "family"
    SOLO = "solo"
    COUPLE = "couple"
    GROUP = "group"
    BUSINESS = "business"


class TravelInterest(str, Enum):
    """Travel interest options."""
    
    ADVENTURE = "adventure"
    RELAXATION = "relaxation"
    CULTURE = "culture"
    FOOD = "food"
    SHOPPING = "shopping"
    NATURE = "nature"
    BEACH = "beach"
    PILGRIMAGE = "pilgrimage"
    SIGHTSEEING = "sightseeing"
    HISTORY = "history"


class UserPreferences(BaseModel):
    """User travel preferences."""
    
    destination: Optional[str] = None
    budget: float = Field(..., gt=0)
    start_date: date
    end_date: date
    travelers: int = Field(1, gt=0)
    travel_style: List[TravelStyle]
    interests: List[TravelInterest]
    is_flexible_dates: bool = False
    is_flexible_destination: bool = False
    previous_destinations: Optional[List[str]] = None
    special_requirements: Optional[str] = None
    
    class Config:
        """Pydantic config."""
        
        schema_extra = {
            "example": {
                "destination": "Dubai",
                "budget": 5000,
                "start_date": "2024-05-15",
                "end_date": "2024-05-20",
                "travelers": 2,
                "travel_style": ["LUXURY"],
                "interests": ["FOOD", "SHOPPING", "CULTURE"],
                "is_flexible_dates": False,
                "is_flexible_destination": False,
                "special_requirements": "We prefer hotels with spa facilities"
            }
        }


class Location(BaseModel):
    """Location model."""
    
    city: str
    country: str
    region: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class Flight(BaseModel):
    """Flight model."""
    
    flight_id: str
    airline: str
    flight_number: str
    departure_airport: str
    arrival_airport: str
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int
    stop_count: int = 0
    price: float
    cabin_class: str
    available_seats: int
    refundable: bool = False
    booking_url: Optional[str] = None
    baggage_allowance: Optional[Dict[str, Any]] = None
    amenities: Optional[List[str]] = None
    
    class Config:
        """Pydantic config."""
        
        schema_extra = {
            "example": {
                "flight_id": "FL123456",
                "airline": "Emirates",
                "flight_number": "EK502",
                "departure_airport": "JFK",
                "arrival_airport": "DXB",
                "departure_time": "2024-05-15T08:30:00Z",
                "arrival_time": "2024-05-16T05:15:00Z",
                "duration_minutes": 825,
                "stop_count": 0,
                "price": 1250.50,
                "cabin_class": "Business",
                "available_seats": 12,
                "refundable": True,
                "booking_url": "https://example.com/book/FL123456",
                "baggage_allowance": {
                    "checked": "2 x 23kg",
                    "cabin": "1 x 7kg"
                },
                "amenities": ["Wi-Fi", "Lie-flat seats", "Gourmet meals"]
            }
        }


class Accommodation(BaseModel):
    """Accommodation model."""
    
    accommodation_id: str
    name: str
    type: str  # hotel, resort, apartment, etc.
    location: Location
    check_in_date: date
    check_out_date: date
    rating: float = Field(None, ge=0, le=5)
    price_per_night: float
    total_price: float
    amenities: List[str] = []
    room_type: str
    refundable: bool = False
    booking_url: Optional[str] = None
    images: Optional[List[str]] = None
    
    class Config:
        """Pydantic config."""
        
        schema_extra = {
            "example": {
                "accommodation_id": "H123456",
                "name": "Burj Al Arab Jumeirah",
                "type": "luxury hotel",
                "location": {
                    "city": "Dubai", 
                    "country": "United Arab Emirates",
                    "latitude": 25.141127,
                    "longitude": 55.185550
                },
                "check_in_date": "2024-05-15",
                "check_out_date": "2024-05-20",
                "rating": 5.0,
                "price_per_night": 1200.00,
                "total_price": 6000.00,
                "amenities": ["Spa", "Private Beach", "Multiple Restaurants", "Butler Service"],
                "room_type": "Deluxe Suite",
                "refundable": True,
                "booking_url": "https://example.com/book/H123456",
                "images": [
                    "https://example.com/images/burj1.jpg",
                    "https://example.com/images/burj2.jpg"
                ]
            }
        }


class Activity(BaseModel):
    """Travel activity model."""
    
    activity_id: str
    name: str
    description: str
    location: Location
    date: date
    start_time: Optional[str] = None
    duration_minutes: Optional[int] = None
    price_per_person: float
    total_price: float
    booking_url: Optional[str] = None
    category: List[str] = []
    images: Optional[List[str]] = None
    
    class Config:
        """Pydantic config."""
        
        schema_extra = {
            "example": {
                "activity_id": "A123456",
                "name": "Desert Safari with BBQ Dinner",
                "description": "Experience an exciting desert adventure with dune bashing followed by a BBQ dinner under the stars with traditional entertainment.",
                "location": {
                    "city": "Dubai", 
                    "country": "United Arab Emirates"
                },
                "date": "2024-05-16",
                "start_time": "15:30",
                "duration_minutes": 360,
                "price_per_person": 85.00,
                "total_price": 170.00,
                "booking_url": "https://example.com/book/A123456",
                "category": ["Adventure", "Cultural", "Food"],
                "images": [
                    "https://example.com/images/desert1.jpg",
                    "https://example.com/images/desert2.jpg"
                ]
            }
        }


class Restaurant(BaseModel):
    """Restaurant recommendation model."""
    
    restaurant_id: str
    name: str
    description: str
    location: Location
    cuisine: List[str]
    price_range: str  # $, $$, $$$, $$$$
    rating: float = Field(None, ge=0, le=5)
    reservation_url: Optional[str] = None
    opening_hours: Optional[Dict[str, str]] = None
    images: Optional[List[str]] = None
    
    class Config:
        """Pydantic config."""
        
        schema_extra = {
            "example": {
                "restaurant_id": "R123456",
                "name": "Al Mahara",
                "description": "Luxury seafood restaurant with a large aquarium centerpiece, located in the Burj Al Arab hotel.",
                "location": {
                    "city": "Dubai", 
                    "country": "United Arab Emirates"
                },
                "cuisine": ["Seafood", "Fine Dining"],
                "price_range": "$$$$",
                "rating": 4.8,
                "reservation_url": "https://example.com/reserve/R123456",
                "opening_hours": {
                    "Monday": "18:30-23:00",
                    "Tuesday": "18:30-23:00",
                    "Wednesday": "18:30-23:00",
                    "Thursday": "18:30-23:00",
                    "Friday": "12:30-15:00, 18:30-23:00",
                    "Saturday": "12:30-15:00, 18:30-23:00",
                    "Sunday": "12:30-15:00, 18:30-23:00"
                },
                "images": [
                    "https://example.com/images/almahara1.jpg",
                    "https://example.com/images/almahara2.jpg"
                ]
            }
        }


class Transportation(BaseModel):
    """Local transportation model."""
    
    type: str  # taxi, public transport, rental car, etc.
    from_location: str
    to_location: str
    date: date
    time: Optional[str] = None
    price: float
    booking_url: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class DailyItinerary(BaseModel):
    """Daily itinerary model."""
    
    date: date
    day_number: int
    activities: List[Activity] = []
    restaurants: List[Restaurant] = []
    transportation: List[Transportation] = []
    notes: Optional[str] = None
    
    class Config:
        """Pydantic config."""
        
        schema_extra = {
            "example": {
                "date": "2024-05-16",
                "day_number": 2,
                "activities": [
                    {
                        "activity_id": "A123456",
                        "name": "Desert Safari with BBQ Dinner",
                        "description": "Experience an exciting desert adventure with dune bashing followed by a BBQ dinner under the stars with traditional entertainment.",
                        "location": {
                            "city": "Dubai", 
                            "country": "United Arab Emirates"
                        },
                        "date": "2024-05-16",
                        "start_time": "15:30",
                        "duration_minutes": 360,
                        "price_per_person": 85.00,
                        "total_price": 170.00,
                        "category": ["Adventure", "Cultural", "Food"]
                    }
                ],
                "restaurants": [
                    {
                        "restaurant_id": "R123457",
                        "name": "Arabian Tea House",
                        "description": "Traditional Emirati cuisine in a charming heritage setting.",
                        "location": {
                            "city": "Dubai", 
                            "country": "United Arab Emirates"
                        },
                        "cuisine": ["Emirati", "Middle Eastern"],
                        "price_range": "$$",
                        "rating": 4.6
                    }
                ],
                "transportation": [
                    {
                        "type": "Taxi",
                        "from_location": "Hotel",
                        "to_location": "Desert Safari Meeting Point",
                        "date": "2024-05-16",
                        "time": "15:00",
                        "price": 25.00
                    }
                ],
                "notes": "Wear comfortable clothes and bring a light jacket for the evening as temperatures drop in the desert."
            }
        }


class Booking(BaseModel):
    """Booking information model."""
    
    booking_id: str
    booking_type: str  # flight, accommodation, activity, etc.
    provider: str
    status: str  # confirmed, pending, cancelled
    booking_date: datetime
    reference_number: str
    confirmation_email: Optional[EmailStr] = None
    payment_details: Optional[Dict[str, Any]] = None
    cancellation_policy: Optional[str] = None
    
    class Config:
        """Pydantic config."""
        
        schema_extra = {
            "example": {
                "booking_id": "B123456",
                "booking_type": "flight",
                "provider": "Emirates",
                "status": "confirmed",
                "booking_date": "2024-04-15T14:30:00Z",
                "reference_number": "EK12345678",
                "confirmation_email": "user@example.com",
                "payment_details": {
                    "amount": 1250.50,
                    "currency": "USD",
                    "payment_method": "Credit Card",
                    "is_paid": True
                },
                "cancellation_policy": "Cancellation available up to 24 hours before departure with a 20% fee."
            }
        }


class TravelItinerary(BaseModel):
    """Complete travel itinerary model."""
    
    itinerary_id: str
    user_preferences: UserPreferences
    destination: Location
    start_date: date
    end_date: date
    flights: List[Flight] = []
    accommodation: Optional[Accommodation] = None
    daily_itineraries: List[DailyItinerary] = []
    bookings: List[Booking] = []
    total_cost: float
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        """Pydantic config."""
        
        schema_extra = {
            "example": {
                "itinerary_id": "ITN123456",
                "user_preferences": {
                    "destination": "Dubai",
                    "budget": 5000,
                    "start_date": "2024-05-15",
                    "end_date": "2024-05-20",
                    "travelers": 2,
                    "travel_style": ["LUXURY"],
                    "interests": ["FOOD", "SHOPPING", "CULTURE"],
                    "is_flexible_dates": False,
                    "is_flexible_destination": False,
                    "special_requirements": "We prefer hotels with spa facilities"
                },
                "destination": {
                    "city": "Dubai", 
                    "country": "United Arab Emirates",
                    "region": "Middle East"
                },
                "start_date": "2024-05-15",
                "end_date": "2024-05-20",
                "flights": [
                    {
                        "flight_id": "FL123456",
                        "airline": "Emirates",
                        "flight_number": "EK502",
                        "departure_airport": "JFK",
                        "arrival_airport": "DXB",
                        "departure_time": "2024-05-15T08:30:00Z",
                        "arrival_time": "2024-05-16T05:15:00Z",
                        "duration_minutes": 825,
                        "stop_count": 0,
                        "price": 1250.50,
                        "cabin_class": "Business",
                        "available_seats": 12,
                        "refundable": True
                    }
                ],
                "accommodation": {
                    "accommodation_id": "H123456",
                    "name": "Burj Al Arab Jumeirah",
                    "type": "luxury hotel",
                    "location": {
                        "city": "Dubai", 
                        "country": "United Arab Emirates"
                    },
                    "check_in_date": "2024-05-15",
                    "check_out_date": "2024-05-20",
                    "rating": 5.0,
                    "price_per_night": 1200.00,
                    "total_price": 6000.00,
                    "amenities": ["Spa", "Private Beach", "Multiple Restaurants", "Butler Service"],
                    "room_type": "Deluxe Suite",
                    "refundable": True
                },
                "daily_itineraries": [
                    {
                        "date": "2024-05-16",
                        "day_number": 2,
                        "activities": [
                            {
                                "activity_id": "A123456",
                                "name": "Desert Safari with BBQ Dinner",
                                "description": "Experience an exciting desert adventure with dune bashing followed by a BBQ dinner under the stars with traditional entertainment.",
                                "location": {
                                    "city": "Dubai", 
                                    "country": "United Arab Emirates"
                                },
                                "date": "2024-05-16",
                                "start_time": "15:30",
                                "duration_minutes": 360,
                                "price_per_person": 85.00,
                                "total_price": 170.00,
                                "category": ["Adventure", "Cultural", "Food"]
                            }
                        ],
                        "restaurants": [
                            {
                                "restaurant_id": "R123457",
                                "name": "Arabian Tea House",
                                "description": "Traditional Emirati cuisine in a charming heritage setting.",
                                "location": {
                                    "city": "Dubai", 
                                    "country": "United Arab Emirates"
                                },
                                "cuisine": ["Emirati", "Middle Eastern"],
                                "price_range": "$$",
                                "rating": 4.6
                            }
                        ],
                        "notes": "Wear comfortable clothes and bring a light jacket for the evening."
                    }
                ],
                "bookings": [
                    {
                        "booking_id": "B123456",
                        "booking_type": "flight",
                        "provider": "Emirates",
                        "status": "confirmed",
                        "booking_date": "2024-04-15T14:30:00Z",
                        "reference_number": "EK12345678"
                    }
                ],
                "total_cost": 4850.50,
                "notes": "This luxurious 5-day Dubai itinerary focuses on fine dining, shopping, and cultural experiences as requested.",
                "created_at": "2024-04-10T12:00:00Z",
                "modified_at": "2024-04-12T15:30:00Z"
            }
        }