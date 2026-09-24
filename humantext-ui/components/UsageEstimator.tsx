'use client';

import React from 'react';

interface UsageEstimatorProps {
  words: number;
  mode: string;
  candidates: number;
  verificationLevel: string;
  estimatedCredits: number;
  onConfirm: () => void;
  onCancel: () => void;
}

export default function UsageEstimator({
  words, mode, candidates, verificationLevel, estimatedCredits, onConfirm, onCancel
}: UsageEstimatorProps) {
  return (
    <div style={{
      position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
      backgroundColor: 'rgba(0,0,0,0.8)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000
    }}>
      <div style={{
        backgroundColor: 'var(--bg-secondary)', padding: '2rem', borderRadius: '12px',
        border: '1px solid var(--border-color)', maxWidth: '400px', width: '100%',
        boxShadow: '0 0 40px rgba(0, 112, 243, 0.2)'
      }}>
        <h2 style={{ marginBottom: '1.5rem', color: '#fff' }}>Estimated Usage</h2>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem', color: 'var(--text-secondary)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>Words:</span> <span style={{ color: '#fff' }}>{words.toLocaleString()}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>Mode:</span> <span style={{ color: '#fff', textTransform: 'capitalize' }}>{mode}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>Candidates:</span> <span style={{ color: '#fff' }}>{candidates}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>Verification:</span> <span style={{ color: '#fff' }}>{verificationLevel}</span>
          </div>
        </div>

        <div style={{ 
          marginTop: '1.5rem', paddingTop: '1.5rem', borderTop: '1px solid var(--border-color)',
          display: 'flex', justifyContent: 'space-between', alignItems: 'center'
        }}>
          <span style={{ fontSize: '1.1rem', color: '#fff' }}>Estimated credits:</span>
          <span style={{ fontSize: '1.4rem', fontWeight: 'bold', color: 'var(--accent-primary)' }}>
            {estimatedCredits.toFixed(1)}
          </span>
        </div>

        <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem' }}>
          <button 
            onClick={onCancel}
            style={{ flex: 1, padding: '0.8rem', backgroundColor: 'transparent', border: '1px solid var(--border-color)', color: '#fff', borderRadius: '6px', cursor: 'pointer' }}
          >
            Cancel
          </button>
          <button 
            onClick={onConfirm}
            style={{ flex: 1, padding: '0.8rem', backgroundColor: 'var(--accent-primary)', border: 'none', color: '#fff', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold' }}
          >
            Continue
          </button>
        </div>
      </div>
    </div>
  );
}
