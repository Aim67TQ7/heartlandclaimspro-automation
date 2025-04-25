#!/usr/bin/env python3
"""
Storm Tracker Module

This module integrates with the National Weather Service API to track storms and severe weather events.
It identifies affected geographic regions for targeted Google Ads campaigns.
"""

import requests
import json
import time
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("storm_tracker.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("storm_tracker")

class StormTracker:
    """
    A class to track storms and severe weather events using the National Weather Service API.
    """
    
    def __init__(self, data_dir="data"):
        """
        Initialize the StormTracker.
        
        Args:
            data_dir (str): Directory to store storm data
        """
        self.base_url = "https://api.weather.gov"
        self.headers = {
            "User-Agent": "StormDamageAutomation/1.0 (contact@example.com)",
            "Accept": "application/geo+json"
        }
        self.data_dir = data_dir
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        logger.info("StormTracker initialized")
    
    def get_active_alerts(self):
        """
        Fetch all active weather alerts from the NWS API.
        
        Returns:
            dict: JSON response containing active alerts
        """
        url = f"{self.base_url}/alerts/active"
        
        try:
            logger.info(f"Fetching active alerts from {url}")
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            alerts = response.json()
            logger.info(f"Retrieved {len(alerts.get('features', []))} active alerts")
            
            # Save raw alerts data
            self._save_data(alerts, "active_alerts.json")
            
            return alerts
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching active alerts: {e}")
            return None
    
    def filter_severe_alerts(self, alerts, severity_threshold="Moderate"):
        """
        Filter alerts based on severity.
        
        Args:
            alerts (dict): Alerts data from NWS API
            severity_threshold (str): Minimum severity level to include
                                     (options: "Minor", "Moderate", "Severe", "Extreme")
        
        Returns:
            list: Filtered alerts meeting the severity criteria
        """
        if not alerts or "features" not in alerts:
            logger.warning("No alerts data to filter")
            return []
        
        severity_levels = {
            "Minor": 1,
            "Moderate": 2,
            "Severe": 3,
            "Extreme": 4
        }
        
        threshold_value = severity_levels.get(severity_threshold, 2)
        
        filtered_alerts = []
        for alert in alerts["features"]:
            properties = alert.get("properties", {})
            severity = properties.get("severity")
            
            if severity and severity_levels.get(severity, 0) >= threshold_value:
                filtered_alerts.append(alert)
        
        logger.info(f"Filtered {len(filtered_alerts)} severe alerts (threshold: {severity_threshold})")
        return filtered_alerts
    
    def extract_storm_regions(self, alerts):
        """
        Extract geographic regions affected by storms from alerts.
        
        Args:
            alerts (list): List of alert objects
        
        Returns:
            list: List of dictionaries containing region information
        """
        regions = []
        
        for alert in alerts:
            properties = alert.get("properties", {})
            geometry = alert.get("geometry")
            
            if not geometry or not properties:
                continue
            
            region_info = {
                "id": properties.get("id"),
                "event": properties.get("event"),
                "headline": properties.get("headline"),
                "severity": properties.get("severity"),
                "certainty": properties.get("certainty"),
                "urgency": properties.get("urgency"),
                "area_desc": properties.get("areaDesc"),
                "geometry": geometry,
                "effective": properties.get("effective"),
                "expires": properties.get("expires"),
                "description": properties.get("description")
            }
            
            regions.append(region_info)
        
        logger.info(f"Extracted {len(regions)} storm-affected regions")
        self._save_data(regions, "storm_regions.json")
        
        return regions
    
    def get_storm_affected_areas(self, severity_threshold="Moderate"):
        """
        Get comprehensive information about storm-affected areas.
        
        Args:
            severity_threshold (str): Minimum severity level to include
        
        Returns:
            list: List of dictionaries containing region information
        """
        alerts = self.get_active_alerts()
        if not alerts:
            return []
        
        severe_alerts = self.filter_severe_alerts(alerts, severity_threshold)
        regions = self.extract_storm_regions(severe_alerts)
        
        return regions
    
    def _save_data(self, data, filename):
        """
        Save data to a JSON file.
        
        Args:
            data: Data to save
            filename (str): Name of the file
        """
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Data saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving data to {filepath}: {e}")

def main():
    """
    Main function to demonstrate the StormTracker functionality.
    """
    tracker = StormTracker(data_dir="storm_data")
    
    # Get storm-affected areas
    regions = tracker.get_storm_affected_areas(severity_threshold="Moderate")
    
    # Print summary
    print(f"\nFound {len(regions)} storm-affected regions:")
    for i, region in enumerate(regions[:5], 1):
        print(f"{i}. {region['event']} - {region['area_desc']} ({region['severity']} severity)")
    
    if len(regions) > 5:
        print(f"...and {len(regions) - 5} more regions")

if __name__ == "__main__":
    main()
