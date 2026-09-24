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
  bypassStrength: string;
  setBypassStrength: (val: string) => void;
}

export default function ControlPanel({
  documentType, setDocumentType,
  targetMode, setTargetMode,
  targetTone, setTargetTone,
  targetAudience, setTargetAudience,
  bypassStrength, setBypassStrength
}: ControlPanelProps) {
  return (
    <div className="glass-panel" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '24px' }}>
      
      <div>
        <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>Bypass Strength</label>
        <select className="glass-select" value={bypassStrength} onChange={(e) => setBypassStrength(e.target.value)}>
          <option value="standard">Standard (0.6 Temp)</option>
          <option value="high">High (0.85 Temp)</option>
          <option value="extreme">Extreme (1.0 Temp)</option>
        </select>
      </div>

      <div>
        <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>Document Type</label>
        <select className="glass-select" value={documentType} onChange={(e) => setDocumentType(e.target.value)}>
          <option value="business">Business / Corporate</option>
          <option value="academic">Academic Essay</option>
          <option value="blog">Blog Post</option>
          <option value="casual">Casual / Social</option>
        </select>
      </div>

      <div>
        <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>Target Mode</label>
        <select className="glass-select" value={targetMode} onChange={(e) => setTargetMode(e.target.value)}>
          <option value="natural">Natural (Default)</option>
          <option value="creative">Highly Creative</option>
          <option value="formal">Strictly Formal</option>
        </select>
      </div>

      <div>
        <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>Target Tone</label>
        <select className="glass-select" value={targetTone} onChange={(e) => setTargetTone(e.target.value)}>
          <option value="clear">Clear & Direct</option>
          <option value="persuasive">Persuasive</option>
          <option value="friendly">Friendly</option>
          <option value="academic">Academic / Neutral</option>
        </select>
      </div>

      <div>
        <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>Target Audience</label>
        <select className="glass-select" value={targetAudience} onChange={(e) => setTargetAudience(e.target.value)}>
          <option value="general">General Public</option>
          <option value="executives">Executives</option>
          <option value="experts">Subject Matter Experts</option>
          <option value="students">Students</option>
        </select>
      </div>
    </div>
  );
}
