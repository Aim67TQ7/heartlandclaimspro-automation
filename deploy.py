#!/usr/bin/env python3
"""
Storm Automation System - Deployment Script

This script handles the deployment of the Storm Automation System,
setting up the necessary directories, installing dependencies,
and starting the required services.
"""

import os
import sys
import subprocess
import argparse
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("deployment.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("deployment")

class Deployment:
    """
    A class to handle deployment of the Storm Automation System.
    """
    
    def __init__(self, base_dir="/home/ubuntu/storm_automation"):
        """
        Initialize the Deployment.
        
        Args:
            base_dir (str): Base directory for the storm automation system
        """
        self.base_dir = base_dir
        self.src_dir = os.path.join(base_dir, "src")
        self.data_dir = os.path.join(base_dir, "data")
        
        logger.info("Deployment initialized")
    
    def check_dependencies(self):
        """
        Check if all required dependencies are installed.
        
        Returns:
            bool: True if all dependencies are installed, False otherwise
        """
        logger.info("Checking dependencies")
        
        # Check if Python is installed
        try:
            subprocess.run(["python3", "--version"], check=True, capture_output=True)
            logger.info("Python is installed")
        except subprocess.CalledProcessError:
            logger.error("Python is not installed")
            return False
        
        # Check if pip is installed
        try:
            subprocess.run(["pip3", "--version"], check=True, capture_output=True)
            logger.info("pip is installed")
        except subprocess.CalledProcessError:
            logger.error("pip is not installed")
            return False
        
        # Check if required packages are installed
        requirements_file = os.path.join(self.base_dir, "requirements.txt")
        if not os.path.exists(requirements_file):
            logger.error(f"Requirements file not found: {requirements_file}")
            return False
        
        logger.info("All dependencies are available")
        return True
    
    def install_dependencies(self):
        """
        Install all required dependencies.
        
        Returns:
            bool: True if installation was successful, False otherwise
        """
        logger.info("Installing dependencies")
        
        requirements_file = os.path.join(self.base_dir, "requirements.txt")
        
        try:
            subprocess.run(["pip3", "install", "-r", requirements_file], check=True)
            logger.info("Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error installing dependencies: {e}")
            return False
    
    def create_directories(self):
        """
        Create all necessary directories for the system.
        
        Returns:
            bool: True if directory creation was successful, False otherwise
        """
        logger.info("Creating directories")
        
        try:
            # Create main data directory
            os.makedirs(self.data_dir, exist_ok=True)
            
            # Create subdirectories
            os.makedirs(os.path.join(self.data_dir, "storm_data"), exist_ok=True)
            os.makedirs(os.path.join(self.data_dir, "photo_uploads"), exist_ok=True)
            os.makedirs(os.path.join(self.data_dir, "photo_uploads", "metadata"), exist_ok=True)
            os.makedirs(os.path.join(self.data_dir, "damage_reports"), exist_ok=True)
            os.makedirs(os.path.join(self.data_dir, "xactimate_claims"), exist_ok=True)
            os.makedirs(os.path.join(self.data_dir, "payment_records"), exist_ok=True)
            
            logger.info("Directories created successfully")
            return True
        except Exception as e:
            logger.error(f"Error creating directories: {e}")
            return False
    
    def start_services(self, port=5000):
        """
        Start all required services.
        
        Args:
            port (int): Port to run the photo collection API on
        
        Returns:
            dict: Dictionary of started processes
        """
        logger.info("Starting services")
        
        processes = {}
        
        try:
            # Start photo collection API
            api_script = os.path.join(self.src_dir, "photo_collection_api.py")
            api_log = open(os.path.join(self.base_dir, "photo_api.log"), "w")
            
            api_process = subprocess.Popen(
                ["python3", api_script, "--host", "0.0.0.0", "--port", str(port)],
                stdout=api_log,
                stderr=api_log
            )
            
            processes["photo_api"] = {
                "process": api_process,
                "log_file": api_log,
                "port": port
            }
            
            logger.info(f"Photo Collection API started on port {port}")
            
            # Note: In a production environment, you would also set up
            # services to run the storm tracking, damage assessment,
            # and other components on a schedule or as daemons.
            
            return processes
        
        except Exception as e:
            logger.error(f"Error starting services: {e}")
            
            # Clean up any started processes
            for service_name, service_info in processes.items():
                service_info["process"].terminate()
                service_info["log_file"].close()
            
            return {}
    
    def stop_services(self, processes):
        """
        Stop all running services.
        
        Args:
            processes (dict): Dictionary of processes to stop
        
        Returns:
            bool: True if all services were stopped successfully, False otherwise
        """
        logger.info("Stopping services")
        
        try:
            for service_name, service_info in processes.items():
                service_info["process"].terminate()
                service_info["log_file"].close()
                logger.info(f"Service {service_name} stopped")
            
            logger.info("All services stopped successfully")
            return True
        except Exception as e:
            logger.error(f"Error stopping services: {e}")
            return False
    
    def run_tests(self):
        """
        Run integration tests to verify the deployment.
        
        Returns:
            bool: True if tests passed, False otherwise
        """
        logger.info("Running integration tests")
        
        test_script = os.path.join(self.base_dir, "tests", "integration_test.py")
        
        try:
            result = subprocess.run(["python3", test_script], check=True, capture_output=True, text=True)
            logger.info("Integration tests passed")
            logger.info(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Integration tests failed: {e}")
            logger.error(e.stdout)
            logger.error(e.stderr)
            return False
    
    def deploy(self, run_tests=True, start_services=True, port=5000):
        """
        Deploy the complete system.
        
        Args:
            run_tests (bool): Whether to run integration tests
            start_services (bool): Whether to start services
            port (int): Port to run the photo collection API on
        
        Returns:
            dict: Deployment results
        """
        logger.info("Starting deployment")
        
        # Check dependencies
        if not self.check_dependencies():
            return {
                "success": False,
                "error": "Dependency check failed",
                "timestamp": datetime.now().isoformat()
            }
        
        # Install dependencies
        if not self.install_dependencies():
            return {
                "success": False,
                "error": "Dependency installation failed",
                "timestamp": datetime.now().isoformat()
            }
        
        # Create directories
        if not self.create_directories():
            return {
                "success": False,
                "error": "Directory creation failed",
                "timestamp": datetime.now().isoformat()
            }
        
        # Run tests if requested
        if run_tests:
            if not self.run_tests():
                return {
                    "success": False,
                    "error": "Integration tests failed",
                    "timestamp": datetime.now().isoformat()
                }
        
        # Start services if requested
        processes = {}
        if start_services:
            processes = self.start_services(port=port)
            if not processes:
                return {
                    "success": False,
                    "error": "Service startup failed",
                    "timestamp": datetime.now().isoformat()
                }
        
        logger.info("Deployment completed successfully")
        
        return {
            "success": True,
            "processes": processes,
            "timestamp": datetime.now().isoformat(),
            "services": {
                "photo_api": f"http://localhost:{port}" if start_services else None
            }
        }

def main():
    """
    Main function to run the deployment.
    """
    parser = argparse.ArgumentParser(description="Storm Automation System Deployment")
    parser.add_argument("--base-dir", default="/home/ubuntu/storm_automation", help="Base directory for the storm automation system")
    parser.add_argument("--port", type=int, default=5000, help="Port to run the photo collection API on")
    parser.add_argument("--no-tests", action="store_true", help="Skip running integration tests")
    parser.add_argument("--no-services", action="store_true", help="Skip starting services")
    args = parser.parse_args()
    
    deployment = Deployment(base_dir=args.base_dir)
    
    result = deployment.deploy(
        run_tests=not args.no_tests,
        start_services=not args.no_services,
        port=args.port
    )
    
    if result["success"]:
        print("\nDeployment completed successfully!")
        
        if "services" in result and result["services"]["photo_api"]:
            print(f"\nPhoto Collection API is running at: {result['services']['photo_api']}")
            print("Use Ctrl+C to stop the services")
            
            try:
                # Keep the script running to maintain the services
                while True:
                    pass
            except KeyboardInterrupt:
                print("\nStopping services...")
                deployment.stop_services(result["processes"])
                print("Services stopped")
    else:
        print(f"\nDeployment failed: {result['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
