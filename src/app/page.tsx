'use client';

import dynamic from 'next/dynamic';

// Avoid SSR hydration mismatch from react-resizable-panels (generates dynamic IDs)
const MainLayout = dynamic(
  () => import('@/components/layout/MainLayout').then((m) => m.MainLayout),
  { ssr: false }
);

export default function Home() {
  return <MainLayout />;
}
