#!/usr/bin/env python3
"""
Manual Blog Scheduling Tool

This script provides a manual scheduling solution for blog posts,
helping users manage their weekly publishing schedule without
requiring automated scheduling.
"""

import os
import json
import argparse
import calendar
from datetime import datetime, timedelta
import re
import sys
import csv

# Add the current directory to the path to import other modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from blog_generator import BlogContentGenerator
from blog_publisher import BlogPublisher

class ManualScheduler:
    """
    A class to manage manual scheduling of blog posts.
    """
    
    def __init__(self, data_dir="/home/ubuntu/blog_automation"):
        """
        Initialize the ManualScheduler.
        
        Args:
            data_dir (str): Directory containing blog data files
        """
        self.data_dir = data_dir
        self.schedule_dir = os.path.join(data_dir, "schedule")
        self.schedule_file = os.path.join(self.schedule_dir, "publishing_schedule.csv")
        self.calendar_file = os.path.join(self.schedule_dir, "publishing_calendar.md")
        self.reminders_file = os.path.join(self.schedule_dir, "upcoming_reminders.md")
        
        # Create schedule directory if it doesn't exist
        os.makedirs(self.schedule_dir, exist_ok=True)
        
        # Initialize the publisher
        self.publisher = BlogPublisher(data_dir=data_dir)
        
        # Initialize the generator
        self.generator = BlogContentGenerator(data_dir=data_dir)
        
        print(f"ManualScheduler initialized with data from {data_dir}")
    
    def create_schedule(self, start_date=None, frequency="weekly", day_of_week="Monday", weeks=12):
        """
        Create a publishing schedule.
        
        Args:
            start_date (str): Start date in YYYY-MM-DD format
            frequency (str): Publishing frequency (weekly, biweekly, monthly)
            day_of_week (str): Day of the week for publishing
            weeks (int): Number of weeks to schedule
        
        Returns:
            str: Path to the created schedule file
        """
        # Parse start date or use next occurrence of specified day
        if start_date:
            try:
                current_date = datetime.strptime(start_date, "%Y-%m-%d")
            except ValueError:
                print(f"Invalid date format: {start_date}. Using next {day_of_week} instead.")
                current_date = self._get_next_day_of_week(day_of_week)
        else:
            current_date = self._get_next_day_of_week(day_of_week)
        
        # Generate weekly topics
        weekly_topics = self.generator.generate_weekly_topics(weeks)
        
        # Create schedule entries
        schedule_entries = []
        
        for i, topic in enumerate(weekly_topics):
            # Calculate publish date based on frequency
            if i > 0:
                if frequency == "weekly":
                    current_date += timedelta(days=7)
                elif frequency == "biweekly":
                    current_date += timedelta(days=14)
                elif frequency == "monthly":
                    # Add roughly a month (4 weeks)
                    current_date += timedelta(days=28)
            
            # Create schedule entry
            entry = {
                "publish_date": current_date.strftime("%Y-%m-%d"),
                "day_of_week": current_date.strftime("%A"),
                "week_number": topic["week"],
                "title": topic["title"],
                "topic": topic["topic"],
                "template_type": topic["template_type"],
                "storm_type": topic["storm_type"],
                "status": "Scheduled",
                "notes": ""
            }
            
            schedule_entries.append(entry)
        
        # Create CSV file
        try:
            with open(self.schedule_file, 'w', newline='') as f:
                fieldnames = ["publish_date", "day_of_week", "week_number", "title", "topic", "template_type", "storm_type", "status", "notes"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for entry in schedule_entries:
                    writer.writerow(entry)
            
            print(f"Created publishing schedule: {self.schedule_file}")
            
            # Create calendar view
            self._create_calendar_view(schedule_entries)
            
            # Create reminders
            self._create_reminders(schedule_entries)
            
            return self.schedule_file
        
        except Exception as e:
            print(f"Error creating schedule: {e}")
            return None
    
    def _get_next_day_of_week(self, day_name):
        """
        Get the date of the next occurrence of a day of the week.
        
        Args:
            day_name (str): Name of the day of the week
        
        Returns:
            datetime: Date of the next occurrence
        """
        # Convert day name to day number (0 = Monday, 6 = Sunday)
        try:
            target_day = list(calendar.day_name).index(day_name)
        except ValueError:
            print(f"Invalid day name: {day_name}. Using Monday instead.")
            target_day = 0  # Monday
        
        # Get current date and day of week
        current_date = datetime.now()
        current_day = current_date.weekday()
        
        # Calculate days until next occurrence
        days_ahead = target_day - current_day
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        
        # Calculate next occurrence
        next_date = current_date + timedelta(days=days_ahead)
        
        # Set time to 9:00 AM
        next_date = next_date.replace(hour=9, minute=0, second=0, microsecond=0)
        
        return next_date
    
    def _create_calendar_view(self, schedule_entries):
        """
        Create a calendar view of the publishing schedule.
        
        Args:
            schedule_entries (list): List of schedule entries
        
        Returns:
            str: Path to the created calendar file
        """
        # Group entries by month and year
        months = {}
        for entry in schedule_entries:
            date = datetime.strptime(entry["publish_date"], "%Y-%m-%d")
            month_year = date.strftime("%B %Y")
            
            if month_year not in months:
                months[month_year] = []
            
            months[month_year].append(entry)
        
        # Create calendar content
        content = "# Blog Publishing Calendar\n\n"
        content += f"Generated on: {datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        for month_year, entries in sorted(months.items(), key=lambda x: datetime.strptime(x[0], "%B %Y")):
            content += f"## {month_year}\n\n"
            
            # Create a table for this month
            content += "| Date | Day | Title | Topic | Status |\n"
            content += "|------|-----|-------|-------|--------|\n"
            
            for entry in sorted(entries, key=lambda x: x["publish_date"]):
                date = entry["publish_date"]
                day = entry["day_of_week"]
                title = entry["title"]
                topic = entry["topic"]
                status = entry["status"]
                
                content += f"| {date} | {day} | {title} | {topic} | {status} |\n"
            
            content += "\n"
        
        # Save calendar file
        try:
            with open(self.calendar_file, 'w') as f:
                f.write(content)
            
            print(f"Created publishing calendar: {self.calendar_file}")
            return self.calendar_file
        
        except Exception as e:
            print(f"Error creating calendar: {e}")
            return None
    
    def _create_reminders(self, schedule_entries):
        """
        Create reminders for upcoming blog posts.
        
        Args:
            schedule_entries (list): List of schedule entries
        
        Returns:
            str: Path to the created reminders file
        """
        # Get current date
        current_date = datetime.now().date()
        
        # Filter upcoming entries (within the next 4 weeks)
        upcoming_entries = []
        for entry in schedule_entries:
            publish_date = datetime.strptime(entry["publish_date"], "%Y-%m-%d").date()
            days_until = (publish_date - current_date).days
            
            if 0 <= days_until <= 28:  # Within the next 4 weeks
                entry["days_until"] = days_until
                upcoming_entries.append(entry)
        
        # Sort by publish date
        upcoming_entries.sort(key=lambda x: x["publish_date"])
        
        # Create reminders content
        content = "# Upcoming Blog Publishing Reminders\n\n"
        content += f"Generated on: {datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        if not upcoming_entries:
            content += "No upcoming blog posts scheduled within the next 4 weeks.\n"
        else:
            for entry in upcoming_entries:
                days_until = entry["days_until"]
                publish_date = entry["publish_date"]
                day = entry["day_of_week"]
                title = entry["title"]
                
                if days_until == 0:
                    urgency = "🔴 TODAY"
                elif days_until <= 2:
                    urgency = "🟠 SOON"
                elif days_until <= 7:
                    urgency = "🟡 THIS WEEK"
                else:
                    urgency = "🟢 UPCOMING"
                
                content += f"## {urgency}: {publish_date} ({day})\n\n"
                content += f"**Title:** {title}\n\n"
                content += f"**Topic:** {entry['topic']}\n\n"
                content += f"**Template Type:** {entry['template_type']}\n\n"
                content += f"**Storm Type:** {entry['storm_type']}\n\n"
                
                # Add preparation steps
                content += "### Preparation Steps:\n\n"
                
                if days_until >= 7:
                    content += "1. ⬜ Generate blog post content (run `python blog_publisher.py --weekly --week {entry['week_number']}`)\n"
                    content += "2. ⬜ Review and edit content\n"
                    content += "3. ⬜ Prepare images\n"
                    content += "4. ⬜ Create downloadable resource\n"
                    content += "5. ⬜ Schedule for publishing\n"
                elif days_until >= 2:
                    content += "1. ✅ Generate blog post content\n"
                    content += "2. ⬜ Review and edit content\n"
                    content += "3. ⬜ Prepare images\n"
                    content += "4. ⬜ Create downloadable resource\n"
                    content += "5. ⬜ Schedule for publishing\n"
                else:
                    content += "1. ✅ Generate blog post content\n"
                    content += "2. ✅ Review and edit content\n"
                    content += "3. ⬜ Prepare images\n"
                    content += "4. ⬜ Create downloadable resource\n"
                    content += "5. ⬜ PUBLISH TODAY\n"
                
                content += "\n---\n\n"
        
        # Save reminders file
        try:
            with open(self.reminders_file, 'w') as f:
                f.write(content)
            
            print(f"Created upcoming reminders: {self.reminders_file}")
            return self.reminders_file
        
        except Exception as e:
            print(f"Error creating reminders: {e}")
            return None
    
    def update_schedule(self, entry_id, status=None, notes=None, new_date=None):
        """
        Update a schedule entry.
        
        Args:
            entry_id (int): Index of the entry to update (1-based)
            status (str): New status for the entry
            notes (str): Notes to add to the entry
            new_date (str): New publish date in YYYY-MM-DD format
        
        Returns:
            bool: Success status
        """
        # Check if schedule file exists
        if not os.path.exists(self.schedule_file):
            print(f"Schedule file not found: {self.schedule_file}")
            return False
        
        # Read schedule entries
        try:
            with open(self.schedule_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                entries = list(reader)
            
            # Check if entry_id is valid
            if entry_id < 1 or entry_id > len(entries):
                print(f"Invalid entry ID: {entry_id}. Valid range is 1-{len(entries)}.")
                return False
            
            # Update entry
            entry = entries[entry_id - 1]
            
            if status:
                entry["status"] = status
            
            if notes:
                entry["notes"] = notes
            
            if new_date:
                try:
                    # Validate date format
                    date_obj = datetime.strptime(new_date, "%Y-%m-%d")
                    entry["publish_date"] = new_date
                    entry["day_of_week"] = date_obj.strftime("%A")
                except ValueError:
                    print(f"Invalid date format: {new_date}. Date should be in YYYY-MM-DD format.")
                    return False
            
            # Write updated entries
            with open(self.schedule_file, 'w', newline='') as f:
                fieldnames = reader.fieldnames
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(entries)
            
            print(f"Updated entry {entry_id} in schedule.")
            
            # Update calendar and reminders
            self._create_calendar_view(entries)
            self._create_reminders(entries)
            
            return True
        
        except Exception as e:
            print(f"Error updating schedule: {e}")
            return False
    
    def mark_as_published(self, entry_id):
        """
        Mark a schedule entry as published.
        
        Args:
            entry_id (int): Index of the entry to mark as published (1-based)
        
        Returns:
            bool: Success status
        """
        return self.update_schedule(entry_id, status="Published")
    
    def list_schedule(self):
        """
        List all schedule entries.
        
        Returns:
            list: List of schedule entries
        """
        # Check if schedule file exists
        if not os.path.exists(self.schedule_file):
            print(f"Schedule file not found: {self.schedule_file}")
            return []
        
        # Read schedule entries
        try:
            with open(self.schedule_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                entries = list(reader)
            
            return entries
        
        except Exception as e:
            print(f"Error reading schedule: {e}")
            return []
    
    def prepare_next_post(self):
        """
        Prepare the next scheduled blog post.
        
        Returns:
            str: Path to the prepared blog post
        """
        # Get current date
        current_date = datetime.now().date()
        
        # Get schedule entries
        entries = self.list_schedule()
        
        # Find the next scheduled post
        next_entry = None
        for entry in entries:
            if entry["status"] != "Published":
                publish_date = datetime.strptime(entry["publish_date"], "%Y-%m-%d").date()
                if publish_date >= current_date:
                    next_entry = entry
                    break
        
        if not next_entry:
  
(Content truncated due to size limit. Use line ranges to read in chunks)