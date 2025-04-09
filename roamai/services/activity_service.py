"""
Service for activity search and booking.
This is a mock service for demonstration purposes.
"""

import logging
import uuid
import random
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any

from ..models.travel import Activity, Location, UserPreferences, TravelInterest, Booking
from ..core.config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ActivityService:
    """Mock service for activity search and booking."""
    
    def __init__(self):
        """Initialize the activity service."""
        # Map of travel interests to activity categories
        self.interest_to_category = {
            TravelInterest.ADVENTURE: ["Adventure", "Outdoor", "Sports", "Adrenaline"],
            TravelInterest.RELAXATION: ["Spa", "Wellness", "Beach", "Nature"],
            TravelInterest.CULTURE: ["Museum", "Art", "History", "Cultural", "Heritage"],
            TravelInterest.FOOD: ["Food", "Culinary", "Cooking Class", "Wine Tasting", "Food Tour"],
            TravelInterest.SHOPPING: ["Shopping", "Market", "Mall", "Boutique"],
            TravelInterest.NATURE: ["Nature", "Park", "Wildlife", "Garden", "Hiking"],
            TravelInterest.BEACH: ["Beach", "Water Sports", "Snorkeling", "Diving", "Surfing"],
            TravelInterest.PILGRIMAGE: ["Religious", "Spiritual", "Pilgrimage", "Temple", "Mosque", "Church"],
            TravelInterest.SIGHTSEEING: ["Sightseeing", "Tour", "Landmark", "Attraction"],
            TravelInterest.HISTORY: ["History", "Archaeology", "Monument", "Heritage"]
        }
        
        # Mock activities by region and category
        self.activity_templates = {
            "Middle East": {
                "Adventure": [
                    {"name": "Desert Safari", "description": "Experience an exciting desert adventure with dune bashing followed by a BBQ dinner under the stars with traditional entertainment.", "duration_minutes": 360, "base_price": 85},
                    {"name": "Sandboarding Adventure", "description": "Ride the desert sand dunes on a sandboard, similar to snowboarding but on sand.", "duration_minutes": 240, "base_price": 65},
                    {"name": "Hot Air Balloon Desert Ride", "description": "Soar above the desert landscape in a hot air balloon for stunning views of the sunrise.", "duration_minutes": 180, "base_price": 200}
                ],
                "Cultural": [
                    {"name": "Old City Walking Tour", "description": "Explore the historic districts with a knowledgeable guide sharing insights on the architecture, history, and culture.", "duration_minutes": 180, "base_price": 50},
                    {"name": "Traditional Craft Workshop", "description": "Learn traditional crafts from local artisans, such as calligraphy, pottery, or textile weaving.", "duration_minutes": 120, "base_price": 60},
                    {"name": "Evening Cultural Show", "description": "Enjoy traditional music, dance performances, and cuisine in an authentic setting.", "duration_minutes": 180, "base_price": 70}
                ],
                "Food": [
                    {"name": "Street Food Tour", "description": "Taste a variety of local street foods with a culinary expert guiding you through the best vendors and dishes.", "duration_minutes": 210, "base_price": 75},
                    {"name": "Cooking Class", "description": "Learn to prepare traditional dishes with a local chef, followed by enjoying the meal you've created.", "duration_minutes": 180, "base_price": 90},
                    {"name": "Dinner Cruise", "description": "Enjoy a luxurious dinner while cruising along the coast or river, taking in the night views of the city.", "duration_minutes": 180, "base_price": 110}
                ],
                "Religious": [
                    {"name": "Sacred Sites Tour", "description": "Visit important religious sites with a knowledgeable guide explaining their significance and history.", "duration_minutes": 240, "base_price": 60},
                    {"name": "Spiritual Meditation Session", "description": "Participate in a guided meditation session at a significant spiritual location.", "duration_minutes": 120, "base_price": 45},
                    {"name": "Religious Festival Experience", "description": "Witness or participate in a traditional religious festival or ceremony, learning about its cultural significance.", "duration_minutes": 180, "base_price": 55}
                ]
            },
            "Europe": {
                "Adventure": [
                    {"name": "Mountain Biking Tour", "description": "Navigate scenic mountain trails with a guide, suitable for various skill levels.", "duration_minutes": 240, "base_price": 70},
                    {"name": "Zipline Adventure", "description": "Experience the thrill of ziplining across valleys with stunning views of the landscape.", "duration_minutes": 180, "base_price": 85},
                    {"name": "Kayaking Expedition", "description": "Paddle through rivers or coastal waters, exploring hidden spots accessible only by water.", "duration_minutes": 210, "base_price": 75}
                ],
                "Cultural": [
                    {"name": "Museum Private Tour", "description": "Enjoy a private tour of a prestigious museum with an art historian or curator.", "duration_minutes": 150, "base_price": 90},
                    {"name": "Historical Walking Tour", "description": "Walk through historical districts with a historian sharing insights and stories about significant events and places.", "duration_minutes": 180, "base_price": 50},
                    {"name": "Opera or Classical Concert", "description": "Attend a world-class opera or classical music performance in a historic venue.", "duration_minutes": 180, "base_price": 120}
                ],
                "Food": [
                    {"name": "Wine Tasting Tour", "description": "Visit vineyards or wine cellars, learning about wine production and tasting various local wines.", "duration_minutes": 240, "base_price": 95},
                    {"name": "Gourmet Food Tour", "description": "Sample delicacies at high-end food shops, markets, and eateries with a culinary expert.", "duration_minutes": 210, "base_price": 85},
                    {"name": "Farm-to-Table Experience", "description": "Visit a local farm, help harvest ingredients, and enjoy a meal prepared with fresh produce.", "duration_minutes": 300, "base_price": 110}
                ]
            },
            "Asia": {
                "Adventure": [
                    {"name": "Jungle Trekking", "description": "Hike through lush rainforests with a guide pointing out wildlife and unique plants.", "duration_minutes": 300, "base_price": 65},
                    {"name": "Island Hopping Tour", "description": "Visit multiple islands by boat, with opportunities for swimming, snorkeling, and beach relaxation.", "duration_minutes": 360, "base_price": 80},
                    {"name": "White Water Rafting", "description": "Navigate rushing river rapids with a team and experienced guide.", "duration_minutes": 240, "base_price": 75}
                ],
                "Cultural": [
                    {"name": "Temple Tour", "description": "Visit ancient temples with a guide explaining their historical and religious significance.", "duration_minutes": 240, "base_price": 55},
                    {"name": "Traditional Dance Lesson", "description": "Learn the basics of a traditional dance form from a professional dancer.", "duration_minutes": 120, "base_price": 50},
                    {"name": "Tea Ceremony Experience", "description": "Participate in a traditional tea ceremony, learning about its cultural importance and techniques.", "duration_minutes": 90, "base_price": 60}
                ],
                "Food": [
                    {"name": "Night Market Food Tour", "description": "Explore vibrant night markets with a guide helping you discover the best local dishes.", "duration_minutes": 180, "base_price": 65},
                    {"name": "Asian Cooking Class", "description": "Learn to prepare authentic dishes with a local chef, including a visit to a market to select ingredients.", "duration_minutes": 240, "base_price": 80},
                    {"name": "Street Food Breakfast Tour", "description": "Start your day sampling traditional breakfast dishes from street vendors and local cafes.", "duration_minutes": 150, "base_price": 55}
                ]
            },
            "North America": {
                "Adventure": [
                    {"name": "Helicopter Tour", "description": "See breathtaking views from above with a helicopter tour over natural or urban landscapes.", "duration_minutes": 60, "base_price": 250},
                    {"name": "Wildlife Safari", "description": "Spot native wildlife in their natural habitats with a naturalist guide.", "duration_minutes": 240, "base_price": 85},
                    {"name": "Rock Climbing Experience", "description": "Try rock climbing with professional instructors and equipment on natural formations or indoor walls.", "duration_minutes": 180, "base_price": 70}
                ],
                "Cultural": [
                    {"name": "Broadway Show", "description": "Attend a world-famous Broadway musical or play in New York City.", "duration_minutes": 150, "base_price": 150},
                    {"name": "Native American Heritage Tour", "description": "Learn about indigenous cultures, traditions, and history from native guides.", "duration_minutes": 210, "base_price": 65},
                    {"name": "Jazz Club Evening", "description": "Enjoy live jazz performances in a historic or renowned venue with dinner or drinks.", "duration_minutes": 180, "base_price": 90}
                ],
                "Food": [
                    {"name": "Food Truck Tour", "description": "Sample a variety of cuisines from popular food trucks with a culinary guide.", "duration_minutes": 180, "base_price": 70},
                    {"name": "Craft Beer Tasting", "description": "Visit microbreweries and sample a range of craft beers with explanations about brewing techniques.", "duration_minutes": 210, "base_price": 75},
                    {"name": "Farm-to-Table Dinner", "description": "Enjoy a multi-course meal prepared with locally sourced ingredients, often at a farm or garden setting.", "duration_minutes": 180, "base_price": 120}
                ]
            }
        }
    
    def search_activities(
        self, 
        destination: Location, 
        date: date,
        interests: List[TravelInterest],
        travelers: int = 2,
        max_price_per_person: Optional[float] = None,
        duration_range: Optional[tuple] = None,  # (min_minutes, max_minutes)
    ) -> List[Activity]:
        """
        Search for activities based on search criteria.
        
        Args:
            destination: Destination location
            date: Activity date
            interests: Travel interests
            travelers: Number of travelers
            max_price_per_person: Maximum price per person
            duration_range: Acceptable duration range in minutes
            
        Returns:
            List of available activities
        """
        logger.info(f"Searching for activities in {destination.city} on {date}")
        
        activities = []
        
        # Determine the region for the destination
        region = destination.region if destination.region else self._get_region_for_country(destination.country)
        
        # Get categories based on interests
        categories = []
        for interest in interests:
            categories.extend(self.interest_to_category.get(interest, []))
        
        # Remove duplicates
        categories = list(set(categories))
        
        # Get activity templates for the region
        region_templates = self.activity_templates.get(region, {})
        if not region_templates:
            # If no templates for the specific region, use a random region
            region_templates = random.choice(list(self.activity_templates.values()))
        
        # Generate activities
        for category in categories:
            # Find matching category in templates
            matching_templates = []
            for template_category, templates in region_templates.items():
                if category in template_category or template_category in category:
                    matching_templates.extend(templates)
            
            if not matching_templates:
                # If no exact match, use a random category's templates
                matching_templates = random.choice(list(region_templates.values()))
            
            # Generate 1-3 activities per category
            for _ in range(random.randint(1, 3)):
                template = random.choice(matching_templates)
                
                # Generate time
                start_hour = random.randint(9, 17)
                start_minute = random.choice([0, 15, 30, 45])
                start_time = f"{start_hour:02d}:{start_minute:02d}"
                
                # Adjust duration if duration_range is specified
                duration_minutes = template["duration_minutes"]
                if duration_range:
                    min_minutes, max_minutes = duration_range
                    if duration_minutes < min_minutes:
                        duration_minutes = min_minutes
                    elif duration_minutes > max_minutes:
                        duration_minutes = max_minutes
                
                # Calculate price
                price_per_person = template["base_price"] * (1 + random.uniform(-0.1, 0.1))  # +/- 10% variation
                total_price = price_per_person * travelers
                
                # Skip if over max price
                if max_price_per_person and price_per_person > max_price_per_person:
                    continue
                
                # Create Activity object
                activity = Activity(
                    activity_id=f"A{uuid.uuid4().hex[:8].upper()}",
                    name=template["name"],
                    description=template["description"],
                    location=destination,
                    date=date,
                    start_time=start_time,
                    duration_minutes=duration_minutes,
                    price_per_person=round(price_per_person, 2),
                    total_price=round(total_price, 2),
                    booking_url=f"https://example.com/book/activity/{uuid.uuid4().hex[:8]}",
                    category=[category],
                    images=[f"https://example.com/images/activity{i+1}.jpg" for i in range(2)]
                )
                
                activities.append(activity)
        
        # Sort activities by price
        activities.sort(key=lambda a: a.price_per_person)
        
        return activities
    
    def book_activity(self, activity: Activity, traveler_details: Dict[str, Any]) -> Optional[Booking]:
        """
        Book an activity.
        
        Args:
            activity: Activity to book
            traveler_details: Dictionary with traveler information
            
        Returns:
            Booking information if successful, None otherwise
        """
        logger.info(f"Booking activity: {activity.name}")
        
        # In a real implementation, this would call an external API
        # For now, let's generate mock booking data
        try:
            # Generate a unique booking reference
            activity_code = "".join([word[0] for word in activity.name.split()[:2]]).upper()
            reference_number = f"{activity_code}{uuid.uuid4().hex[:8].upper()}"
            
            booking = Booking(
                booking_id=f"B{uuid.uuid4().hex[:8].upper()}",
                booking_type="activity",
                provider=f"{activity.name} Provider",
                status="confirmed",
                booking_date=datetime.now(),
                reference_number=reference_number,
                confirmation_email=traveler_details.get("email"),
                payment_details={
                    "amount": activity.total_price,
                    "currency": "USD",
                    "payment_method": traveler_details.get("payment_method", "Credit Card"),
                    "is_paid": True
                },
                cancellation_policy="Free cancellation up to 24 hours before the activity."
            )
            
            return booking
        except Exception as e:
            logger.error(f"Error booking activity: {e}")
            return None
    
    def _get_region_for_country(self, country: str) -> str:
        """
        Get the region for a country.
        
        Args:
            country: Country name
            
        Returns:
            Region name
        """
        middle_east_countries = ["Saudi Arabia", "United Arab Emirates", "Qatar", "Bahrain", "Kuwait", "Oman", "Jordan", "Lebanon", "Israel"]
        europe_countries = ["United Kingdom", "France", "Germany", "Italy", "Spain", "Portugal", "Greece", "Switzerland", "Austria", "Netherlands", "Belgium", "Sweden", "Norway", "Denmark", "Finland"]
        asia_countries = ["Japan", "China", "Thailand", "Vietnam", "Singapore", "Indonesia", "Malaysia", "South Korea", "India", "Philippines", "Sri Lanka", "Maldives"]
        north_america_countries = ["United States", "Canada", "Mexico"]
        
        if country in middle_east_countries:
            return "Middle East"
        elif country in europe_countries:
            return "Europe"
        elif country in asia_countries:
            return "Asia"
        elif country in north_america_countries:
            return "North America"
        else:
            # Default to a random region
            return random.choice(["Middle East", "Europe", "Asia", "North America"])