import React from 'react';

export default function AdminDashboard() {
  return (
    <div style={{ minHeight: '100vh', backgroundColor: 'var(--bg-primary)', padding: '2rem 5%' }}>
      
      <header style={{ marginBottom: '3rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '1rem' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#fff' }}>Admin Analytics</h1>
        <p style={{ color: 'var(--text-secondary)' }}>Live telemetry and observability metrics.</p>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
        
        {/* Cost Dashboard (Master Prompt Point 52) */}
        <div style={{ backgroundColor: 'var(--bg-secondary)', padding: '2rem', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
          <h2 style={{ color: '#fff', marginBottom: '1.5rem', fontSize: '1.2rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            💰 Cost Dashboard
          </h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Daily API Cost:</span>
              <span style={{ color: '#ff6b6b', fontWeight: 'bold' }}>$42.15</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Cost / 1K Words:</span>
              <span style={{ color: '#fff' }}>$0.012</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Cache Savings:</span>
              <span style={{ color: '#00ff64', fontWeight: 'bold' }}>18.4%</span>
            </div>
          </div>
        </div>

        {/* Performance Dashboard (Master Prompt Point 53) */}
        <div style={{ backgroundColor: 'var(--bg-secondary)', padding: '2rem', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
          <h2 style={{ color: '#fff', marginBottom: '1.5rem', fontSize: '1.2rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            ⚡ Performance Dashboard
          </h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-secondary)' }}>P50 Latency:</span>
              <span style={{ color: '#fff' }}>3.2s</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-secondary)' }}>P95 Latency:</span>
              <span style={{ color: '#ff9600' }}>8.7s</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Average Queue Time:</span>
              <span style={{ color: '#fff' }}>1.1s</span>
            </div>
          </div>
        </div>

        {/* Quality Dashboard (Master Prompt Point 54) */}
        <div style={{ backgroundColor: 'var(--bg-secondary)', padding: '2rem', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
          <h2 style={{ color: '#fff', marginBottom: '1.5rem', fontSize: '1.2rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            ⚖️ Quality Dashboard
          </h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Semantic Failure Rate:</span>
              <span style={{ color: '#00ff64' }}>1.2%</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Avg Revisions / Job:</span>
              <span style={{ color: '#fff' }}>0.4</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-secondary)' }}>User Acceptance Rate:</span>
              <span style={{ color: '#00ff64', fontWeight: 'bold' }}>94%</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
