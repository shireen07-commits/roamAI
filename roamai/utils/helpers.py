"""
Helper functions for the RoamAI application.
"""

import json
import logging
import random
import uuid
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional, Union

from ..models.travel import TravelItinerary

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_id(prefix: str = "") -> str:
    """
    Generate a unique ID.
    
    Args:
        prefix: Optional prefix for the ID
        
    Returns:
        Unique ID string
    """
    return f"{prefix}{uuid.uuid4().hex[:8].upper()}"


def format_currency(amount: float, currency: str = "USD") -> str:
    """
    Format a currency amount.
    
    Args:
        amount: Amount to format
        currency: Currency code
        
    Returns:
        Formatted currency string
    """
    if currency == "USD":
        return f"${amount:.2f}"
    elif currency == "EUR":
        return f"€{amount:.2f}"
    elif currency == "GBP":
        return f"£{amount:.2f}"
    else:
        return f"{amount:.2f} {currency}"


def format_datetime(dt: datetime, include_time: bool = True) -> str:
    """
    Format a datetime object.
    
    Args:
        dt: Datetime to format
        include_time: Whether to include the time
        
    Returns:
        Formatted datetime string
    """
    if include_time:
        return dt.strftime("%B %d, %Y at %H:%M")
    else:
        return dt.strftime("%B %d, %Y")


def format_date(d: date) -> str:
    """
    Format a date object.
    
    Args:
        d: Date to format
        
    Returns:
        Formatted date string
    """
    return d.strftime("%B %d, %Y")


def calculate_trip_duration(start_date: date, end_date: date) -> int:
    """
    Calculate the duration of a trip in days.
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        Trip duration in days
    """
    return (end_date - start_date).days + 1


def parse_date(date_str: str) -> date:
    """
    Parse a date string.
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        Date object
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        logger.error(f"Invalid date format: {date_str}")
        raise ValueError(f"Invalid date format: {date_str}. Expected YYYY-MM-DD.")


def itinerary_to_dict(itinerary: TravelItinerary) -> Dict[str, Any]:
    """
    Convert an itinerary to a dictionary.
    
    Args:
        itinerary: Travel itinerary
        
    Returns:
        Dictionary representation of the itinerary
    """
    return json.loads(itinerary.model_dump_json())


def dict_to_itinerary(data: Dict[str, Any]) -> TravelItinerary:
    """
    Convert a dictionary to an itinerary.
    
    Args:
        data: Dictionary representation of an itinerary
        
    Returns:
        Travel itinerary
    """
    return TravelItinerary(**data)


def serialize_dates(obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    Serialize date and datetime objects in a dictionary.
    
    Args:
        obj: Dictionary possibly containing date and datetime objects
        
    Returns:
        Dictionary with serialized dates
    """
    for key, value in obj.items():
        if isinstance(value, datetime):
            obj[key] = value.isoformat()
        elif isinstance(value, date):
            obj[key] = value.isoformat()
        elif isinstance(value, dict):
            obj[key] = serialize_dates(value)
        elif isinstance(value, list):
            obj[key] = [serialize_dates(item) if isinstance(item, dict) else item for item in value]
    
    return obj