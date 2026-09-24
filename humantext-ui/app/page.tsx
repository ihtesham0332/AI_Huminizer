import Link from 'next/link';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'HumanText AI | Undetectable AI Humanizer & Ghostwriter',
  description: 'Bypass AI detectors instantly. HumanText uses an advanced multi-agent architecture to humanize your ChatGPT and Claude text naturally.',
  keywords: 'AI humanizer, bypass AI detection, undetectable AI, rewrite AI text',
}

export default function LandingPage() {
  return (
    <main className="landing-page">
      {/* Navigation */}
      <nav className="flex justify-between items-center px-4 py-4 md:px-8 border-b border-gray-800">
        <div className="font-bold text-lg md:text-xl">HumanText <span className="text-gradient">AI</span></div>
        <div className="flex gap-4">
          <Link href="/dashboard" className="no-underline">
            <button className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-white font-medium transition-colors text-sm md:text-base">Get Started</button>
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="text-center px-4 py-16 md:py-24 max-w-4xl mx-auto">
        <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
          Make AI Text <br/><span className="text-gradient">100% Undetectable.</span>
        </h1>
        <p className="text-lg md:text-xl text-gray-400 mb-10 max-w-2xl mx-auto px-4">
          Stop relying on cheap synonym-swappers. HumanText utilizes a sophisticated LangGraph multi-agent brain to protect your citations and rewrite text with true human rhythm.
        </p>
        <Link href="/dashboard" className="inline-block mt-4">
          <button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-bold py-4 px-8 rounded-full shadow-lg transform transition hover:scale-105 text-lg">
            Try HumanText for Free
          </button>
        </Link>
      </section>

      <section className="px-4 py-16 md:py-24 bg-[var(--bg-card)]">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-center text-3xl md:text-5xl font-bold mb-12">Local, Open-Source Power</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            
            <article className="glass-panel">
              <h3 className="text-gradient">🛡️ Fact & Citation Guardians</h3>
              <p style={{ color: 'var(--text-secondary)' }}>Our agents extract and protect your numbers, dates, and APA/IEEE citations before rewriting ever begins. 100% hallucination-free.</p>
            </article>

            <article className="glass-panel">
              <h3 className="text-gradient">👻 Ninja & Ghost Modes</h3>
              <p style={{ color: 'var(--text-secondary)' }}>Need to bypass Turnitin or GPTZero? Switch to Ghost Mode for aggressive, deep structural rewrites that destroy AI watermarks.</p>
            </article>

            <article className="glass-panel">
              <h3 className="text-gradient">👨‍💻 Personal Writing DNA</h3>
              <p style={{ color: 'var(--text-secondary)' }}>Upload your previous essays. We use vector embeddings to learn your exact stylistic voice and enforce it on the AI.</p>
            </article>

          </div>
        </div>
      </section>



      <footer className="px-4 py-8 text-center text-gray-500 border-t border-gray-800">
        <p className="mb-4">&copy; 2026 HumanText AI. All rights reserved.</p>
        <div className="flex flex-col sm:flex-row justify-center gap-4 sm:gap-6 text-sm">
          <a href="/privacy" className="hover:text-gray-300 transition-colors underline">Privacy Policy</a>
          <a href="/terms" className="hover:text-gray-300 transition-colors underline">Terms of Service</a>
          <a href="/contact" className="hover:text-gray-300 transition-colors underline">Contact Support</a>
        </div>
      </footer>
    </main>
  );
}
