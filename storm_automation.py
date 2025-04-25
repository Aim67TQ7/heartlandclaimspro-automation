#!/usr/bin/env python3
"""
Storm Automation System - Main Controller

This script coordinates the entire storm automation workflow:
1. Track storms using the National Weather Service API
2. Create targeted Google Ads campaigns for affected regions
3. Manage the photo collection and processing workflow
4. Handle Xactimate integration and submission

Usage:
    python storm_automation.py
"""

import os
import logging
import argparse
import time
from datetime import datetime

# Import our modules
from storm_tracker import StormTracker
from ads_campaign_manager import AdsCampaignManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("storm_automation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("storm_automation")

class StormAutomationSystem:
    """
    Main controller for the Storm Automation System.
    """
    
    def __init__(self, data_dir="storm_data", daily_budget=300):
        """
        Initialize the Storm Automation System.
        
        Args:
            data_dir (str): Directory to store data
            daily_budget (float): Daily budget for ad campaigns in USD
        """
        self.data_dir = data_dir
        self.daily_budget = daily_budget
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize components
        self.storm_tracker = StormTracker(data_dir=data_dir)
        self.ads_manager = AdsCampaignManager(data_dir=data_dir, daily_budget=daily_budget)
        
        logger.info("Storm Automation System initialized")
    
    def run_storm_tracking(self, severity_threshold="Moderate"):
        """
        Run the storm tracking process.
        
        Args:
            severity_threshold (str): Minimum severity level to include
        
        Returns:
            list: Storm-affected regions
        """
        logger.info(f"Starting storm tracking with severity threshold: {severity_threshold}")
        regions = self.storm_tracker.get_storm_affected_areas(severity_threshold)
        
        if regions:
            logger.info(f"Found {len(regions)} storm-affected regions")
        else:
            logger.info("No storm-affected regions found")
        
        return regions
    
    def create_ad_campaigns(self):
        """
        Create targeted ad campaigns for storm-affected regions.
        
        Returns:
            list: Created campaigns
        """
        logger.info("Creating targeted ad campaigns for storm-affected regions")
        campaigns = self.ads_manager.create_campaigns_for_all_regions()
        
        if campaigns:
            logger.info(f"Created/updated {len(campaigns)} ad campaigns")
            
            # Get campaign summary
            summary = self.ads_manager.get_campaign_summary()
            logger.info(f"Campaign summary: {summary}")
        else:
            logger.info("No ad campaigns created")
        
        return campaigns
    
    def run_full_workflow(self, severity_threshold="Moderate"):
        """
        Run the complete storm automation workflow.
        
        Args:
            severity_threshold (str): Minimum severity level to include
        
        Returns:
            dict: Workflow results
        """
        start_time = datetime.now()
        logger.info(f"Starting full storm automation workflow at {start_time}")
        
        # Step 1: Track storms
        regions = self.run_storm_tracking(severity_threshold)
        
        # Step 2: Create ad campaigns
        campaigns = self.create_ad_campaigns()
        
        # Future steps will be implemented here:
        # - Photo collection workflow
        # - AI damage assessment
        # - Xactimate integration
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        results = {
            "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_seconds": duration,
            "regions_found": len(regions),
            "campaigns_created": len(campaigns),
            "severity_threshold": severity_threshold
        }
        
        logger.info(f"Completed full workflow in {duration:.2f} seconds")
        return results

def main():
    """
    Main function to run the Storm Automation System.
    """
    parser = argparse.ArgumentParser(description="Storm Automation System")
    parser.add_argument("--data-dir", default="storm_data", help="Directory to store data")
    parser.add_argument("--budget", type=float, default=300, help="Daily budget for ad campaigns in USD")
    parser.add_argument("--severity", default="Moderate", choices=["Minor", "Moderate", "Severe", "Extreme"],
                        help="Minimum severity threshold for storm alerts")
    parser.add_argument("--track-only", action="store_true", help="Only run storm tracking, skip ad campaigns")
    args = parser.parse_args()
    
    system = StormAutomationSystem(data_dir=args.data_dir, daily_budget=args.budget)
    
    if args.track_only:
        print(f"\nRunning storm tracking with severity threshold: {args.severity}")
        regions = system.run_storm_tracking(args.severity)
        
        print(f"\nFound {len(regions)} storm-affected regions:")
        for i, region in enumerate(regions[:5], 1):
            print(f"{i}. {region['event']} - {region['area_desc']} ({region['severity']} severity)")
        
        if len(regions) > 5:
            print(f"...and {len(regions) - 5} more regions")
    else:
        print(f"\nRunning full storm automation workflow with severity threshold: {args.severity}")
        results = system.run_full_workflow(args.severity)
        
        print("\nWorkflow Results:")
        print(f"Start Time: {results['start_time']}")
        print(f"End Time: {results['end_time']}")
        print(f"Duration: {results['duration_seconds']:.2f} seconds")
        print(f"Regions Found: {results['regions_found']}")
        print(f"Campaigns Created: {results['campaigns_created']}")
        
        # Print campaign summary if campaigns were created
        if results['campaigns_created'] > 0:
            summary = system.ads_manager.get_campaign_summary()
            print("\nCampaign Summary:")
            print(f"Total Campaigns: {summary['total_campaigns']}")
            print(f"Active Campaigns: {summary['active_campaigns']}")
            print(f"Total Daily Budget: ${summary['total_daily_budget']:.2f}")
            
            print("\nCampaigns by Severity:")
            for severity, count in summary['by_severity'].items():
                print(f"  {severity}: {count}")

if __name__ == "__main__":
    main()
