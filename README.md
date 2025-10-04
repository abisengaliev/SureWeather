# 🌍 SureWeather - NASA Space Apps Challenge 2025

SureWeather is an interactive weather forecasting and event suitability application that combines short-term forecasts, long-term climate probabilities, event recommendations, and clothing suggestions with an engaging world map interface.

## 🚀 Features

### 🌤️ Dual Weather System
- **Short-term Forecast (16 days)**: Real-time data from OpenWeather One Call API 3.0
- **Long-term Outlook (6 months)**: Seasonal climate probabilities using NASA POWER simulation
- **Fallback Generator**: Synthetic weather data when API is unavailable

### 🎯 Smart Event Recommendations
- **Weather-based Classification**: Events categorized by weather compatibility
- **Suitability Scoring**: 0-100 scores based on weather conditions
- **Categories**: 
  - ☀️ Sunny-friendly (concerts, festivals, hiking)
  - 🌧️ Rain-compatible (museums, indoor events)
  - 🌬️ Wind-based (kite festivals, sailing)
  - ❄️ Cold-weather (skiing, winter activities)
  - 😓 Weather-sensitive (outdoor dining, photography)

### 👕 Intelligent Clothing Recommendations
- **Weather-appropriate Gear**: Smart suggestions based on conditions
- **Priority System**: Essential vs optional items
- **Comfort Tips**: Practical advice for weather conditions

### 🗺️ Interactive World Map
- **GPS Detection**: Automatic location detection
- **Smooth Animations**: Fly-to animations with Leaflet
- **Click Anywhere**: Get weather data for any location

### 📊 Seasonal Outlook Dashboard
- **Probability Heatmaps**: Visual climate trend representation
- **Monthly Breakdowns**: 6-month seasonal forecasts
- **Climate Zone Analysis**: Location-based climate modeling

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **OpenWeather API**: Real-time weather data
- **SQLite**: Local database for query history
- **Pydantic**: Data validation and serialization
- **Machine Learning**: Event suitability scoring and climate modeling

### Frontend
- **Next.js 14**: React framework with SSR
- **TypeScript**: Type-safe development
- **TailwindCSS**: Utility-first CSS framework
- **Framer Motion**: Smooth animations and transitions
- **Leaflet**: Interactive maps
- **Recharts**: Data visualization

### Deployment
- **Docker**: Containerized deployment
- **Docker Compose**: Multi-service orchestration
- **Production Ready**: Vercel + Render deployment configs

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for development)
- Python 3.9+ (for development)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd nasa-weather-app
```

### 2. Environment Configuration
```bash
# Create environment file
echo "OPENWEATHER_API_KEY=your_api_key_here" > deployment/.env
```

### 3. Start with Docker
```bash
cd deployment
docker-compose up --build
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🏗️ Development Setup

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

## 📁 Project Structure

```
nasa-weather-app/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── routes.py            # API endpoints
│   │   ├── services.py          # Weather API integration
│   │   ├── models.py            # Data models
│   │   ├── scoring.py           # Event suitability scoring
│   │   ├── clothing.py          # Clothing recommendations
│   │   └── db.py               # Database operations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/              # Next.js pages
│   │   ├── contexts/           # React contexts
│   │   ├── utils/              # Utility functions
│   │   └── styles/             # CSS styles
│   ├── package.json
│   └── Dockerfile
├── ml/
│   ├── probabilities.py        # Climate probability models
│   ├── scoring.py              # ML scoring algorithms
│   └── categories.py           # Event classification
├── deployment/
│   ├── docker-compose.yml
│   └── README.md
└── README.md
```

## 🔧 API Endpoints

### Weather Data
- `GET /api/v1/forecast/short-term` - 16-day weather forecast
- `GET /api/v1/forecast/long-term` - 6-month seasonal outlook

### Event Recommendations
- `GET /api/v1/events/recommendations` - Weather-based event suggestions
- `GET /api/v1/events` - All available events
- `GET /api/v1/score/event` - Event suitability scoring

### Clothing & Gear
- `GET /api/v1/clothing/recommendations` - Weather-appropriate clothing

### Utility
- `GET /api/v1/health` - Health check
- `GET /api/v1/history` - Query history

## 🎨 Key Features in Detail

### Weather Forecasting
- **Real-time Data**: OpenWeather One Call API 3.0 integration
- **Fallback System**: Synthetic weather generator for reliability
- **Comfort Index**: 0-100 scale based on temperature, humidity, wind, precipitation
- **Visual Indicators**: Weather condition icons and color coding

### Event Suitability System
- **Smart Classification**: ML-based event categorization
- **Weather Requirements**: Temperature, wind, precipitation thresholds
- **Scoring Algorithm**: Multi-factor suitability calculation
- **Recommendations**: Actionable tips for each event

### Interactive Map
- **GPS Integration**: Automatic location detection
- **Smooth Animations**: Fly-to animations for location changes
- **Click Interaction**: Get weather data for any location
- **Responsive Design**: Works on desktop and mobile

### Seasonal Outlook
- **Climate Modeling**: 6-month probability forecasts
- **Heatmap Visualization**: Monthly weather condition probabilities
- **Climate Zones**: Location-based climate analysis
- **Trend Analysis**: Historical pattern recognition

## 🚀 Deployment

### Production Deployment
```bash
# Using Docker Compose
docker-compose -f docker-compose.prod.yml up --build -d

# Individual services
# Backend: Deploy to Render/Heroku/AWS
# Frontend: Deploy to Vercel/Netlify
```

### Environment Variables
- `OPENWEATHER_API_KEY`: OpenWeather API key (optional)
- `NEXT_PUBLIC_API_URL`: Backend API URL

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is created for NASA Space Apps Challenge 2024.

## 🙏 Acknowledgments

- **NASA Space Apps Challenge** for the inspiration
- **OpenWeather** for weather data API
- **NASA POWER** for climate data inspiration
- **Open source community** for amazing tools and libraries

## 📞 Support

For questions and support:
- Create an issue in the repository
- Check the troubleshooting guide
- Review API documentation at `/docs`

---

**Built with ❤️ for NASA Space Apps Challenge 2025**


