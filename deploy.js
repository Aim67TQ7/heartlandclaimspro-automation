#!/usr/bin/env node

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// Configuration
const appDir = path.resolve(__dirname);
const buildDir = path.join(appDir, '.next');

console.log('Starting deployment process for Blog Automation Web Application...');

// Step 1: Install dependencies
console.log('\n📦 Installing dependencies...');
try {
  execSync('npm install', { stdio: 'inherit', cwd: appDir });
  console.log('✅ Dependencies installed successfully');
} catch (error) {
  console.error('❌ Failed to install dependencies:', error.message);
  process.exit(1);
}

// Step 2: Run tests
console.log('\n🧪 Running tests...');
try {
  execSync('npm test', { stdio: 'inherit', cwd: appDir });
  console.log('✅ Tests passed successfully');
} catch (error) {
  console.error('❌ Tests failed:', error.message);
  const shouldContinue = process.env.FORCE_DEPLOY === 'true';
  if (!shouldContinue) {
    console.error('Deployment aborted due to test failures. Set FORCE_DEPLOY=true to override.');
    process.exit(1);
  }
  console.warn('⚠️ Continuing deployment despite test failures because FORCE_DEPLOY=true');
}

// Step 3: Build the application
console.log('\n🏗️ Building application...');
try {
  execSync('npm run build', { stdio: 'inherit', cwd: appDir });
  console.log('✅ Build completed successfully');
} catch (error) {
  console.error('❌ Build failed:', error.message);
  process.exit(1);
}

// Step 4: Deploy the application
console.log('\n🚀 Deploying application...');
try {
  // For this example, we'll use the built-in Next.js deployment command
  // In a real environment, this might be replaced with a command to deploy to a specific hosting service
  execSync('npx next-deploy', { stdio: 'inherit', cwd: appDir });
  console.log('✅ Deployment completed successfully');
} catch (error) {
  console.error('❌ Deployment failed:', error.message);
  console.log('\n🔄 Falling back to static export...');
  
  try {
    // Create an export directory
    const exportDir = path.join(appDir, 'out');
    if (!fs.existsSync(exportDir)) {
      fs.mkdirSync(exportDir, { recursive: true });
    }
    
    // Export the application as static files
    execSync('npx next export', { stdio: 'inherit', cwd: appDir });
    console.log('✅ Static export completed successfully');
    
    // Deploy the static files
    console.log('\n📤 Deploying static files...');
    execSync(`deploy_apply_deployment --type static --local_dir ${exportDir}`, { stdio: 'inherit' });
    console.log('✅ Static deployment completed successfully');
  } catch (exportError) {
    console.error('❌ Static export failed:', exportError.message);
    process.exit(1);
  }
}

console.log('\n🎉 Blog Automation Web Application has been successfully deployed!');
console.log('You can now access it at the URL provided above.');
