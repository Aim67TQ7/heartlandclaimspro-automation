#!/usr/bin/env python3
"""
Payment Processing Module

This module handles the payment processing workflow for contractors after
successful claim submissions. It tracks claim status, calculates payments,
and notifies contractors when payments are ready.
"""

import os
import json
import logging
import argparse
from datetime import datetime, timedelta
import uuid
import time
import random  # For simulation purposes only

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("payment_processing.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("payment_processing")

class PaymentProcessor:
    """
    A class to handle payment processing for contractors.
    
    Note: This is a simulation of payment processing. In a production environment,
    this would integrate with actual payment processing systems.
    """
    
    def __init__(self, claims_dir="xactimate_claims", output_dir="payment_records"):
        """
        Initialize the PaymentProcessor.
        
        Args:
            claims_dir (str): Directory containing Xactimate claim submissions
            output_dir (str): Directory to store payment records
        """
        self.claims_dir = claims_dir
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info("PaymentProcessor initialized")
    
    def get_approved_claims(self):
        """
        Get a list of approved claims ready for payment.
        
        Returns:
            list: List of approved claim data
        """
        approved_claims = []
        
        # Check claims directory
        if not os.path.exists(self.claims_dir):
            logger.warning(f"Claims directory not found: {self.claims_dir}")
            return approved_claims
        
        # Scan result files
        for filename in os.listdir(self.claims_dir):
            if filename.endswith('_result.json'):
                result_file = os.path.join(self.claims_dir, filename)
                
                try:
                    with open(result_file, 'r') as f:
                        result = json.load(f)
                    
                    # Check if this claim is approved and not yet paid
                    if result.get('status') == 'Approved':
                        job_id = result.get('job_id')
                        
                        # Check if payment has already been processed
                        payment_file = os.path.join(self.output_dir, f"{job_id}_payment.json")
                        if not os.path.exists(payment_file):
                            # Get the corresponding claim data
                            claim_file = os.path.join(self.claims_dir, f"{job_id}_claim.json")
                            
                            if os.path.exists(claim_file):
                                with open(claim_file, 'r') as f:
                                    claim_data = json.load(f)
                                
                                approved_claims.append({
                                    'result': result,
                                    'claim': claim_data
                                })
                
                except Exception as e:
                    logger.error(f"Error reading result file {filename}: {e}")
        
        logger.info(f"Found {len(approved_claims)} approved claims ready for payment")
        return approved_claims
    
    def calculate_contractor_payment(self, claim_data, payment_percentage=0.7):
        """
        Calculate payment amount for a contractor.
        
        Args:
            claim_data (dict): Claim data
            payment_percentage (float): Percentage of claim amount to pay to contractor
        
        Returns:
            float: Payment amount
        """
        # Get the total claim amount
        total_amount = claim_data.get('totals', {}).get('total', 0)
        
        # Calculate contractor payment
        payment_amount = total_amount * payment_percentage
        
        return payment_amount
    
    def process_payment(self, claim_info):
        """
        Process payment for an approved claim.
        
        Args:
            claim_info (dict): Claim information including result and claim data
        
        Returns:
            dict: Payment record
        """
        result = claim_info['result']
        claim_data = claim_info['claim']
        
        job_id = result.get('job_id')
        claim_id = result.get('claim_id')
        xactimate_id = result.get('xactimate_id')
        
        logger.info(f"Processing payment for job {job_id}, claim {claim_id}")
        
        # Calculate payment amount
        payment_amount = self.calculate_contractor_payment(claim_data)
        
        # In a real implementation, this would integrate with a payment
        # processing system to send the payment to the contractor
        
        # Simulate processing time
        time.sleep(1)
        
        # Create payment record
        payment_record = {
            'payment_id': str(uuid.uuid4()),
            'job_id': job_id,
            'claim_id': claim_id,
            'xactimate_id': xactimate_id,
            'contractor_id': claim_data.get('contractor_id', 'unknown'),
            'payment_amount': payment_amount,
            'total_claim_amount': claim_data.get('totals', {}).get('total', 0),
            'payment_percentage': 0.7,
            'payment_date': datetime.now().isoformat(),
            'payment_method': 'Direct Deposit',
            'status': 'Processed',
            'notes': 'Payment for storm damage assessment and documentation'
        }
        
        # Save payment record
        payment_file = os.path.join(self.output_dir, f"{job_id}_payment.json")
        
        try:
            with open(payment_file, 'w') as f:
                json.dump(payment_record, f, indent=2)
            logger.info(f"Saved payment record to {payment_file}")
        except Exception as e:
            logger.error(f"Error saving payment record: {e}")
            return None
        
        return payment_record
    
    def process_all_payments(self):
        """
        Process payments for all approved claims.
        
        Returns:
            list: List of payment records
        """
        approved_claims = self.get_approved_claims()
        
        if not approved_claims:
            logger.info("No approved claims ready for payment")
            return []
        
        payment_records = []
        for claim_info in approved_claims:
            try:
                payment_record = self.process_payment(claim_info)
                if payment_record:
                    payment_records.append(payment_record)
            except Exception as e:
                job_id = claim_info.get('result', {}).get('job_id', 'unknown')
                logger.error(f"Error processing payment for job {job_id}: {e}")
        
        logger.info(f"Processed {len(payment_records)} payments")
        return payment_records
    
    def get_payment_status(self, job_id):
        """
        Get the status of a payment.
        
        Args:
            job_id (str): Job ID
        
        Returns:
            dict: Payment record
        """
        payment_file = os.path.join(self.output_dir, f"{job_id}_payment.json")
        
        if not os.path.exists(payment_file):
            logger.warning(f"No payment record found for job {job_id}")
            return None
        
        try:
            with open(payment_file, 'r') as f:
                payment_record = json.load(f)
            
            logger.info(f"Retrieved payment status for job {job_id}")
            return payment_record
        except Exception as e:
            logger.error(f"Error reading payment record: {e}")
            return None
    
    def generate_payment_report(self, start_date=None, end_date=None):
        """
        Generate a report of payments within a date range.
        
        Args:
            start_date (str): Start date in ISO format (YYYY-MM-DD)
            end_date (str): End date in ISO format (YYYY-MM-DD)
        
        Returns:
            dict: Payment report
        """
        # Set default date range if not provided
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        start_datetime = datetime.fromisoformat(start_date + 'T00:00:00')
        end_datetime = datetime.fromisoformat(end_date + 'T23:59:59')
        
        logger.info(f"Generating payment report from {start_date} to {end_date}")
        
        # Get all payment records
        payment_records = []
        for filename in os.listdir(self.output_dir):
            if filename.endswith('_payment.json'):
                payment_file = os.path.join(self.output_dir, filename)
                
                try:
                    with open(payment_file, 'r') as f:
                        payment_record = json.load(f)
                    
                    # Check if payment date is within range
                    payment_date = datetime.fromisoformat(payment_record.get('payment_date', '').split('.')[0])
                    if start_datetime <= payment_date <= end_datetime:
                        payment_records.append(payment_record)
                
                except Exception as e:
                    logger.error(f"Error reading payment file {filename}: {e}")
        
        # Calculate totals
        total_payments = len(payment_records)
        total_amount = sum(record.get('payment_amount', 0) for record in payment_records)
        total_claim_amount = sum(record.get('total_claim_amount', 0) for record in payment_records)
        
        # Create report
        report = {
            'start_date': start_date,
            'end_date': end_date,
            'total_payments': total_payments,
            'total_amount': total_amount,
            'total_claim_amount': total_claim_amount,
            'average_payment': total_amount / total_payments if total_payments > 0 else 0,
            'payment_records': payment_records
        }
        
        # Save report
        report_file = os.path.join(self.output_dir, f"payment_report_{start_date}_to_{end_date}.json")
        
        try:
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            logger.info(f"Saved payment report to {report_file}")
        except Exception as e:
            logger.error(f"Error saving payment report: {e}")
        
        return report
    
    def notify_contractor(self, payment_record):
        """
        Notify a contractor about a processed payment.
        
        Args:
            payment_record (dict): Payment record
        
        Returns:
            bool: Success status
        """
        # In a real implementation, this would send an email or push notification
        # to the contractor. For simulation, we'll just log the notification.
        
        job_id = payment_record.get('job_id')
        payment_amount = payment_record.get('payment_amount')
        payment_date = payment_record.get('payment_date')
        
        logger.info(f"Notifying contractor about payment for job {job_id}")
        logger.info(f"Payment amount: ${payment_amount:.2f}, Date: {payment_date}")
        
        # Simulate notification
        notification = {
            'to': 'contractor@example.com',
            'subject': f"Payment Processed for Job {job_id}",
            'body': f"Your payment of ${payment_amount:.2f} for job {job_id} has been processed on {payment_date}. " +
                    f"The payment will be deposited to your account within 1-2 business days."
        }
        
        # Save notification record
        notification_file = os.path.join(self.output_dir, f"{job_id}_notification.json")
        
        try:
            with open(notification_file, 'w') as f:
                json.dump(notification, f, indent=2)
            logger.info(f"Saved notification record to {notification_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving notification record: {e}")
            return False

def main():
    """
    Main function to run the PaymentProcessor.
    """
    parser = argparse.ArgumentParser(description="Payment Processing")
    parser.add_argument("--claims-dir", default="xactimate_claims", help="Directory containing Xactimate claim submissions")
    parser.add_argument("--output-dir", default="payment_records", help="Directory to store payment records")
    parser.add_argument("--job-id", help="Check payment status for a specific job ID")
    parser.add_argument("--process-all", action="store_true", help="Process all approved claims")
    parser.add_argument("--report", action="store_true", help="Generate payment report")
    parser.add_argument("--start-date", help="Start date for report (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="End date for report (YYYY-MM-DD)")
    args = parser.parse_args()
    
    processor = PaymentProcessor(claims_dir=args.claims_dir, output_dir=args.output_dir)
    
    if args.job_id:
        # Check payment status for a specific job
        print(f"\nChecking payment status for job {args.job_id}...")
        payment = processor.get_payment_status(args.job_id)
        
        if payment:
            print("\nPayment Status:")
            print(f"Job ID: {payment['job_id']}")
            print(f"Payment ID: {payment['payment_id']}")
            print(f"Amount: ${payment['payment_amount']:.2f}")
            print(f"Date: {payment['payment_date']}")
            print(f"Method: {payment['payment_method']}")
            print(f"Status: {payment['status']}")
        else:
            print(f"No payment record found for job {args.job_id}")
    
    elif args.process_all:
        # Process all approved claims
        print("\nProcessing payments for all approved claims...")
        payments = processor.process_all_payments()
        
        if payments:
            print(f"\nProcessed {len(payments)} payments:")
            for payment in payments:
                print(f"  Job {payment['job_id']}: " +
                      f"${payment['payment_amount']:.2f} via {payment['payment_method']}")
                
                # Notify contractor
                processor.notify_contractor(payment)
        else:
            print("No approved claims ready for payment")
    
    elif args.report:
        # Generate payment report
        print("\nGenerating payment report...")
        report = processor.generate_payment_report(args.start_date, args.end_date)
        
        if report:
            print("\nPayment Report:")
            print(f"Period: {report['start_date']} to {report['end_date']}")
            print(f"Total Payments: {report['total_payments']}")
            print(f"Total Amount: ${report['total_amount']:.2f}")
            print(f"Average Payment: ${report['average_payment']:.2f}")
        else:
            print("Failed to generate payment report")
    
    else:
        # Just list approved claims
        approved_claims = processor.get_approved_claims()
        
        if approved_claims:
            print(f"\nFound {len(approved_claims)} approved claims ready for payment:")
            for claim_info in approved_claims:
                job_id = claim_info['result']['job_id']
                amount = claim_info['claim']['totals']['total']
                print(f"  Job {job_id}: ${amount:.2f}")
            print("\nUse --process-all to process these payments")
        else:
            print("\nNo approved claims ready for pa
(Content truncated due to size limit. Use line ranges to read in chunks)