# 🚗 Smart EV Charging Station Locator

A smart electric vehicle charging station locator that tracks your location, monitors battery levels, and automatically suggests nearby charging stations when your battery runs low.

## 🌟 Features

- **Real-time Location Tracking**: Uses GPS to track your current location
- **Battery Monitoring**: Monitor your EV's battery level in real-time
- **Smart Notifications**: Automatically suggests charging stations when battery < 25%
- **Interactive Map**: OpenStreetMap-based interface with search functionality
- **Speed Tracking**: Shows current vehicle speed
- **Route History**: Stores location and battery data

## 🛠️ Technology Stack

- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Frontend**: PyQt6, HTML/CSS/JavaScript, Leaflet.js
- **APIs**: OpenChargeMap API for charging station data
- **Database**: SQLite for route history

## 🚀 Quick Start

### Prerequisites

Make sure you have Python 3.8+ installed on your system.

### Installation

1. **Install Dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

### Running the Application

#### Option 1: Use the Start Scripts (Recommended)

1. **Start Backend Server**:
   ```bash
   python start_backend.py
   ```

2. **Start Frontend Application** (in a new terminal):
   ```bash
   python start_frontend.py
   ```

#### Option 2: Manual Start

1. **Initialize Database**:
   ```bash
   cd backend
   python init_db.py
   ```

2. **Start Backend Server**:
   ```bash
   cd backend
   uvicorn app:app --reload 
   ```

3. **Start Frontend Application** (in a new terminal):
   ```bash
   cd frontend
   python main.py
   ```

## 📱 Usage

1. **Launch the Application**: The frontend will open a window with an interactive map
2. **Allow Location Access**: Grant location permissions when prompted
3. **Set Battery Level**: Use the battery input field to set your current battery level
4. **Monitor**: The app will track your location and speed automatically
5. **Low Battery Alert**: When battery drops below 25%, nearby charging stations will be suggested

## 🔌 API Endpoints

- `GET /` - Health check
- `POST /api/location/update` - Update vehicle location and battery level
- `GET /api/charging/` - Get nearest charging station
- `POST /api/route/` - Get route between two points

## 📊 Database Schema

### RouteHistory Table
- `id`: Primary key
- `lat`: Latitude coordinate
- `lng`: Longitude coordinate
- `battery`: Battery level percentage
- `timestamp`: Entry timestamp

## 🗺️ Map Features

- **Search**: Find locations using the search box
- **Add Markers**: Click on the map or use the "Add Marker" button
- **Current Location**: Click "My Location" to center map on your position
- **Clear Markers**: Remove all markers from the map

## 🔧 Configuration

### Environment Variables
- No environment variables required for basic setup
- The app uses demo API keys for OpenChargeMap

### API Keys
- OpenChargeMap: Uses demo key (limited requests)
- For production, get your own API key from [OpenChargeMap](https://openchargemap.org/site/develop/api)

## 🚨 Troubleshooting

### Common Issues

1. **"Module not found" errors**:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. **Port 8000 already in use**:
   - Stop other services using port 8000
   - Or modify the port in `backend/main.py`

3. **Location permissions denied**:
   - Enable location services in your browser
   - For local files, some browsers may restrict geolocation

4. **PyQt6 import errors**:
   ```bash
   pip install PyQt6 PyQt6-WebEngine
   ```

### Debug Mode

To run in debug mode with more detailed logs:
```bash
cd backend
uvicorn app:app --host 127.0.0.1 --port 8000 --reload --log-level debug
```

## 📝 Development

### Project Structure
```
Tata hackathon/
├── .gitignore  # gitignore file for GitHub
├── README.md  # Project documentation
├── backend
│   ├── __init__.py  # initializes package
│   ├── app.py  # main FastAPI app
│   ├── database.py  # database configuration
│   ├── init_db.py
│   ├── main.py
│   ├── mapapp.db
│   ├── models.py  # models
│   ├── requirements.txt
│   ├── routes
│   │   ├── __init__.py  # initializes package
│   │   ├── charging.py
│   │   ├── location.py
│   │   └── route.py
│   └── services
│       ├── __init__.py  # initializes package
│       ├── charging_service.py
│       └── routing_service.py
├── frontend
│   ├── main.py
│   ├── map.html
│   └── map_new.html
├── start_backend.py
├── start_frontend.py
```

### Adding New Features

1. **Backend**: Add routes in `backend/routes/`
2. **Frontend**: Modify `frontend/map.html` for UI changes
3. **Database**: Update models in `backend/models.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🎯 Future Enhancements

- [ ] Real-time traffic data integration
- [ ] Multiple vehicle support
- [ ] Charging station booking
- [ ] Route optimization
- [ ] Mobile app version
- [ ] Advanced battery analytics