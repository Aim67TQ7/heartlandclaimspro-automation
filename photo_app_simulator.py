#!/usr/bin/env python3
"""
Mobile App Simulator for Photo Collection

This script simulates the mobile app that contractors would use to submit photos.
It provides a command-line interface to interact with the Photo Collection API.
"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime
import uuid

class PhotoAppSimulator:
    """
    A class to simulate the mobile app for contractors to submit photos.
    """
    
    def __init__(self, api_url="http://localhost:5000"):
        """
        Initialize the PhotoAppSimulator.
        
        Args:
            api_url (str): URL of the Photo Collection API
        """
        self.api_url = api_url
        self.contractor_id = None
        self.token = None
        self.contractor_name = None
        self.jobs = []
    
    def login(self, email, password):
        """
        Log in to the system.
        
        Args:
            email (str): Contractor's email
            password (str): Contractor's password
        
        Returns:
            bool: Success status
        """
        url = f"{self.api_url}/api/contractor/login"
        
        try:
            response = requests.post(url, json={
                "email": email,
                "password": password
            })
            
            if response.status_code == 200:
                data = response.json()
                self.contractor_id = data["contractor_id"]
                self.token = data["token"]
                self.contractor_name = data["name"]
                print(f"\nWelcome, {self.contractor_name}!")
                return True
            else:
                print(f"\nLogin failed: {response.json().get('error', 'Unknown error')}")
                return False
        
        except requests.exceptions.RequestException as e:
            print(f"\nError connecting to API: {e}")
            return False
    
    def get_jobs(self):
        """
        Get active jobs for the contractor.
        
        Returns:
            bool: Success status
        """
        if not self.contractor_id:
            print("\nYou must log in first.")
            return False
        
        url = f"{self.api_url}/api/contractor/jobs"
        
        try:
            response = requests.get(url, headers={
                "X-Contractor-ID": self.contractor_id
            })
            
            if response.status_code == 200:
                data = response.json()
                self.jobs = data["jobs"]
                
                print("\nYour active jobs:")
                for i, job in enumerate(self.jobs, 1):
                    print(f"{i}. {job['address']} - {job['storm_type']} ({job['status']})")
                
                return True
            else:
                print(f"\nFailed to get jobs: {response.json().get('error', 'Unknown error')}")
                return False
        
        except requests.exceptions.RequestException as e:
            print(f"\nError connecting to API: {e}")
            return False
    
    def upload_photo(self, job_index, photo_path, metadata=None):
        """
        Upload a photo for a job.
        
        Args:
            job_index (int): Index of the job (1-based)
            photo_path (str): Path to the photo file
            metadata (dict): Additional metadata for the photo
        
        Returns:
            bool: Success status
        """
        if not self.contractor_id:
            print("\nYou must log in first.")
            return False
        
        if not self.jobs:
            print("\nYou must get jobs first.")
            return False
        
        if job_index < 1 or job_index > len(self.jobs):
            print(f"\nInvalid job index. Please choose between 1 and {len(self.jobs)}.")
            return False
        
        if not os.path.exists(photo_path):
            print(f"\nPhoto file not found: {photo_path}")
            return False
        
        job = self.jobs[job_index - 1]
        job_id = job["job_id"]
        
        url = f"{self.api_url}/api/photos/upload"
        
        # Default metadata
        form_data = {
            "job_id": job_id,
            "damage_type": metadata.get("damage_type", "Unknown"),
            "notes": metadata.get("notes", ""),
            "latitude": metadata.get("latitude", "0.0"),
            "longitude": metadata.get("longitude", "0.0"),
            "accuracy": metadata.get("accuracy", "0.0"),
            "device_model": metadata.get("device_model", "Simulator"),
            "os_version": metadata.get("os_version", "1.0"),
            "app_version": metadata.get("app_version", "1.0")
        }
        
        try:
            with open(photo_path, 'rb') as f:
                files = {'photo': f}
                response = requests.post(
                    url,
                    headers={"X-Contractor-ID": self.contractor_id},
                    data=form_data,
                    files=files
                )
            
            if response.status_code == 200:
                data = response.json()
                print(f"\nPhoto uploaded successfully!")
                print(f"Photo ID: {data['photo_id']}")
                print(f"Status: {data['status']}")
                print(f"Message: {data['message']}")
                return True
            else:
                print(f"\nFailed to upload photo: {response.json().get('error', 'Unknown error')}")
                return False
        
        except requests.exceptions.RequestException as e:
            print(f"\nError connecting to API: {e}")
            return False
    
    def view_job_photos(self, job_index):
        """
        View all photos for a job.
        
        Args:
            job_index (int): Index of the job (1-based)
        
        Returns:
            bool: Success status
        """
        if not self.contractor_id:
            print("\nYou must log in first.")
            return False
        
        if not self.jobs:
            print("\nYou must get jobs first.")
            return False
        
        if job_index < 1 or job_index > len(self.jobs):
            print(f"\nInvalid job index. Please choose between 1 and {len(self.jobs)}.")
            return False
        
        job = self.jobs[job_index - 1]
        job_id = job["job_id"]
        
        url = f"{self.api_url}/api/photos/{job_id}"
        
        try:
            response = requests.get(url, headers={
                "X-Contractor-ID": self.contractor_id
            })
            
            if response.status_code == 200:
                data = response.json()
                photos = data["photos"]
                
                print(f"\nPhotos for job at {job['address']}:")
                print(f"Total photos: {data['photo_count']}")
                
                for i, photo in enumerate(photos, 1):
                    print(f"{i}. {photo['damage_type']} - Uploaded: {photo['upload_time']}")
                    print(f"   Status: {photo['processing_status']}")
                    print(f"   URL: {self.api_url}{photo['url']}")
                
                return True
            else:
                print(f"\nFailed to get photos: {response.json().get('error', 'Unknown error')}")
                return False
        
        except requests.exceptions.RequestException as e:
            print(f"\nError connecting to API: {e}")
            return False

def interactive_mode(simulator):
    """
    Run the simulator in interactive mode.
    
    Args:
        simulator (PhotoAppSimulator): The simulator instance
    """
    print("\nStorm Damage Photo Collection App Simulator")
    print("===========================================")
    
    while True:
        print("\nOptions:")
        print("1. Login")
        print("2. View Jobs")
        print("3. Upload Photo")
        print("4. View Job Photos")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            email = input("Email: ")
            password = input("Password: ")
            simulator.login(email, password)
        
        elif choice == "2":
            simulator.get_jobs()
        
        elif choice == "3":
            if not simulator.jobs:
                print("\nYou must get jobs first.")
                continue
            
            job_index = int(input(f"Job index (1-{len(simulator.jobs)}): "))
            photo_path = input("Path to photo file: ")
            damage_type = input("Damage type (roof, siding, structural, water, other): ")
            notes = input("Notes: ")
            
            # Get location (in a real app, this would come from GPS)
            latitude = input("Latitude (default: 0.0): ") or "0.0"
            longitude = input("Longitude (default: 0.0): ") or "0.0"
            
            metadata = {
                "damage_type": damage_type,
                "notes": notes,
                "latitude": latitude,
                "longitude": longitude,
                "device_model": "Simulator",
                "os_version": "1.0",
                "app_version": "1.0"
            }
            
            simulator.upload_photo(job_index, photo_path, metadata)
        
        elif choice == "4":
            if not simulator.jobs:
                print("\nYou must get jobs first.")
                continue
            
            job_index = int(input(f"Job index (1-{len(simulator.jobs)}): "))
            simulator.view_job_photos(job_index)
        
        elif choice == "5":
            print("\nExiting simulator. Goodbye!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")

def main():
    """
    Main function to run the Photo App Simulator.
    """
    parser = argparse.ArgumentParser(description="Photo App Simulator")
    parser.add_argument("--api-url", default="http://localhost:5000", help="URL of the Photo Collection API")
    parser.add_argument("--email", help="Contractor's email for automatic login")
    parser.add_argument("--password", help="Contractor's password for automatic login")
    parser.add_argument("--upload", help="Path to photo file for automatic upload")
    parser.add_argument("--job-index", type=int, help="Job index for automatic upload")
    parser.add_argument("--damage-type", help="Damage type for automatic upload")
    args = parser.parse_args()
    
    simulator = PhotoAppSimulator(api_url=args.api_url)
    
    # Check if automatic mode is requested
    if args.email and args.password and args.upload and args.job_index:
        if simulator.login(args.email, args.password):
            if simulator.get_jobs():
                metadata = {
                    "damage_type": args.damage_type or "Unknown",
                    "notes": "Uploaded via command line",
                    "device_model": "CLI Simulator",
                    "os_version": "1.0",
                    "app_version": "1.0"
                }
                simulator.upload_photo(args.job_index, args.upload, metadata)
    else:
        # Run in interactive mode
        interactive_mode(simulator)

if __name__ == "__main__":
    main()
