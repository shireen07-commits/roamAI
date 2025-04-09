"""
Script to list the components and interfaces of the RoamAI system.
"""

import inspect
import os
import sys

# Ensure PYTHONPATH includes the current directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import components
from roamai.services.travel_planner import TravelPlannerService
from roamai.services.flight_service import FlightService
from roamai.services.accommodation_service import AccommodationService
from roamai.services.activity_service import ActivityService
from roamai.services.notification_service import NotificationService
from roamai.services.openai_service import OpenAIService
from roamai.models.travel import (
    UserPreferences, TravelStyle, TravelInterest, Location, 
    TravelItinerary, Flight, Accommodation, Activity, Restaurant,
    DailyItinerary, Booking, Transportation
)

def print_section_header(title):
    """Print a section header."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)

def print_class_info(cls):
    """Print information about a class."""
    print(f"\n{cls.__name__}:")
    print("-" * 80)
    
    # Get class docstring
    if cls.__doc__:
        print(f"Description: {cls.__doc__.strip()}")
    
    # Get methods
    methods = inspect.getmembers(cls, predicate=inspect.isfunction)
    if methods:
        print("\nMethods:")
        for name, method in methods:
            if not name.startswith('_'):  # Skip private methods
                sig = inspect.signature(method)
                print(f"  {name}{sig}")
                if method.__doc__:
                    doc = method.__doc__.strip().split("\n")[0]
                    print(f"    {doc}")

def print_enum_info(enum_cls):
    """Print information about an enum."""
    print(f"\n{enum_cls.__name__}:")
    print("-" * 80)
    
    # Get enum docstring
    if enum_cls.__doc__:
        print(f"Description: {enum_cls.__doc__.strip()}")
    
    # Get values
    values = [member.value for member in enum_cls]
    print(f"Values: {values}")

def main():
    """List the components and interfaces of the RoamAI system."""
    print_section_header("RoamAI System Overview")
    
    print("\nRoamAI is an AI-powered travel planning agent built with Python.")
    print("It helps users plan and book travel itineraries by generating personalized")
    print("recommendations for flights, accommodations, and activities based on user preferences.")
    
    # Print service classes
    print_section_header("Services")
    print_class_info(TravelPlannerService)
    print_class_info(FlightService)
    print_class_info(AccommodationService)
    print_class_info(ActivityService)
    print_class_info(NotificationService)
    print_class_info(OpenAIService)
    
    # Print model classes
    print_section_header("Data Models")
    print_class_info(UserPreferences)
    print_class_info(TravelItinerary)
    print_class_info(Location)
    print_class_info(Flight)
    print_class_info(Accommodation)
    print_class_info(Activity)
    print_class_info(DailyItinerary)
    print_class_info(Booking)
    
    # Print enums
    print_section_header("Enumerations")
    print_enum_info(TravelStyle)
    print_enum_info(TravelInterest)
    
    print("\n\n")
    print_section_header("End of System Overview")

if __name__ == "__main__":
    main()