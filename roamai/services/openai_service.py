"""
Service for interacting with OpenAI API.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Union

import openai
from openai import OpenAI
from pydantic import ValidationError

from ..core.config import settings
from ..models.travel import UserPreferences, TravelItinerary, Location

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIService:
    """Service for interacting with OpenAI API."""
    
    def __init__(self):
        """Initialize the OpenAI service."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.DEFAULT_MODEL
    
    def generate_travel_recommendations(
        self, 
        preferences: UserPreferences
    ) -> List[Location]:
        """
        Generate destination recommendations based on user preferences.
        
        Args:
            preferences: User travel preferences
            
        Returns:
            List of recommended destinations
        """
        # Create a prompt for the OpenAI model
        prompt = self._create_destination_recommendation_prompt(preferences)
        
        # Call OpenAI API
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a travel destination recommendation expert with knowledge of trending destinations, especially in the Middle East and Saudi Arabia. Your task is to recommend destinations based on user preferences."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
            )
            
            # Parse the response
            response_content = response.choices[0].message.content
            if not response_content:
                logger.error("Empty response received from OpenAI API")
                return []
            
            data = json.loads(response_content)
            
            # Validate and create Location objects
            locations = []
            for item in data.get("destinations", []):
                try:
                    location = Location(
                        city=item.get("city", ""),
                        country=item.get("country", ""),
                        region=item.get("region", None),
                        latitude=item.get("latitude", None),
                        longitude=item.get("longitude", None)
                    )
                    locations.append(location)
                except ValidationError as e:
                    logger.error(f"Error validating location data: {e}")
            
            return locations
            
        except Exception as e:
            logger.error(f"Error generating travel recommendations: {e}")
            return []
    
    def create_travel_itinerary(
        self, 
        preferences: UserPreferences, 
        destination: Location
    ) -> Optional[TravelItinerary]:
        """
        Create a comprehensive travel itinerary based on user preferences and selected destination.
        
        Args:
            preferences: User travel preferences
            destination: Selected destination
            
        Returns:
            A complete travel itinerary or None if an error occurs
        """
        # Create a prompt for the OpenAI model
        prompt = self._create_itinerary_prompt(preferences, destination)
        
        # Call OpenAI API
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a travel itinerary planning expert with knowledge of destinations, attractions, restaurants, and travel logistics. Your task is to create a detailed, day-by-day travel itinerary based on user preferences and selected destination."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
            )
            
            # Parse the response
            response_content = response.choices[0].message.content
            if not response_content:
                logger.error("Empty response received from OpenAI API")
                return None
            
            data = json.loads(response_content)
            
            # The structure of the data should be similar to the TravelItinerary model
            try:
                itinerary = TravelItinerary(**data)
                return itinerary
            except ValidationError as e:
                logger.error(f"Error validating itinerary data: {e}")
                return None
            
        except Exception as e:
            logger.error(f"Error creating travel itinerary: {e}")
            return None
    
    def analyze_destination_trends(self, region: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze trending destinations, particularly focused on Middle East if specified.
        
        Args:
            region: Optional region to focus on
            
        Returns:
            Dictionary with trending destinations and relevant information
        """
        # Create a prompt for the OpenAI model
        prompt = f"Provide an analysis of current trending travel destinations"
        if region:
            prompt += f" in {region}"
        prompt += ". Include information about why these destinations are trending, unique experiences they offer, and any recent developments that make them attractive to travelers. Format the response as a structured JSON with an array of destinations."
        
        if settings.PRIORITIZE_MIDDLE_EAST:
            prompt += " Prioritize destinations in the Middle East and Saudi Arabia."
        
        # Call OpenAI API
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a travel trend analyst with deep knowledge of global travel trends, especially in the Middle East and Saudi Arabia."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
            )
            
            # Parse the response
            response_content = response.choices[0].message.content
            if not response_content:
                logger.error("Empty response received from OpenAI API")
                return {}
            
            return json.loads(response_content)
            
        except Exception as e:
            logger.error(f"Error analyzing destination trends: {e}")
            return {}
    
    def get_social_media_content(self, destination: str) -> Dict[str, Any]:
        """
        Simulate getting social media content about a destination.
        This would usually involve integrating with social media APIs,
        but we're simulating it here using OpenAI.
        
        Args:
            destination: Destination to get content for
            
        Returns:
            Dictionary with social media content
        """
        # Create a prompt for the OpenAI model
        prompt = f"Generate a list of simulated trending social media content about {destination} that would help a traveler get excited about visiting. Include types of content like 'reels', 'photos', 'vlogs', and 'posts'. For each piece of content, provide a title, brief description, popularity metrics, and a fictional creator name. Format the response as a structured JSON with arrays for each content type."
        
        # Call OpenAI API
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a social media analyst specializing in travel content."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
            )
            
            # Parse the response
            response_content = response.choices[0].message.content
            if not response_content:
                logger.error("Empty response received from OpenAI API")
                return {}
            
            return json.loads(response_content)
            
        except Exception as e:
            logger.error(f"Error getting social media content: {e}")
            return {}
    
    def process_pilgrimage_requirements(
        self, 
        preferences: UserPreferences
    ) -> Dict[str, Any]:
        """
        Process specific requirements for pilgrimage travel, leveraging Nusuk partnership.
        
        Args:
            preferences: User travel preferences
            
        Returns:
            Dictionary with pilgrimage-specific information and recommendations
        """
        if not settings.PARTNER_WITH_NUSUK:
            return {"error": "Nusuk partnership is not enabled"}
        
        # Check if pilgrimage is among the interests
        if "PILGRIMAGE" not in [i.value for i in preferences.interests]:
            return {"error": "User is not interested in pilgrimage travel"}
        
        # Create a prompt for the OpenAI model
        prompt = """
        Create a comprehensive guide for pilgrimage travel to Saudi Arabia, including:
        1. Visa requirements and process
        2. Recommended accommodations near religious sites
        3. Suggested itinerary for religious activities
        4. Essential items to pack
        5. Cultural norms and etiquette to observe
        6. Health and safety recommendations
        7. Available flights through Nusuk's 450+ airline partners
        
        Format the response as a structured JSON with sections for each category.
        """
        
        # Call OpenAI API
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a pilgrimage travel specialist with deep knowledge of religious travel to Saudi Arabia."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
            )
            
            # Parse the response
            response_content = response.choices[0].message.content
            if not response_content:
                logger.error("Empty response received from OpenAI API")
                return {}
            
            data = json.loads(response_content)
            data["nusuk_partnership"] = True
            data["airline_count"] = settings.AIRLINES_COUNT
            
            return data
            
        except Exception as e:
            logger.error(f"Error processing pilgrimage requirements: {e}")
            return {}
    
    def _create_destination_recommendation_prompt(self, preferences: UserPreferences) -> str:
        """
        Create a prompt for destination recommendations.
        
        Args:
            preferences: User travel preferences
            
        Returns:
            Prompt string for OpenAI API
        """
        prompt = "Based on the following user preferences, recommend 5 suitable travel destinations:\n\n"
        
        # Add user preferences to the prompt
        if preferences.destination:
            prompt += f"Preferred destination: {preferences.destination}\n"
        else:
            prompt += "No specific destination preference (open to recommendations)\n"
        
        prompt += f"Budget: ${preferences.budget}\n"
        prompt += f"Travel dates: {preferences.start_date} to {preferences.end_date}\n"
        prompt += f"Number of travelers: {preferences.travelers}\n"
        prompt += f"Travel style: {', '.join([style.value for style in preferences.travel_style])}\n"
        prompt += f"Interests: {', '.join([interest.value for interest in preferences.interests])}\n"
        
        if preferences.is_flexible_dates:
            prompt += "Dates are flexible\n"
        
        if preferences.is_flexible_destination:
            prompt += "Destination is flexible\n"
        
        if preferences.previous_destinations:
            prompt += f"Previous destinations: {', '.join(preferences.previous_destinations)}\n"
        
        if preferences.special_requirements:
            prompt += f"Special requirements: {preferences.special_requirements}\n"
        
        # Add Almosafer-specific requirements
        if settings.PRIORITIZE_MIDDLE_EAST:
            prompt += "\nPrioritize destinations in the Middle East and Saudi Arabia, but include other options if they are a better match for the preferences.\n"
        
        # Check if pilgrimage is an interest
        if "PILGRIMAGE" in [i.value for i in preferences.interests]:
            prompt += "\nInclude options for religious pilgrimage in Saudi Arabia, highlighting Nusuk partnership benefits.\n"
        
        # Output format instructions
        prompt += """
        Format your response as a JSON object with the following structure:
        {
            "destinations": [
                {
                    "city": "City name",
                    "country": "Country name",
                    "region": "Region name",
                    "description": "Brief description of the destination and why it matches the preferences",
                    "key_attractions": ["Attraction 1", "Attraction 2", ...],
                    "estimated_daily_cost": Numeric value in USD,
                    "best_time_to_visit": "Information about the best time to visit",
                    "latitude": Numeric latitude value (optional),
                    "longitude": Numeric longitude value (optional)
                },
                ...
            ]
        }
        """
        
        return prompt
    
    def _create_itinerary_prompt(self, preferences: UserPreferences, destination: Location) -> str:
        """
        Create a prompt for generating a travel itinerary.
        
        Args:
            preferences: User travel preferences
            destination: Selected destination
            
        Returns:
            Prompt string for OpenAI API
        """
        prompt = f"Create a detailed travel itinerary for a trip to {destination.city}, {destination.country} based on the following user preferences:\n\n"
        
        # Add user preferences to the prompt
        prompt += f"Budget: ${preferences.budget}\n"
        prompt += f"Travel dates: {preferences.start_date} to {preferences.end_date}\n"
        prompt += f"Number of travelers: {preferences.travelers}\n"
        prompt += f"Travel style: {', '.join([style.value for style in preferences.travel_style])}\n"
        prompt += f"Interests: {', '.join([interest.value for interest in preferences.interests])}\n"
        
        if preferences.special_requirements:
            prompt += f"Special requirements: {preferences.special_requirements}\n"
        
        # Add Almosafer-specific requirements
        if settings.PRIORITIZE_LUXURY and "LUXURY" in [s.value for s in preferences.travel_style]:
            prompt += "\nPrioritize luxury experiences, high-end accommodations, and premium services.\n"
        
        # Calculate trip duration
        start_date = preferences.start_date
        end_date = preferences.end_date
        duration = (end_date - start_date).days + 1
        
        prompt += f"\nThis is a {duration}-day trip. Please include:\n"
        prompt += "1. Recommended flights (prioritize luxury airlines if the style is 'luxury')\n"
        prompt += "2. Accommodation recommendation\n"
        prompt += "3. Day-by-day itinerary with activities, restaurants, and transportation\n"
        prompt += "4. Total cost breakdown\n"
        
        # Check if pilgrimage is an interest
        if "PILGRIMAGE" in [i.value for i in preferences.interests]:
            prompt += "\nInclude religious activities and accommodations near religious sites.\n"
        
        # Output format instructions
        prompt += """
        Format your response to match the TravelItinerary model structure with the following main components:
        - itinerary_id (a unique string)
        - user_preferences (the provided preferences)
        - destination (the location object)
        - start_date and end_date
        - flights (array of Flight objects)
        - accommodation (an Accommodation object)
        - daily_itineraries (array of DailyItinerary objects, one for each day)
        - bookings (array of Booking objects for flights, accommodation, etc.)
        - total_cost (numeric sum of all expenses)
        - notes (any additional relevant information)
        
        Ensure all nested objects follow their respective models with all required fields.
        """
        
        return prompt