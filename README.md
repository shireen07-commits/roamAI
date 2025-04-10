# roamAI
# RoamAI: AI-Powered Travel Planning Agent

RoamAI is a comprehensive travel planning platform built with Python that leverages artificial intelligence to create personalized travel experiences. From destination recommendations to complete itineraries with flight, accommodation, and activity bookings, RoamAI streamlines the entire travel planning process.

## 🌟 Features

- **Personalized Destination Recommendations**: Get AI-powered travel suggestions based on your preferences
- **Complete Itinerary Generation**: Create detailed travel plans with activities tailored to your interests
- **Flight Booking**: Search and book flights with detailed information (airline, flight numbers, times)
- **Accommodation Booking**: Find and reserve hotels with room details and amenities
- **Activity Planning**: Discover and schedule activities based on your interests
- **Transportation Options**: Local transit recommendations for your destination
- **Booking Management**: Track all your reservations in one place
- **Notification System**: Receive confirmation emails and travel alerts

## 🛠️ Technology Stack

- **Python 3.11+**
- **FastAPI**: For the RESTful API
- **Pydantic**: For data validation and settings management
- **OpenAI**: For intelligent recommendations and content generation
- **Jinja2**: For email template rendering
- **Uvicorn**: ASGI server

## 📋 Prerequisites

- Python 3.11 or higher
- OpenAI API key

## 🚀 Installation

1. Clone the repository:
```bash

```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with the following:
```
OPENAI_API_KEY=your_openai_api_key
```

## 🏃‍♂️ Running RoamAI

### Option 1: Run the Demo Script

To see RoamAI in action with a predefined trip to Dubai:

```bash
cd src
PYTHONPATH=. python demo.py
```

This will display a simulated travel planning process including flight bookings, accommodation, daily activities, and confirmation emails.

### Option 2: Run the API Server

To start the FastAPI server:

```bash
cd src
PYTHONPATH=. python server.py
```

The server will start at `http://0.0.0.0:8000/` with the following endpoints:

- API documentation: `http://0.0.0.0:8000/docs`
- Health check: `http://0.0.0.0:8000/`
- API endpoints at `http://0.0.0.0:8000/api/...`

## 📖 API Documentation

Once the server is running, you can access the interactive API documentation at `http://0.0.0.0:8000/docs`.

Key endpoints include:

- `/api/recommendations`: Get destination recommendations
- `/api/itinerary`: Create a complete travel itinerary
- `/api/trending`: Get trending destinations
- `/api/social`: Access social media content for destinations
- `/api/pilgrimage`: Get pilgrimage-specific information

## 📁 Project Structure

```
src/
├── roamai/
│   ├── api/           # API endpoints and FastAPI app
│   ├── core/          # Core configuration
│   ├── data/          # Data files and mock databases
│   ├── models/        # Pydantic data models
│   ├── services/      # Service modules (flight, accommodation, etc.)
│   ├── templates/     # Email and notification templates
│   └── utils/         # Utility functions
├── demo.py            # Non-interactive demo script
└── server.py          # FastAPI server script
```

## 🧠 Core Services

RoamAI is built on a modular service-oriented architecture:

- **TravelPlannerService**: Orchestrates the travel planning process
- **FlightService**: Handles flight search and booking
- **AccommodationService**: Manages accommodation search and booking
- **ActivityService**: Recommends and books activities
- **NotificationService**: Sends booking confirmations and travel alerts
- **OpenAIService**: Provides AI-powered recommendations and content

## 🔍 Sample Output

The system generates comprehensive travel itineraries including:

- Flight details (airline, flight numbers, departure/arrival times)
- Accommodation information (hotel name, room type, amenities)
- Daily activities based on interests
- Restaurant recommendations
- Local transportation options
- Booking references and confirmation emails
- Total trip cost and other metrics

## 🛣️ Development Roadmap

- [ ] Integration with real flight booking APIs (Amadeus, Skyscanner)
- [ ] Integration with real hotel booking APIs (Booking.com, Expedia)
- [ ] User authentication and profile management
- [ ] Mobile application development
- [ ] Trip sharing and collaboration features
- [ ] Real-time travel updates and notifications

## 🙏 Acknowledgements

- OpenAI for providing the AI capabilities
- FastAPI for the efficient API framework
