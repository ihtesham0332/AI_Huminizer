import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'HumanText Engine | AI Text Transformation',
  description: 'Advanced Multi-Agent Natural Text Transformation System',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
