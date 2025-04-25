#!/usr/bin/env python3
"""
Test script for the Storm Automation System

This script tests the core functionality of the storm tracking and ad campaign components.
"""

import os
import json
import unittest
from unittest.mock import patch, MagicMock
import sys

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from storm_tracker import StormTracker
from ads_campaign_manager import AdsCampaignManager
from storm_automation import StormAutomationSystem

class TestStormTracker(unittest.TestCase):
    """Test cases for the StormTracker class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data_dir = "test_data"
        os.makedirs(self.test_data_dir, exist_ok=True)
        self.tracker = StormTracker(data_dir=self.test_data_dir)
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up test files
        for file in os.listdir(self.test_data_dir):
            os.remove(os.path.join(self.test_data_dir, file))
        os.rmdir(self.test_data_dir)
    
    @patch('requests.get')
    def test_get_active_alerts(self, mock_get):
        """Test fetching active alerts."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "features": [
                {"properties": {"severity": "Severe"}, "geometry": {}}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        alerts = self.tracker.get_active_alerts()
        
        # Verify the API was called correctly
        mock_get.assert_called_once_with(
            "https://api.weather.gov/alerts/active",
            headers=self.tracker.headers
        )
        
        # Verify the response was processed correctly
        self.assertEqual(len(alerts["features"]), 1)
        self.assertEqual(alerts["features"][0]["properties"]["severity"], "Severe")
    
    def test_filter_severe_alerts(self):
        """Test filtering alerts by severity."""
        test_alerts = {
            "features": [
                {"properties": {"severity": "Minor"}},
                {"properties": {"severity": "Moderate"}},
                {"properties": {"severity": "Severe"}},
                {"properties": {"severity": "Extreme"}}
            ]
        }
        
        # Test filtering with different thresholds
        minor_filtered = self.tracker.filter_severe_alerts(test_alerts, "Minor")
        self.assertEqual(len(minor_filtered), 4)
        
        moderate_filtered = self.tracker.filter_severe_alerts(test_alerts, "Moderate")
        self.assertEqual(len(moderate_filtered), 3)
        
        severe_filtered = self.tracker.filter_severe_alerts(test_alerts, "Severe")
        self.assertEqual(len(severe_filtered), 2)
        
        extreme_filtered = self.tracker.filter_severe_alerts(test_alerts, "Extreme")
        self.assertEqual(len(extreme_filtered), 1)
    
    def test_extract_storm_regions(self):
        """Test extracting storm regions from alerts."""
        test_alerts = [
            {
                "properties": {
                    "id": "test-id-1",
                    "event": "Flood",
                    "headline": "Flood Warning",
                    "severity": "Moderate",
                    "certainty": "Likely",
                    "urgency": "Expected",
                    "areaDesc": "Test County",
                    "effective": "2025-04-24T10:00:00Z",
                    "expires": "2025-04-24T16:00:00Z",
                    "description": "Test description"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
                }
            }
        ]
        
        regions = self.tracker.extract_storm_regions(test_alerts)
        
        # Verify regions were extracted correctly
        self.assertEqual(len(regions), 1)
        self.assertEqual(regions[0]["id"], "test-id-1")
        self.assertEqual(regions[0]["event"], "Flood")
        self.assertEqual(regions[0]["severity"], "Moderate")
        self.assertEqual(regions[0]["area_desc"], "Test County")

