"""
Command-line interface for the RoamAI application.
"""

import logging
import argparse
from datetime import datetime, date, timedelta
import json

from .core.config import settings
from .models.travel import UserPreferences, Location, TravelStyle, TravelInterest
from .services.travel_planner import TravelPlannerService
from .utils.helpers import serialize_dates

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description=f"{settings.APP_NAME} - {settings.APP_DESCRIPTION}")
    
    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Recommend destinations command
    recommend_parser = subparsers.add_parser("recommend", help="Recommend destinations based on user preferences")
    recommend_parser.add_argument("--destination", help="Preferred destination")
    recommend_parser.add_argument("--budget", type=float, required=True, help="Travel budget")
    recommend_parser.add_argument("--start-date", required=True, help="Start date (YYYY-MM-DD)")
    recommend_parser.add_argument("--end-date", required=True, help="End date (YYYY-MM-DD)")
    recommend_parser.add_argument("--travelers", type=int, default=1, help="Number of travelers")
    recommend_parser.add_argument("--travel-style", nargs="+", required=True, choices=[s.value for s in TravelStyle], help="Travel style")
    recommend_parser.add_argument("--interests", nargs="+", required=True, choices=[i.value for i in TravelInterest], help="Travel interests")
    recommend_parser.add_argument("--flexible-dates", action="store_true", help="Dates are flexible")
    recommend_parser.add_argument("--flexible-destination", action="store_true", help="Destination is flexible")
    recommend_parser.add_argument("--output", default="recommendations.json", help="Output file")
    
    # Trending destinations command
    trending_parser = subparsers.add_parser("trending", help="Get trending destinations")
    trending_parser.add_argument("--region", help="Optional region to focus on")
    trending_parser.add_argument("--output", default="trending.json", help="Output file")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize service
    travel_planner = TravelPlannerService()
    
    # Execute command
    if args.command == "recommend":
        # Convert string dates to date objects
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d").date()
        
        # Convert string travel style to TravelStyle enum values
        travel_style = [TravelStyle(style) for style in args.travel_style]
        
        # Convert string interests to TravelInterest enum values
        interests = [TravelInterest(interest) for interest in args.interests]
        
        # Create user preferences object
        preferences = UserPreferences(
            destination=args.destination,
            budget=args.budget,
            start_date=start_date,
            end_date=end_date,
            travelers=args.travelers,
            travel_style=travel_style,
            interests=interests,
            is_flexible_dates=args.flexible_dates,
            is_flexible_destination=args.flexible_destination
        )
        
        logger.info(f"Generating destination recommendations for preferences: {preferences}")
        
        # Get recommendations
        recommendations = travel_planner.recommend_destinations(preferences)
        
        if not recommendations:
            logger.error("No destinations found matching the preferences")
        else:
            # Convert recommendations to serializable format
            recommendations_dict = [json.loads(r.model_dump_json()) for r in recommendations]
            
            # Save to output file
            with open(args.output, "w") as f:
                json.dump(recommendations_dict, f, indent=2)
            
            logger.info(f"Saved {len(recommendations)} recommendations to {args.output}")
            
            # Print recommendations to console
            print(f"\nRecommended Destinations:")
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. {rec.city}, {rec.country}")
    
    elif args.command == "trending":
        logger.info(f"Getting trending destinations for region: {args.region}")
        
        # Get trending destinations
        trending = travel_planner.get_trending_destinations(args.region)
        
        if not trending:
            logger.error("No trending destinations found")
        else:
            # Serialize dates
            trending = serialize_dates(trending)
            
            # Save to output file
            with open(args.output, "w") as f:
                json.dump(trending, f, indent=2)
            
            logger.info(f"Saved trending destinations to {args.output}")
            
            # Print trending destinations to console
            print(f"\nTrending Destinations:")
            if "destinations" in trending:
                for i, dest in enumerate(trending["destinations"], 1):
                    print(f"{i}. {dest.get('city', 'Unknown')}, {dest.get('country', 'Unknown')}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()