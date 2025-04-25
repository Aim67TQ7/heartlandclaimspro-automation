#!/usr/bin/env python3
"""
Google Ads Campaign Manager

This module creates and manages targeted Google Ads campaigns for storm-affected regions.
It uses geographic data from the StormTracker to create precisely targeted campaigns.
"""

import os
import json
import logging
from datetime import datetime, timedelta
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ads_campaign.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ads_campaign")

class AdsCampaignManager:
    """
    A class to create and manage targeted Google Ads campaigns for storm-affected regions.
    
    Note: This is a simulation of the Google Ads API integration. In a production environment,
    this would use the actual Google Ads API client library.
    """
    
    def __init__(self, data_dir="storm_data", daily_budget=300):
        """
        Initialize the AdsCampaignManager.
        
        Args:
            data_dir (str): Directory containing storm data
            daily_budget (float): Daily budget for ad campaigns in USD
        """
        self.data_dir = data_dir
        self.daily_budget = daily_budget
        self.campaigns_file = os.path.join(data_dir, "active_campaigns.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Load existing campaigns if available
        self.active_campaigns = self._load_campaigns()
        
        logger.info(f"AdsCampaignManager initialized with ${daily_budget}/day budget")
    
    def _load_campaigns(self):
        """
        Load existing campaigns from file.
        
        Returns:
            dict: Dictionary of active campaigns
        """
        if not os.path.exists(self.campaigns_file):
            return {}
        
        try:
            with open(self.campaigns_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading campaigns: {e}")
            return {}
    
    def _save_campaigns(self):
        """
        Save active campaigns to file.
        """
        try:
            with open(self.campaigns_file, 'w') as f:
                json.dump(self.active_campaigns, f, indent=2)
            logger.info(f"Campaigns saved to {self.campaigns_file}")
        except Exception as e:
            logger.error(f"Error saving campaigns: {e}")
    
    def load_storm_regions(self):
        """
        Load storm region data from the StormTracker output.
        
        Returns:
            list: List of storm region dictionaries
        """
        regions_file = os.path.join(self.data_dir, "storm_regions.json")
        
        if not os.path.exists(regions_file):
            logger.warning(f"Storm regions file not found: {regions_file}")
            return []
        
        try:
            with open(regions_file, 'r') as f:
                regions = json.load(f)
            logger.info(f"Loaded {len(regions)} storm regions from {regions_file}")
            return regions
        except Exception as e:
            logger.error(f"Error loading storm regions: {e}")
            return []
    
    def create_campaign_for_region(self, region):
        """
        Create a Google Ads campaign for a specific storm-affected region.
        
        Args:
            region (dict): Storm region information
        
        Returns:
            dict: Campaign information
        """
        region_id = region.get("id")
        event_type = region.get("event")
        area_desc = region.get("area_desc")
        severity = region.get("severity")
        
        # Check if campaign already exists for this region
        if region_id in self.active_campaigns:
            logger.info(f"Campaign already exists for region {region_id}")
            return self.active_campaigns[region_id]
        
        # Create a new campaign
        campaign_id = str(uuid.uuid4())
        campaign_name = f"Storm Damage - {event_type} - {area_desc}"
        
        # Calculate budget based on severity
        severity_multiplier = {
            "Minor": 0.5,
            "Moderate": 1.0,
            "Severe": 1.5,
            "Extreme": 2.0
        }.get(severity, 1.0)
        
        campaign_budget = self.daily_budget * severity_multiplier
        
        # Create ad content
        headline = f"Get Paid to Inspect Homes After {event_type} in {area_desc}"
        description = "Take photos after storms. No roof climbing. Fast pay. Apply in under 5 mins."
        
        # Create campaign object
        campaign = {
            "campaign_id": campaign_id,
            "region_id": region_id,
            "name": campaign_name,
            "status": "ENABLED",
            "daily_budget": campaign_budget,
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "targeting": {
                "geo_targeting": {
                    "type": "POLYGON",
                    "coordinates": region.get("geometry", {}).get("coordinates", [])
                },
                "area_desc": area_desc
            },
            "ad_content": {
                "headline": headline,
                "description": description,
                "call_to_action": "Apply Now",
                "final_url": "https://example.com/storm-inspector-signup"
            },
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event_type": event_type,
            "severity": severity
        }
        
        # In a real implementation, this would call the Google Ads API
        # to create the campaign with proper geo-targeting
        
        # Add to active campaigns
        self.active_campaigns[region_id] = campaign
        self._save_campaigns()
        
        logger.info(f"Created campaign '{campaign_name}' with ${campaign_budget}/day budget")
        return campaign
    
    def create_campaigns_for_all_regions(self):
        """
        Create Google Ads campaigns for all storm-affected regions.
        
        Returns:
            list: List of created campaigns
        """
        regions = self.load_storm_regions()
        if not regions:
            logger.warning("No storm regions found to create campaigns for")
            return []
        
        created_campaigns = []
        for region in regions:
            campaign = self.create_campaign_for_region(region)
            created_campaigns.append(campaign)
        
        logger.info(f"Created/updated {len(created_campaigns)} campaigns for storm-affected regions")
        return created_campaigns
    
    def update_campaign_status(self, region_id, status):
        """
        Update the status of an existing campaign.
        
        Args:
            region_id (str): ID of the region/campaign to update
            status (str): New status (ENABLED, PAUSED, REMOVED)
        
        Returns:
            bool: Success status
        """
        if region_id not in self.active_campaigns:
            logger.warning(f"Campaign for region {region_id} not found")
            return False
        
        self.active_campaigns[region_id]["status"] = status
        self._save_campaigns()
        
        logger.info(f"Updated campaign for region {region_id} to status {status}")
        return True
    
    def get_active_campaigns(self):
        """
        Get all active campaigns.
        
        Returns:
            list: List of active campaign dictionaries
        """
        active = [c for c in self.active_campaigns.values() if c["status"] == "ENABLED"]
        logger.info(f"Retrieved {len(active)} active campaigns")
        return active
    
    def get_campaign_summary(self):
        """
        Get a summary of all campaigns.
        
        Returns:
            dict: Campaign summary statistics
        """
        campaigns = list(self.active_campaigns.values())
        
        total_budget = sum(c["daily_budget"] for c in campaigns if c["status"] == "ENABLED")
        
        by_severity = {}
        for c in campaigns:
            severity = c["severity"]
            if severity not in by_severity:
                by_severity[severity] = 0
            by_severity[severity] += 1
        
        by_status = {}
        for c in campaigns:
            status = c["status"]
            if status not in by_status:
                by_status[status] = 0
            by_status[status] += 1
        
        summary = {
            "total_campaigns": len(campaigns),
            "active_campaigns": len([c for c in campaigns if c["status"] == "ENABLED"]),
            "total_daily_budget": total_budget,
            "by_severity": by_severity,
            "by_status": by_status
        }
        
        return summary

def main():
    """
    Main function to demonstrate the AdsCampaignManager functionality.
    """
    campaign_manager = AdsCampaignManager(data_dir="storm_data", daily_budget=300)
    
    # Create campaigns for all storm regions
    campaigns = campaign_manager.create_campaigns_for_all_regions()
    
    # Print summary
    if campaigns:
        summary = campaign_manager.get_campaign_summary()
        print("\nCampaign Summary:")
        print(f"Total Campaigns: {summary['total_campaigns']}")
        print(f"Active Campaigns: {summary['active_campaigns']}")
        print(f"Total Daily Budget: ${summary['total_daily_budget']:.2f}")
        
        print("\nCampaigns by Severity:")
        for severity, count in summary['by_severity'].items():
            print(f"  {severity}: {count}")
        
        print("\nCampaigns by Status:")
        for status, count in summary['by_status'].items():
            print(f"  {status}: {count}")
    else:
        print("No campaigns created. Make sure to run the StormTracker first to generate storm region data.")

if __name__ == "__main__":
    main()
