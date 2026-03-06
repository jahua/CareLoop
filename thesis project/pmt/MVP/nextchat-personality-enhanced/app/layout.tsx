/**
 * NextChat-Enhanced: Root Layout
 * Combines NextChat patterns with Phase 1 personality features
 */

import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'NextChat-Enhanced | Personality-Adaptive AI',
  description: 'NextChat enhanced with Phase 1 multi-agent personality detection and therapeutic adaptation',
  keywords: [
    'NextChat',
    'personality AI',
    'OCEAN traits',
    'therapeutic chatbot',
    'multi-agent system',
    'EMA smoothing',
    'personality detection'
  ],
  authors: [{ name: 'NextChat-Enhanced Team' }],
  viewport: 'width=device-width, initial-scale=1',
  robots: 'index, follow',
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ffffff' },
    { media: '(prefers-color-scheme: dark)', color: '#000000' },
  ],
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon.png',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
        <meta name="theme-color" content="#000000" />
        <link rel="manifest" href="/manifest.json" />
        
        {/* NextChat-Enhanced Meta */}
        <meta name="nextchat-enhanced-version" content="2.16.1-personality-v1.0" />
        <meta name="personality-detection" content="enabled" />
        <meta name="multi-agent-system" content="phase1" />
      </head>
      <body className={inter.className}>
        <div id="root">
          {children}
        </div>
        
        {/* Phase 1 System Status */}
        <div id="system-status" style={{ display: 'none' }}>
          <span data-personality="enabled" />
          <span data-ema-smoothing="enabled" />
          <span data-multi-agent="enabled" />
          <span data-verification="enabled" />
        </div>
      </body>
    </html>
  );
}

















































