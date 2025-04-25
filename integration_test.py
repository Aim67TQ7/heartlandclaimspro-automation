#!/usr/bin/env python3
"""
System Integration Test Script

This script tests the complete storm automation workflow by running all components
in sequence and verifying the results at each stage.
"""

import os
import sys
import json
import logging
import argparse
import time
from datetime import datetime

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import our modules
from storm_tracker import StormTracker
from ads_campaign_manager import AdsCampaignManager
from storm_automation import StormAutomationSystem
from damage_assessment import DamageAssessment
from xactimate_integration import XactimateIntegration
from payment_processing import PaymentProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("integration_test.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("integration_test")

class IntegrationTest:
    """
    A class to run integration tests for the complete storm automation system.
    """
    
    def __init__(self, base_dir="/home/ubuntu/storm_automation"):
        """
        Initialize the IntegrationTest.
        
        Args:
            base_dir (str): Base directory for the storm automation system
        """
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, "test_data")
        
        # Create test data directory
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize components
        self.storm_tracker = StormTracker(data_dir=self.data_dir)
        self.ads_manager = AdsCampaignManager(data_dir=self.data_dir, daily_budget=300)
        self.system = StormAutomationSystem(data_dir=self.data_dir, daily_budget=300)
        self.damage_assessment = DamageAssessment(
            data_dir=os.path.join(self.data_dir, "photo_uploads"),
            output_dir=os.path.join(self.data_dir, "damage_reports")
        )
        self.xactimate = XactimateIntegration(
            data_dir=os.path.join(self.data_dir, "damage_reports"),
            output_dir=os.path.join(self.data_dir, "xactimate_claims")
        )
        self.payment_processor = PaymentProcessor(
            claims_dir=os.path.join(self.data_dir, "xactimate_claims"),
            output_dir=os.path.join(self.data_dir, "payment_records")
        )
        
        logger.info("IntegrationTest initialized")
    
    def setup_test_data(self):
        """
        Set up test data for the integration test.
        
        Returns:
            bool: Success status
        """
        logger.info("Setting up test data")
        
        # Create directories
        os.makedirs(os.path.join(self.data_dir, "photo_uploads"), exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "photo_uploads", "metadata"), exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "damage_reports"), exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "xactimate_claims"), exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "payment_records"), exist_ok=True)
        
        # Create a mock storm alert
        mock_alert = {
            "features": [
                {
                    "properties": {
                        "id": "test-alert-001",
                        "event": "Severe Thunderstorm",
                        "headline": "Severe Thunderstorm Warning",
                        "severity": "Severe",
                        "certainty": "Observed",
                        "urgency": "Immediate",
                        "areaDesc": "Test County, Test State",
                        "effective": "2025-04-24T10:00:00Z",
                        "expires": "2025-04-24T16:00:00Z",
                        "description": "Test severe thunderstorm with damaging winds and hail."
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
                    }
                }
            ]
        }
        
        # Save mock alert
        with open(os.path.join(self.data_dir, "active_alerts.json"), "w") as f:
            json.dump(mock_alert, f, indent=2)
        
        # Create a mock photo upload
        job_id = "test-job-001"
        photo_id = "test-photo-001"
        
        # Create job directory
        os.makedirs(os.path.join(self.data_dir, "photo_uploads", job_id), exist_ok=True)
        
        # Create a mock photo file (empty file)
        with open(os.path.join(self.data_dir, "photo_uploads", job_id, f"{photo_id}.jpg"), "w") as f:
            f.write("Mock photo content")
        
        # Create photo metadata
        metadata = {
            "photo_id": photo_id,
            "job_id": job_id,
            "contractor_id": "test-contractor-001",
            "original_filename": "test_photo.jpg",
            "file_size_bytes": 1024,
            "upload_time": datetime.now().isoformat(),
            "location": {
                "latitude": "35.1234",
                "longitude": "-80.5678",
                "accuracy": "10.0"
            },
            "device_info": {
                "model": "Test Device",
                "os_version": "1.0",
                "app_version": "1.0"
            },
            "damage_type": "roof",
            "notes": "Test photo for integration testing"
        }
        
        # Save metadata
        with open(os.path.join(self.data_dir, "photo_uploads", "metadata", f"{photo_id}.json"), "w") as f:
            json.dump(metadata, f, indent=2)
        
        logger.info("Test data setup complete")
        return True
    
    def test_storm_tracking(self):
        """
        Test the storm tracking component.
        
        Returns:
            bool: Success status
        """
        logger.info("Testing storm tracking")
        
        try:
            # Get storm-affected areas
            regions = self.storm_tracker.get_storm_affected_areas(severity_threshold="Moderate")
            
            if not regions:
                logger.error("No storm regions found")
                return False
            
            logger.info(f"Found {len(regions)} storm regions")
            return True
        
        except Exception as e:
            logger.error(f"Error testing storm tracking: {e}")
            return False
    
    def test_ads_campaign(self):
        """
        Test the ads campaign component.
        
        Returns:
            bool: Success status
        """
        logger.info("Testing ads campaign creation")
        
        try:
            # Create campaigns
            campaigns = self.ads_manager.create_campaigns_for_all_regions()
            
            if not campaigns:
                logger.error("No campaigns created")
                return False
            
            logger.info(f"Created {len(campaigns)} campaigns")
            return True
        
        except Exception as e:
            logger.error(f"Error testing ads campaign: {e}")
            return False
    
    def test_damage_assessment(self):
        """
        Test the damage assessment component.
        
        Returns:
            bool: Success status
        """
        logger.info("Testing damage assessment")
        
        try:
            # Process photos
            results = self.damage_assessment.process_pending_photos()
            
            if not results:
                logger.error("No assessment results generated")
                return False
            
            logger.info(f"Generated {len(results)} assessment results")
            
            # Generate job summary
            job_id = "test-job-001"
            summary = self.damage_assessment.generate_job_summary(job_id)
            
            if not summary:
                logger.error(f"No summary generated for job {job_id}")
                return False
            
            logger.info(f"Generated summary for job {job_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error testing damage assessment: {e}")
            return False
    
    def test_xactimate_integration(self):
        """
        Test the Xactimate integration component.
        
        Returns:
            bool: Success status
        """
        logger.info("Testing Xactimate integration")
        
        try:
            # Get ready jobs
            ready_jobs = self.xactimate.get_ready_jobs()
            
            if not ready_jobs:
                logger.error("No jobs ready for Xactimate")
                return False
            
            logger.info(f"Found {len(ready_jobs)} jobs ready for Xactimate")
            
            # Process jobs
            results = []
            for job_id in ready_jobs:
                result = self.xactimate.process_job(job_id)
                if result:
                    results.append(result)
            
            if not results:
                logger.error("No Xactimate submissions created")
                return False
            
            logger.info(f"Created {len(results)} Xactimate submissions")
            
            # Check submission status
            for result in results:
                job_id = result['job_id']
                status = self.xactimate.check_submission_status(job_id)
                logger.info(f"Submission status for job {job_id}: {status['status']}")
            
            return True
        
        except Exception as e:
            logger.error(f"Error testing Xactimate integration: {e}")
            return False
    
    def test_payment_processing(self):
        """
        Test the payment processing component.
        
        Returns:
            bool: Success status
        """
        logger.info("Testing payment processing")
        
        try:
            # Get approved claims
            approved_claims = self.payment_processor.get_approved_claims()
            
            if not approved_claims:
                logger.error("No approved claims found")
                return False
            
            logger.info(f"Found {len(approved_claims)} approved claims")
            
            # Process payments
            payments = []
            for claim_info in approved_claims:
                payment = self.payment_processor.process_payment(claim_info)
                if payment:
                    payments.append(payment)
                    
                    # Notify contractor
                    self.payment_processor.notify_contractor(payment)
            
            if not payments:
                logger.error("No payments processed")
                return False
            
            logger.info(f"Processed {len(payments)} payments")
            
            # Generate report
            report = self.payment_processor.generate_payment_report()
            
            if not report:
                logger.error("No payment report generated")
                return False
            
            logger.info("Generated payment report")
            return True
        
        except Exception as e:
            logger.error(f"Error testing payment processing: {e}")
            return False
    
    def test_full_workflow(self):
        """
        Test the complete workflow from start to finish.
        
        Returns:
            bool: Success status
        """
        logger.info("Testing full workflow")
        
        try:
            # Run the full workflow
            results = self.system.run_full_workflow(severity_threshold="Moderate")
            
            if not results:
                logger.error("Full workflow failed")
                return False
            
            logger.info("Full workflow completed successfully")
            logger.info(f"Results: {results}")
            
            # Test damage assessment
            if not self.test_damage_assessment():
                logger.error("Damage assessment failed")
                return False
            
            # Test Xactimate integration
            if not self.test_xactimate_integration():
                logger.error("Xactimate integration failed")
                return False
            
            # Test payment processing
            if not self.test_payment_processing():
                logger.error("Payment processing failed")
                return False
            
            logger.info("Full workflow test completed successfully")
            return True
        
        except Exception as e:
            logger.error(f"Error testing full workflow: {e}")
            return False
    
    def run_all_tests(self):
        """
        Run all integration tests.
        
        Returns:
            dict: Test results
        """
        logger.info("Running all integration tests")
        
        # Set up test data
        if not self.setup_test_data():
            logger.error("Failed to set up test data")
            return {"success": False, "error": "Failed to set up test data"}
        
        # Run tests
        test_results = {
            "storm_tracking": self.test_storm_tracking(),
            "ads_campaign": self.test_ads_campaign(),
            "damage_assessment": self.test_damage_assessment(),
            "xactimate_integration": self.test_xactimate_integration(),
            "payment_processing": self.test_payment_processing(),
            "full_workflow": self.test_full_workflow()
        }
        
        # Calculate overall success
        overall_success = all(test_results.values())
        
        logger.info(f"All tests completed. Overall success: {overall_success}")
        
        return {
            "success": overall_success,
            "results": test_results,
            "timestamp": datetime.now().isoformat()
        }

