# Storm Damage Automation System - User Guide

## Overview

The Storm Damage Automation System is a comprehensive solution that automates the entire workflow for storm damage assessment and insurance claim processing. The system consists of several integrated components:

1. **Storm Tracking System**: Monitors weather alerts to identify regions affected by storms
2. **Google Ads Campaign Manager**: Creates targeted ad campaigns to recruit contractors in affected areas
3. **Photo Collection System**: Allows contractors to submit photos of storm damage via a mobile app
4. **AI Damage Assessment**: Analyzes photos to identify and classify storm damage elements
5. **Xactimate Integration**: Automatically completes and submits insurance claims
6. **Payment Processing**: Handles contractor payments after successful claim submissions

This guide provides instructions for setting up, deploying, and using the system.

## System Requirements

- Python 3.10 or higher
- Internet connection for accessing weather APIs and Google Ads
- Sufficient storage space for photos and data (minimum 10GB recommended)
- Linux-based operating system (Ubuntu 20.04 or higher recommended)

## Installation

1. Clone the repository or extract the system files to your desired location:

```bash
git clone https://github.com/example/storm-automation.git
cd storm-automation
```

2. Run the deployment script to set up the system:

```bash
python3 deploy.py
```

This script will:
- Check and install all required dependencies
- Create necessary directories for data storage
- Run integration tests to verify the system is working correctly
- Start the required services

By default, the Photo Collection API will run on port 5000. You can specify a different port using the `--port` option:

```bash
python3 deploy.py --port 8080
```

## Configuration

### Storm Tracking Configuration

The storm tracking system uses the National Weather Service API to monitor weather alerts. No API key is required, but you can configure the severity threshold in the `storm_automation.py` script:

```bash
python3 src/storm_automation.py --severity Moderate
```

Available severity levels:
- Minor
- Moderate
- Severe
- Extreme

### Google Ads Configuration

To configure the Google Ads campaign settings, edit the `ads_campaign_manager.py` file or specify the daily budget when running the script:

```bash
python3 src/ads_campaign_manager.py --daily-budget 300
```

## Using the System

### Running the Complete Workflow

To run the complete automation workflow:

```bash
python3 src/storm_automation.py
```

This will:
1. Track storms and identify affected regions
2. Create targeted Google Ads campaigns for those regions
3. Prepare the system for photo submissions from contractors

### Managing Photo Submissions

The Photo Collection API provides endpoints for contractors to submit photos. The API runs automatically when you deploy the system.

To test the photo submission process, you can use the simulator:

```bash
python3 src/photo_app_simulator.py
```

This will start an interactive session where you can:
- Log in as a contractor
- View available jobs
- Upload photos
- View submitted photos

### Processing Damage Assessments

To process submitted photos and generate damage assessments:

```bash
python3 src/damage_assessment.py
```

To generate a summary for a specific job:

```bash
python3 src/damage_assessment.py --job-id JOB_ID --summary
```

### Submitting Insurance Claims

To submit insurance claims to Xactimate:

```bash
python3 src/xactimate_integration.py --process-all
```

To check the status of a specific claim:

```bash
python3 src/xactimate_integration.py --job-id JOB_ID --check-status
```

### Processing Payments

To process payments for approved claims:

```bash
python3 src/payment_processing.py --process-all
```

To check the status of a specific payment:

```bash
python3 src/payment_processing.py --job-id JOB_ID
```

To generate a payment report:

```bash
python3 src/payment_processing.py --report
```

## System Architecture

The system is designed with a modular architecture, allowing each component to function independently while also working together as an integrated system.

### Component Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Storm Tracker  │────▶│  Ads Campaign   │     │ Photo Collection │
│                 │     │    Manager      │     │       API        │
└─────────────────┘     └─────────────────┘     └────────┬─────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Payment      │◀────│   Xactimate     │◀────│     Damage      │
│   Processing    │     │   Integration   │     │   Assessment    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Data Flow

1. The Storm Tracker identifies regions affected by storms
2. The Ads Campaign Manager creates targeted campaigns for those regions
3. Contractors respond to ads and submit photos through the Photo Collection API
4. The Damage Assessment module analyzes the photos to identify damage
5. The Xactimate Integration module creates and submits insurance claims
6. The Payment Processing module handles payments to contractors

## Troubleshooting

### Common Issues

#### API Connection Issues

If the system fails to connect to the National Weather Service API:

1. Check your internet connection
2. Verify that the API is operational by visiting https://api.weather.gov
3. Check the logs for specific error messages

#### Photo Upload Issues

If contractors are unable to upload photos:

1. Verify that the Photo Collection API is running
2. Check the API logs for error messages
3. Ensure the upload directory has proper permissions

#### Integration Test Failures

If integration tests fail during deployment:

1. Check the test logs for specific failures
2. Verify that all dependencies are installed correctly
3. Ensure all required directories exist and have proper permissions

### Log Files

The system generates several log files that can help diagnose issues:

- `storm_tracker.log`: Logs from the storm tracking component
- `ads_campaign.log`: Logs from the Google Ads campaign manager
- `photo_api.log`: Logs from the photo collection API
- `damage_assessment.log`: Logs from the damage assessment component
- `xactimate_integration.log`: Logs from the Xactimate integration component
- `payment_processing.log`: Logs from the payment processing component
- `integration_test.log`: Logs from the integration tests
- `deployment.log`: Logs from the deployment process

## Support and Maintenance

### Updating the System

To update the system to the latest version:

1. Pull the latest changes from the repository
2. Run the deployment script again

```bash
git pull
python3 deploy.py
```

### Backing Up Data

It's recommended to regularly back up the data directories:

```bash
tar -czf storm_automation_backup.tar.gz data/
```

### Getting Support

For technical support or feature requests, please contact:

- Email: support@example.com
- Phone: (555) 123-4567

## Conclusion

The Storm Damage Automation System provides a complete solution for automating the storm damage assessment and insurance claim process. By following this guide, you should be able to set up, configure, and use the system effectively.

For more detailed information about each component, please refer to the individual component documentation in the `docs` directory.
