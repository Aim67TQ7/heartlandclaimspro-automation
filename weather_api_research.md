# Weather API Research for Storm Tracking

## National Weather Service (NWS) API

### Overview
- Free, open data API provided by the US government
- No API key required, but User-Agent header is needed
- Reasonable rate limits for typical use
- Cache-friendly approach with content expiration based on information lifecycle
- API URL: https://api.weather.gov

### Key Features
- Provides real-time access to critical forecasts, alerts, and observations
- Returns data in GeoJSON format by default, which includes precise geographic coordinates
- Supports various data formats: GeoJSON, JSON-LD, DWML, OXML, CAP, ATOM
- Alerts include detailed information about affected areas with polygon coordinates

### Alerts Endpoint
- Endpoint: https://api.weather.gov/alerts/active
- Returns all active weather alerts nationwide
- Each alert contains:
  - Unique identifier
  - Geographic polygon coordinates defining the affected area
  - Area description (county/region names)
  - Event type (Flood Advisory, Severe Weather Statement, etc.)
  - Severity level (Minor, Moderate, Severe)
  - Timing information (sent, effective, onset, expires, ends)
  - Detailed description of the weather event
  - Instructions for affected populations

### Advantages
- Free to use with no subscription required
- Provides precise geographic boundaries of affected areas
- Includes detailed metadata about each weather event
- Official source of weather alerts in the US

### Limitations
- Limited to US territories
- Rate limits not publicly disclosed

## OpenWeatherMap Global Weather Alerts API

### Overview
- Commercial API with subscription model
- Collects weather warnings from national weather warning systems worldwide
- API URL: https://api.openweathermap.org

### Key Features
- Global coverage of weather alerts
- Push notification system for real-time alerts
- Each alert contains:
  - Geographic polygon coordinates of affected area
  - Message type (warning, watch, etc.)
  - Categories (Met for meteorological)
  - Urgency, severity, and certainty ratings
  - Timing information
  - Detailed description in multiple languages
  - Instructions for affected populations

### Advantages
- Global coverage beyond US territories
- Push notification system for immediate alerts
- Multilingual support

### Limitations
- Requires paid subscription
- Monthly pricing model

## Conclusion

For our storm damage tracking system, the National Weather Service API appears to be the most suitable option for the following reasons:

1. It's free to use with reasonable rate limits
2. It provides detailed geographic data in GeoJSON format
3. It includes precise polygon coordinates of affected areas
4. It offers comprehensive metadata about each weather event
5. It's an official, authoritative source of weather alerts

The NWS API will allow us to:
- Track storms and severe weather events in real-time
- Identify precise geographic boundaries of affected areas
- Extract severity and timing information for prioritization
- Use the geographic data to create targeted Google Ads campaigns

If global coverage is needed in the future, we can integrate OpenWeatherMap's Global Weather Alerts API as a supplementary data source.
