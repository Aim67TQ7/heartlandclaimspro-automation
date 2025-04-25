'use client';

import React from 'react';
import Layout from '@/components/Layout';
import PageHeader from '@/components/PageHeader';
import Card from '@/components/Card';
import Button from '@/components/Button';
import LoadingSpinner from '@/components/LoadingSpinner';

export default function Dashboard() {
  return (
    <Layout>
      <PageHeader 
        title="Dashboard" 
        description="Welcome to the Blog Automation System"
        actions={
          <Button variant="primary">Generate New Blog Post</Button>
        }
      />
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <Card title="Blog Posts">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-3xl font-bold text-gray-dark">12</p>
              <p className="text-sm text-gray-500">Total blog posts</p>
            </div>
            <div className="p-3 bg-blue-100 rounded-full">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
              </svg>
            </div>
          </div>
          <div className="mt-4">
            <div className="flex justify-between text-sm">
              <span>Published</span>
              <span>8</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
              <div className="bg-green-500 h-2 rounded-full" style={{ width: '66.7%' }}></div>
            </div>
          </div>
        </Card>
        
        <Card title="SEO Performance">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-3xl font-bold text-gray-dark">78</p>
              <p className="text-sm text-gray-500">Average SEO score</p>
            </div>
            <div className="p-3 bg-green-100 rounded-full">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
          </div>
          <div className="mt-4">
            <div className="flex justify-between text-sm">
              <span>Target</span>
              <span>85</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
              <div className="bg-primary h-2 rounded-full" style={{ width: '78%' }}></div>
            </div>
          </div>
        </Card>
        
        <Card title="Upcoming Posts">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-3xl font-bold text-gray-dark">4</p>
              <p className="text-sm text-gray-500">Scheduled posts</p>
            </div>
            <div className="p-3 bg-purple-100 rounded-full">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
          <div className="mt-4">
            <div className="text-sm text-gray-500">Next post in</div>
            <div className="text-lg font-semibold text-gray-dark">3 days</div>
          </div>
        </Card>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Recent Blog Posts">
          <div className="space-y-4">
            <div className="flex items-center justify-between p-2 hover:bg-gray-50 rounded-md">
              <div>
                <h4 className="font-medium text-gray-dark">Understanding Storm Damage Insurance Claims</h4>
                <p className="text-sm text-gray-500">Published on Apr 20, 2025</p>
              </div>
              <div className="flex space-x-2">
                <span className="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">Published</span>
                <span className="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800">SEO: 85</span>
              </div>
            </div>
            
            <div className="flex items-center justify-between p-2 hover:bg-gray-50 rounded-md">
              <div>
                <h4 className="font-medium text-gray-dark">5 Steps to Document Hail Damage for Insurance</h4>
                <p className="text-sm text-gray-500">Published on Apr 15, 2025</p>
              </div>
              <div className="flex space-x-2">
                <span className="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">Published</span>
                <span className="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800">SEO: 92</span>
              </div>
            </div>
            
            <div className="flex items-center justify-between p-2 hover:bg-gray-50 rounded-md">
              <div>
                <h4 className="font-medium text-gray-dark">How to Appeal a Denied Storm Damage Claim</h4>
                <p className="text-sm text-gray-500">Draft saved on Apr 22, 2025</p>
              </div>
              <div className="flex space-x-2">
                <span className="px-2 py-1 text-xs rounded-full bg-yellow-100 text-yellow-800">Draft</span>
                <span className="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800">SEO: 76</span>
              </div>
            </div>
          </div>
          <div className="mt-4 text-center">
            <Button variant="outline" size="sm">View All Posts</Button>
          </div>
        </Card>
        
        <Card title="Upcoming Schedule">
          <div className="space-y-4">
            <div className="flex items-center p-2 hover:bg-gray-50 rounded-md">
              <div className="flex-shrink-0 w-12 h-12 bg-primary-light rounded-md flex items-center justify-center text-white font-bold">
                <div className="text-center">
                  <div className="text-xs">APR</div>
                  <div className="text-lg">28</div>
                </div>
              </div>
              <div className="ml-4">
                <h4 className="font-medium text-gray-dark">Wind Damage Assessment Guide</h4>
                <p className="text-sm text-gray-500">Educational guide</p>
              </div>
            </div>
            
            <div className="flex items-center p-2 hover:bg-gray-50 rounded-md">
              <div className="flex-shrink-0 w-12 h-12 bg-primary-light rounded-md flex items-center justify-center text-white font-bold">
                <div className="text-center">
                  <div className="text-xs">MAY</div>
                  <div className="text-lg">05</div>
                </div>
              </div>
              <div className="ml-4">
                <h4 className="font-medium text-gray-dark">Preparing for Hurricane Season</h4>
                <p className="text-sm text-gray-500">Seasonal content</p>
              </div>
            </div>
            
            <div className="flex items-center p-2 hover:bg-gray-50 rounded-md">
              <div className="flex-shrink-0 w-12 h-12 bg-primary-light rounded-md flex items-center justify-center text-white font-bold">
                <div className="text-center">
                  <div className="text-xs">MAY</div>
                  <div className="text-lg">12</div>
                </div>
              </div>
              <div className="ml-4">
                <h4 className="font-medium text-gray-dark">Working with Public Adjusters</h4>
                <p className="text-sm text-gray-500">Expert insights</p>
              </div>
            </div>
          </div>
          <div className="mt-4 text-center">
            <Button variant="outline" size="sm">View Full Schedule</Button>
          </div>
        </Card>
      </div>
    </Layout>
  );
}
