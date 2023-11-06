/** @format */

import type { Metadata } from 'next';
import { Roboto } from 'next/font/google';
import styles from '@/styles/globals.module.scss';

const roboto = Roboto({ subsets: ['latin'], weight: '400' });

export const metadata: Metadata = {
  title: 'Hom3lab',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${styles.body} roboto.className`}>{children}</body>
    </html>
  );
}
