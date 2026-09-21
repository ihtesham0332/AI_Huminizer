import Workspace from '../components/Workspace';

export default function Home() {
  return (
    <main>
      <header style={{ padding: '24px 0', borderBottom: '1px solid var(--border-color)', background: 'var(--bg-card)', backdropFilter: 'blur(16px)' }}>
        <div className="container flex-between" style={{ padding: '0 2rem', margin: '0 auto' }}>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700, letterSpacing: '-0.05em' }}>
            <span style={{ color: 'var(--text-primary)' }}>HumanText</span>
            <span className="text-gradient">Engine</span>
          </h1>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
            <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--success-color)', boxShadow: '0 0 10px var(--success-color)' }}></div>
            Local Qwen2.5 Online
          </div>
        </div>
      </header>
      
      <section style={{ paddingTop: '2rem' }}>
        <div className="container animate-fade-up" style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h1 style={{ fontSize: '3rem', marginBottom: '16px' }}>Instantly <span className="text-gradient">Humanize</span> AI Text.</h1>
          <p style={{ fontSize: '1.2rem', color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto' }}>
            Powered by a local, fully private multi-agent LangGraph orchestration. Strip away robotic jargon in seconds.
          </p>
        </div>

        <Workspace />
      </section>
    </main>
  );
}
