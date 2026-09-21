'use client';
import React from 'react';

interface ControlPanelProps {
  documentType: string;
  setDocumentType: (val: string) => void;
  targetMode: string;
  setTargetMode: (val: string) => void;
  targetTone: string;
  setTargetTone: (val: string) => void;
  targetAudience: string;
  setTargetAudience: (val: string) => void;
}

export default function ControlPanel({
  documentType, setDocumentType,
  targetMode, setTargetMode,
  targetTone, setTargetTone,
  targetAudience, setTargetAudience
}: ControlPanelProps) {
  return (
    <div className="glass-panel" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '24px' }}>
      
      <div>
        <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>Document Type</label>
        <select className="glass-select" value={documentType} onChange={e => setDocumentType(e.target.value)}>
          <option value="business">Business / Corporate</option>
          <option value="academic">Academic / Research</option>
          <option value="creative">Creative / Fiction</option>
          <option value="casual">Casual / Social</option>
        </select>
      </div>

      <div>
        <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>Target Mode</label>
        <select className="glass-select" value={targetMode} onChange={e => setTargetMode(e.target.value)}>
          <option value="natural">Natural (Default)</option>
          <option value="professional">Professional</option>
          <option value="simplified">Simplified</option>
          <option value="persuasive">Persuasive</option>
        </select>
      </div>

      <div>
        <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>Target Tone</label>
        <select className="glass-select" value={targetTone} onChange={e => setTargetTone(e.target.value)}>
          <option value="clear">Clear & Direct</option>
          <option value="conversational">Conversational</option>
          <option value="formal">Formal & Polite</option>
          <option value="enthusiastic">Enthusiastic</option>
        </select>
      </div>

      <div>
        <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>Target Audience</label>
        <select className="glass-select" value={targetAudience} onChange={e => setTargetAudience(e.target.value)}>
          <option value="general">General Public</option>
          <option value="experts">Domain Experts</option>
          <option value="coworkers">Coworkers / Team</option>
          <option value="students">Students / Beginners</option>
        </select>
      </div>

    </div>
  );
}
