'use client';

import React from 'react';

export default function Footer() {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="bg-gray-dark text-white py-8 mt-auto">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-heading font-bold mb-4">Heartland Claims</h3>
            <p className="text-sm">
              Helping storm victims navigate insurance claims with automated blog content
              that provides valuable insights and guidance.
            </p>
          </div>
          <div>
            <h3 className="text-lg font-heading font-bold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li><a href="/" className="text-sm hover:text-primary-light transition-colors">Dashboard</a></li>
              <li><a href="/blog-generator" className="text-sm hover:text-primary-light transition-colors">Blog Generator</a></li>
              <li><a href="/content-tester" className="text-sm hover:text-primary-light transition-colors">Content Tester</a></li>
              <li><a href="/publishing" className="text-sm hover:text-primary-light transition-colors">Publishing</a></li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-heading font-bold mb-4">Contact</h3>
            <p className="text-sm mb-2">Have questions about our blog automation system?</p>
            <a href="mailto:contact@heartlandclaimsrpo.com" className="text-primary-light hover:underline text-sm">
              contact@heartlandclaimsrpo.com
            </a>
          </div>
        </div>
        <div className="border-t border-gray-600 mt-8 pt-4 text-center text-sm">
          <p>&copy; {currentYear} Heartland Claims. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
