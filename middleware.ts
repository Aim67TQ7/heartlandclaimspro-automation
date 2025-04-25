import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

// Middleware to check if user is authenticated
export function middleware(request: NextRequest) {
  // Get session ID from cookie
  const sessionId = request.cookies.get('session_id')?.value;
  
  // Check if path requires authentication
  const isAuthPath = request.nextUrl.pathname.startsWith('/api/auth');
  const isLoginPath = request.nextUrl.pathname === '/api/auth/login';
  const isPublicPath = request.nextUrl.pathname === '/' || 
                       request.nextUrl.pathname === '/login' || 
                       request.nextUrl.pathname.startsWith('/_next');
  
  // Allow access to public paths and login API without authentication
  if (isPublicPath || (isAuthPath && isLoginPath)) {
    return NextResponse.next();
  }
  
  // If no session ID, redirect to login
  if (!sessionId) {
    // If API request, return 401
    if (request.nextUrl.pathname.startsWith('/api/')) {
      return NextResponse.json({ success: false, error: 'Unauthorized' }, { status: 401 });
    }
    
    // Otherwise redirect to login page
    const url = new URL('/login', request.url);
    url.searchParams.set('from', request.nextUrl.pathname);
    return NextResponse.redirect(url);
  }
  
  // Continue with the request
  return NextResponse.next();
}

// Configure which paths the middleware applies to
export const config = {
  matcher: [
    // Apply to all paths except public assets
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
}
