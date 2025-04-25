# Blog Automation Web Application Deployment Guide

This document provides instructions for deploying the Blog Automation Web Application to a production environment.

## Prerequisites

- Node.js 16.x or higher
- npm 8.x or higher
- Access to a hosting service that supports Next.js applications

## Deployment Steps

### Option 1: Using the Deployment Script

We've created an automated deployment script that handles the entire process:

1. Make the deployment script executable:
   ```bash
   chmod +x deploy.js
   ```

2. Run the deployment script:
   ```bash
   node deploy.js
   ```

The script will:
- Install all dependencies
- Run tests to ensure everything is working correctly
- Build the application
- Deploy the application to production
- Fall back to static export if needed

### Option 2: Manual Deployment

If you prefer to deploy manually, follow these steps:

1. Install dependencies:
   ```bash
   npm install
   ```

2. Run tests:
   ```bash
   npm test
   ```

3. Build the application:
   ```bash
   npm run build
   ```

4. Deploy using Next.js deployment:
   ```bash
   npx next-deploy
   ```

   Or export as static files:
   ```bash
   npx next export
   ```

5. Deploy the static files to your hosting service.

## Environment Configuration

Before deployment, ensure you have set up the following environment variables:

- `NODE_ENV`: Set to `production` for production deployment
- `API_BASE_URL`: Base URL for the blog automation API
- `AUTH_SECRET`: Secret key for authentication (must be at least 32 characters)

You can set these in a `.env.production` file or directly on your hosting service.

## Post-Deployment Verification

After deployment, verify that:

1. The application is accessible at the deployed URL
2. You can log in with your credentials
3. All features are working correctly:
   - Blog generation
   - Content testing
   - Publishing workflow
   - Scheduling system
   - Admin dashboard

## Troubleshooting

If you encounter issues during deployment:

1. Check the deployment logs for specific error messages
2. Verify that all environment variables are correctly set
3. Ensure your hosting service supports Next.js applications
4. Try the static export option if your hosting service doesn't support server-side rendering

For additional help, refer to the technical documentation or contact the development team.

## Maintenance

Regular maintenance tasks:

1. Update dependencies regularly to ensure security
2. Monitor application performance and logs
3. Back up the database and content regularly
4. Test new features in a staging environment before deploying to production