class TestAdsCampaignManager(unittest.TestCase):
    """Test cases for the AdsCampaignManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data_dir = "test_data"
        os.makedirs(self.test_data_dir, exist_ok=True)
        self.campaign_manager = AdsCampaignManager(data_dir=self.test_data_dir, daily_budget=300)
        
        # Create test storm regions data
        self.test_regions = [
            {
                "id": "test-id-1",
                "event": "Flood",
                "headline": "Flood Warning",
                "severity": "Moderate",
                "certainty": "Likely",
                "urgency": "Expected",
                "area_desc": "Test County",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
                }
            }
        ]
        
        with open(os.path.join(self.test_data_dir, "storm_regions.json"), "w") as f:
            json.dump(self.test_regions, f)
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up test files
        for file in os.listdir(self.test_data_dir):
            os.remove(os.path.join(self.test_data_dir, file))
        os.rmdir(self.test_data_dir)
    
    def test_load_storm_regions(self):
        """Test loading storm regions from file."""
        regions = self.campaign_manager.load_storm_regions()
        
        # Verify regions were loaded correctly
        self.assertEqual(len(regions), 1)
        self.assertEqual(regions[0]["id"], "test-id-1")
        self.assertEqual(regions[0]["event"], "Flood")
    
    def test_create_campaign_for_region(self):
        """Test creating a campaign for a region."""
        campaign = self.campaign_manager.create_campaign_for_region(self.test_regions[0])
        
        # Verify campaign was created correctly
        self.assertEqual(campaign["region_id"], "test-id-1")
        self.assertEqual(campaign["status"], "ENABLED")
        self.assertEqual(campaign["daily_budget"], 300)  # Moderate severity = 1.0 multiplier
        self.assertEqual(campaign["event_type"], "Flood")
        self.assertEqual(campaign["severity"], "Moderate")
        self.assertTrue("Get Paid to Inspect Homes After Flood" in campaign["ad_content"]["headline"])
    
    def test_create_campaigns_for_all_regions(self):
        """Test creating campaigns for all regions."""
        campaigns = self.campaign_manager.create_campaigns_for_all_regions()
        
        # Verify campaigns were created correctly
        self.assertEqual(len(campaigns), 1)
        self.assertEqual(campaigns[0]["region_id"], "test-id-1")
    
    def test_get_campaign_summary(self):
        """Test getting campaign summary."""
        # Create a campaign first
        self.campaign_manager.create_campaign_for_region(self.test_regions[0])
        
        summary = self.campaign_manager.get_campaign_summary()
        
        # Verify summary is correct
        self.assertEqual(summary["total_campaigns"], 1)
        self.assertEqual(summary["active_campaigns"], 1)
        self.assertEqual(summary["total_daily_budget"], 300)
        self.assertEqual(summary["by_severity"]["Moderate"], 1)
        self.assertEqual(summary["by_status"]["ENABLED"], 1)

class TestStormAutomationSystem(unittest.TestCase):
    """Test cases for the StormAutomationSystem class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data_dir = "test_data"
        os.makedirs(self.test_data_dir, exist_ok=True)
        
        # Create a mock system with patched components
        self.storm_tracker_patcher = patch('storm_tracker.StormTracker')
        self.ads_manager_patcher = patch('ads_campaign_manager.AdsCampaignManager')
        
        self.mock_storm_tracker = self.storm_tracker_patcher.start()
        self.mock_ads_manager = self.ads_manager_patcher.start()
        
        # Configure mock return values
        self.mock_storm_tracker.return_value.get_storm_affected_areas.return_value = [
            {"id": "test-id-1", "event": "Flood", "severity": "Moderate", "area_desc": "Test County"}
        ]
        
        self.mock_ads_manager.return_value.create_campaigns_for_all_regions.return_value = [
            {"campaign_id": "test-campaign-1", "region_id": "test-id-1", "status": "ENABLED"}
        ]
        
        self.mock_ads_manager.return_value.get_campaign_summary.return_value = {
            "total_campaigns": 1,
            "active_campaigns": 1,
            "total_daily_budget": 300,
            "by_severity": {"Moderate": 1},
            "by_status": {"ENABLED": 1}
        }
        
        # Create the system with mocked components
        self.system = StormAutomationSystem(data_dir=self.test_data_dir, daily_budget=300)
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Stop the patchers
        self.storm_tracker_patcher.stop()
        self.ads_manager_patcher.stop()
        
        # Clean up test directory
        if os.path.exists(self.test_data_dir):
            for file in os.listdir(self.test_data_dir):
                os.remove(os.path.join(self.test_data_dir, file))
            os.rmdir(self.test_data_dir)
    
    def test_run_storm_tracking(self):
        """Test running storm tracking."""
        regions = self.system.run_storm_tracking("Moderate")
        
        # Verify storm tracker was called correctly
        self.mock_storm_tracker.return_value.get_storm_affected_areas.assert_called_once_with("Moderate")
        
        # Verify regions were returned correctly
        self.assertEqual(len(regions), 1)
        self.assertEqual(regions[0]["id"], "test-id-1")
    
    def test_create_ad_campaigns(self):
        """Test creating ad campaigns."""
        campaigns = self.system.create_ad_campaigns()
        
        # Verify ads manager was called correctly
        self.mock_ads_manager.return_value.create_campaigns_for_all_regions.assert_called_once()
        
        # Verify campaigns were returned correctly
        self.assertEqual(len(campaigns), 1)
        self.assertEqual(campaigns[0]["campaign_id"], "test-campaign-1")
    
    def test_run_full_workflow(self):
        """Test running the full workflow."""
        results = self.system.run_full_workflow("Moderate")
        
        # Verify components were called correctly
        self.mock_storm_tracker.return_value.get_storm_affected_areas.assert_called_once_with("Moderate")
        self.mock_ads_manager.return_value.create_campaigns_for_all_regions.assert_called_once()
        
        # Verify results are correct
        self.assertEqual(results["regions_found"], 1)
        self.assertEqual(results["campaigns_created"], 1)
        self.assertEqual(results["severity_threshold"], "Moderate")

if __name__ == "__main__":
    unittest.main()
