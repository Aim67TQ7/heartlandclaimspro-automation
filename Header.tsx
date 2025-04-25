'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navigation = [
  { name: 'Dashboard', href: '/' },
  { name: 'Blog Generator', href: '/blog-generator' },
  { name: 'Content Tester', href: '/content-tester' },
  { name: 'Publishing', href: '/publishing' },
  { name: 'Scheduling', href: '/scheduling' },
  { name: 'Settings', href: '/settings' },
];

export default function Header() {
  const pathname = usePathname();

  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center">
            <Link href="/" className="flex items-center">
              <span className="text-primary font-heading text-2xl font-bold">Heartland</span>
              <span className="text-primary-dark font-heading text-2xl font-bold ml-1">Claims</span>
            </Link>
          </div>
          <nav className="hidden md:flex space-x-8">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={`${
                  pathname === item.href
                    ? 'text-primary-dark font-semibold'
                    : 'text-gray-dark hover:text-primary'
                } transition-colors duration-200 font-medium`}
              >
                {item.name}
              </Link>
            ))}
          </nav>
          <div className="md:hidden">
            <button
              type="button"
              className="text-gray-dark hover:text-primary focus:outline-none"
              aria-label="Toggle menu"
            >
              <svg
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
