import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

// Helper function to execute Python script and get JSON response
async function executePythonAPI(method: string, apiPath: string, data?: any): Promise<any> {
  return new Promise((resolve, reject) => {
    const pythonScriptPath = path.join(process.cwd(), 'src/lib/blog-automation-api.py');
    
    // Prepare the arguments for the Python script
    const args = [
      pythonScriptPath,
      '--method', method,
      '--path', apiPath
    ];
    
    // If data is provided, add it as a JSON string
    if (data) {
      args.push('--data', JSON.stringify(data));
    }
    
    // Spawn Python process
    const pythonProcess = spawn('python3', args);
    
    let result = '';
    let error = '';
    
    // Collect data from stdout
    pythonProcess.stdout.on('data', (data) => {
      result += data.toString();
    });
    
    // Collect errors from stderr
    pythonProcess.stderr.on('data', (data) => {
      error += data.toString();
    });
    
    // Handle process completion
    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Python process exited with code ${code}: ${error}`));
        return;
      }
      
      try {
        // Parse the JSON result
        const jsonResult = JSON.parse(result);
        resolve(jsonResult);
      } catch (e) {
        reject(new Error(`Failed to parse Python response: ${result}`));
      }
    });
  });
}

// API route handler for blog posts
export async function GET(request: NextRequest) {
  try {
    const result = await executePythonAPI('GET', '/api/blog-posts');
    return NextResponse.json(result);
  } catch (error) {
    console.error('Error fetching blog posts:', error);
    return NextResponse.json({ success: false, error: 'Failed to fetch blog posts' }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const data = await request.json();
    const result = await executePythonAPI('POST', '/api/blog-posts', data);
    return NextResponse.json(result);
  } catch (error) {
    console.error('Error generating blog post:', error);
    return NextResponse.json({ success: false, error: 'Failed to generate blog post' }, { status: 500 });
  }
}
