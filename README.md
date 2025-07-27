# 🚗 Smart EV Charging Station Locator

## Overview
This project utilizes Leaflet JS, OpenStreetMap (OSM), and Open Source Routing Machine (OSRM) to provide efficient routing. It also incorporates a Cooja simulator to mimic battery percentage drop and track it in real-time. When the battery level falls below a predetermined threshold, the user is presented with an option to redirect to the nearest charging station.

## 🌟 Features

* **Real-time Battery Tracking**: Simulate battery percentage drop using Cooja simulator and track it in real-time.
* **Smart Routing**: Utilize OSRM for efficient routing and provide turn-by-turn directions.
* **Nearest Charging Station Redirect**: Offer users the option to redirect to the nearest charging station when the battery level falls below a certain threshold.
* **Interactive Map**: Leverage Leaflet JS and OSM to display an interactive map with routing information and charging station locations.

## 🛠️ Technology Stack

* **Frontend**: Leaflet JS, OpenStreetMap (OSM), PyQt6
* **Backend**: FastAPI, Python
* **Simulator**: Cooja
* **Routing Engine**: Open Source Routing Machine (OSRM)

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
1. **Start Battery Tracker**:
   ```bash
   python battery_tracker.py # from root directory
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
├── Makefile
├── README.md  # Project documentation
├── backend
│   ├── __init__.py  # initializes package
│   ├── app.py  # main FastAPI app
│   ├── models.py  # models
│   ├── requirements.txt
│   └── services
│       ├── __init__.py  # initializes package
│       ├── charging_service.py
│       └── routing_service.py
├── battery-sim.c
├── battery_log.txt
├── battery_tracker.py
├── frontend
│   ├── main.py
│   └── map.html
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

- Real-time traffic data integration
- Multiple vehicle support
- Charging station booking
- Route optimization
- Mobile app version
- Advanced battery analytics