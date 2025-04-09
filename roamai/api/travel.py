"""
Travel-related API endpoints for RoamAI.
"""

import logging
from datetime import date, datetime
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from ..models.travel import (
    UserPreferences, TravelStyle, TravelInterest, Location, TravelItinerary
)
from ..services.travel_planner import TravelPlannerService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(tags=["Travel"])

# Create service instance
travel_planner = TravelPlannerService()

# Request and response models
class UserPreferenceRequest(BaseModel):
    """User travel preferences request model."""
    
    destination: Optional[str] = None
    budget: float
    start_date: date
    end_date: date
    travelers: int
    travel_style: List[str]
    interests: List[str]
    is_flexible_dates: bool = False
    is_flexible_destination: bool = False
    special_requirements: Optional[str] = None

class TravelerDetailsRequest(BaseModel):
    """Traveler details request model."""
    
    name: str
    email: str
    phone: str
    departure_city: str
    additional_details: Optional[Dict[str, Any]] = None

class DestinationRecommendationResponse(BaseModel):
    """Destination recommendation response model."""
    
    city: str
    country: str
    region: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    highlights: Optional[List[str]] = None
    match_score: Optional[float] = None

# API endpoints
@router.post("/recommendations", response_model=List[DestinationRecommendationResponse])
async def get_destination_recommendations(preferences: UserPreferenceRequest):
    """
    Get destination recommendations based on user preferences.
    """
    try:
        # Convert API request model to internal model
        user_prefs = UserPreferences(
            destination=preferences.destination,
            budget=preferences.budget,
            start_date=preferences.start_date,
            end_date=preferences.end_date,
            travelers=preferences.travelers,
            travel_style=[TravelStyle(s) for s in preferences.travel_style],
            interests=[TravelInterest(i) for i in preferences.interests],
            is_flexible_dates=preferences.is_flexible_dates,
            is_flexible_destination=preferences.is_flexible_destination,
            special_requirements=preferences.special_requirements
        )
        
        # Get recommendations from service
        recommendations = travel_planner.recommend_destinations(user_prefs)
        
        # Convert to response model
        response = []
        for rec in recommendations:
            response.append(DestinationRecommendationResponse(
                city=rec.city,
                country=rec.country,
                region=rec.region,
                description=rec.description,
                image_url=rec.image_url,
                highlights=rec.highlights,
                match_score=rec.match_score
            ))
        
        return response
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/itinerary", response_model=Dict[str, Any])
async def create_travel_itinerary(
    preferences: UserPreferenceRequest,
    traveler_details: TravelerDetailsRequest
):
    """
    Create a complete travel itinerary including flights, accommodation, and activities.
    """
    try:
        # Convert API request models to internal models
        user_prefs = UserPreferences(
            destination=preferences.destination,
            budget=preferences.budget,
            start_date=preferences.start_date,
            end_date=preferences.end_date,
            travelers=preferences.travelers,
            travel_style=[TravelStyle(s) for s in preferences.travel_style],
            interests=[TravelInterest(i) for i in preferences.interests],
            is_flexible_dates=preferences.is_flexible_dates,
            is_flexible_destination=preferences.is_flexible_destination,
            special_requirements=preferences.special_requirements
        )
        
        # Create destination location from preferences
        destination = Location(
            city=preferences.destination,
            country="",  # Will be populated by the service
            region=""    # Will be populated by the service
        )
        
        # Process traveler details
        traveler_dict = {
            "name": traveler_details.name,
            "email": traveler_details.email,
            "phone": traveler_details.phone,
            "departure_city": traveler_details.departure_city
        }
        
        if traveler_details.additional_details:
            traveler_dict.update(traveler_details.additional_details)
        
        # Create itinerary
        itinerary = travel_planner.create_and_book_itinerary(
            user_prefs, destination, traveler_dict
        )
        
        if not itinerary:
            raise HTTPException(
                status_code=500,
                detail="Failed to create travel itinerary"
            )
        
        # Convert to dictionary and return
        return itinerary.model_dump()
    except Exception as e:
        logger.error(f"Error creating itinerary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trending")
async def get_trending_destinations(region: Optional[str] = None):
    """
    Get trending destinations, optionally filtered by region.
    """
    try:
        return travel_planner.get_trending_destinations(region)
    except Exception as e:
        logger.error(f"Error getting trending destinations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/social-content/{destination}")
async def get_destination_social_content(destination: str):
    """
    Get social media content for a specific destination.
    """
    try:
        return travel_planner.get_destination_social_content(destination)
    except Exception as e:
        logger.error(f"Error getting social content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pilgrimage")
async def get_pilgrimage_information(preferences: UserPreferenceRequest):
    """
    Get pilgrimage-specific information and recommendations.
    """
    try:
        # Convert API request model to internal model
        user_prefs = UserPreferences(
            destination=preferences.destination,
            budget=preferences.budget,
            start_date=preferences.start_date,
            end_date=preferences.end_date,
            travelers=preferences.travelers,
            travel_style=[TravelStyle(s) for s in preferences.travel_style],
            interests=[TravelInterest(i) for i in preferences.interests],
            is_flexible_dates=preferences.is_flexible_dates,
            is_flexible_destination=preferences.is_flexible_destination,
            special_requirements=preferences.special_requirements
        )
        
        return travel_planner.get_pilgrimage_info(user_prefs)
    except Exception as e:
        logger.error(f"Error getting pilgrimage information: {e}")
        raise HTTPException(status_code=500, detail=str(e))