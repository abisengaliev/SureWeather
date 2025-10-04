# NASA Weather App - Deployment Guide

This guide will help you deploy the NASA Weather App for the Space Apps Challenge.

## Prerequisites

- Docker and Docker Compose installed
- OpenWeather API key (optional, app works with fallback data)

## Quick Start

1. **Clone and navigate to the project:**
   ```bash
   cd nasa-weather-app
   ```

2. **Set up environment variables:**
   ```bash
   # Create .env file in the deployment directory
   echo "OPENWEATHER_API_KEY=your_api_key_here" > deployment/.env
   ```

3. **Start the application:**
   ```bash
   cd deployment
   docker-compose up --build
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Features

### 🌤️ Weather Forecasting
- **Short-term forecast (16 days)**: Real-time weather data from OpenWeather One Call API 3.0
- **Long-term outlook (6 months)**: Seasonal climate probabilities using NASA POWER data simulation
- **Fallback system**: Synthetic weather generator when API is unavailable

### 🎯 Event Suitability
- **Smart classification**: Events categorized by weather compatibility
- **Scoring system**: 0-100 suitability scores based on weather conditions
- **Categories**: Sunny-friendly, rain-compatible, wind-based, cold-weather, uncomfortable

### 👕 Clothing Recommendations
- **Intelligent suggestions**: Weather-appropriate clothing and gear
- **Priority system**: Essential vs optional items
- **Comfort tips**: Practical advice for weather conditions

### 🗺️ Interactive Map
- **GPS detection**: Automatic location detection
- **Smooth animations**: Fly-to animations when selecting locations
- **Click anywhere**: Get weather data for any location

### 📊 Seasonal Outlook
- **Probability heatmaps**: Visual representation of climate trends
- **Monthly breakdowns**: 6-month seasonal forecasts
- **Climate zones**: Location-based climate analysis

## API Endpoints

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

## Development

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

## Production Deployment

### Using Docker Compose
```bash
# Production build
docker-compose -f docker-compose.prod.yml up --build -d
```

### Individual Services

#### Backend (FastAPI)
- **Platform**: Render, Heroku, AWS, Google Cloud
- **Requirements**: Python 3.9+, 512MB RAM minimum
- **Environment variables**: `OPENWEATHER_API_KEY`

#### Frontend (Next.js)
- **Platform**: Vercel, Netlify, AWS Amplify
- **Environment variables**: `NEXT_PUBLIC_API_URL`

## Configuration

### Environment Variables

#### Backend
- `OPENWEATHER_API_KEY`: OpenWeather API key (optional)
- `PYTHONPATH`: Python path (set to `/app`)

#### Frontend
- `NEXT_PUBLIC_API_URL`: Backend API URL

### Database
- **Development**: SQLite (included)
- **Production**: PostgreSQL (recommended)

## Monitoring

### Health Checks
- Backend: `GET /health`
- Frontend: `GET /` (returns 200)

### Logs
```bash
# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Check if backend is running on port 8000
   - Verify `NEXT_PUBLIC_API_URL` environment variable

2. **Map Not Loading**
   - Ensure Leaflet CSS is loaded
   - Check browser console for errors

3. **Weather Data Not Loading**
   - Verify OpenWeather API key (optional)
   - Check network connectivity
   - App will use fallback data if API fails

### Performance Optimization

1. **Caching**: Implement Redis for API response caching
2. **CDN**: Use CDN for static assets
3. **Database**: Upgrade to PostgreSQL for production
4. **Monitoring**: Add application performance monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is created for NASA Space Apps Challenge 2024.

## Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation at `/docs`