def main():
    """
    Main function to run the integration tests.
    """
    parser = argparse.ArgumentParser(description="Storm Automation Integration Tests")
    parser.add_argument("--base-dir", default="/home/ubuntu/storm_automation", help="Base directory for the storm automation system")
    parser.add_argument("--test", choices=["storm", "ads", "damage", "xactimate", "payment", "full", "all"], default="all", help="Test to run")
    args = parser.parse_args()
    
    test = IntegrationTest(base_dir=args.base_dir)
    
    if args.test == "storm":
        success = test.test_storm_tracking()
        print(f"Storm tracking test {'succeeded' if success else 'failed'}")
    
    elif args.test == "ads":
        success = test.test_ads_campaign()
        print(f"Ads campaign test {'succeeded' if success else 'failed'}")
    
    elif args.test == "damage":
        success = test.test_damage_assessment()
        print(f"Damage assessment test {'succeeded' if success else 'failed'}")
    
    elif args.test == "xactimate":
        success = test.test_xactimate_integration()
        print(f"Xactimate integration test {'succeeded' if success else 'failed'}")
    
    elif args.test == "payment":
        success = test.test_payment_processing()
        print(f"Payment processing test {'succeeded' if success else 'failed'}")
    
    elif args.test == "full":
        success = test.test_full_workflow()
        print(f"Full workflow test {'succeeded' if success else 'failed'}")
    
    else:  # all
        results = test.run_all_tests()
        
        print("\nIntegration Test Results:")
        print(f"Overall Success: {'Yes' if results['success'] else 'No'}")
        
        print("\nComponent Tests:")
        for component, success in results['results'].items():
            print(f"  {component}: {'Passed' if success else 'Failed'}")

if __name__ == "__main__":
    main()
