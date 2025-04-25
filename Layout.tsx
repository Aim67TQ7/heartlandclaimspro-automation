'use client';

import React, { ReactNode } from 'react';
import Header from './Header';
import Footer from './Footer';
import Sidebar from './Sidebar';

interface LayoutProps {
  children: ReactNode;
  showSidebar?: boolean;
}

export default function Layout({ children, showSidebar = true }: LayoutProps) {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <div className="flex flex-grow">
        {showSidebar && (
          <Sidebar />
        )}
        <main className="flex-grow p-6">
          <div className="container mx-auto">
            {children}
          </div>
        </main>
      </div>
      <Footer />
    </div>
  );
}
