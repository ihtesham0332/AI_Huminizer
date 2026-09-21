'use client';
import React, { useState } from 'react';
import ControlPanel from './ControlPanel';
import ScoreDial from './ScoreDial';
import { humanizeText } from '../lib/api';

export default function Workspace() {
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  
  const [documentType, setDocumentType] = useState('business');
  const [targetMode, setTargetMode] = useState('natural');
  const [targetTone, setTargetTone] = useState('clear');
  const [targetAudience, setTargetAudience] = useState('general');

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  
  const [qualityScore, setQualityScore] = useState(0);
  const [naturalScore, setNaturalScore] = useState(0);

  const handleHumanize = async () => {
    if (!inputText.trim()) {
      setError("Please enter some text to humanize.");
      return;
    }

    setIsLoading(true);
    setError('');
    setOutputText('');
    setQualityScore(0);
    setNaturalScore(0);

    try {
      const response = await humanizeText({
        text: inputText,
        document_type: documentType,
        target_mode: targetMode,
        target_tone: targetTone,
        target_audience: targetAudience
      });
      
      // Simulate typing effect for the output
      let i = 0;
      const resultText = response.humanized_text;
      const typeInterval = setInterval(() => {
        setOutputText(prev => prev + resultText.charAt(i));
        i++;
        if (i >= resultText.length) {
          clearInterval(typeInterval);
          setQualityScore(response.quality_score);
          setNaturalScore(response.naturalness_score);
        }
      }, 15);
      
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred. Is the API running?');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container animate-fade-up">
      <ControlPanel 
        documentType={documentType} setDocumentType={setDocumentType}
        targetMode={targetMode} setTargetMode={setTargetMode}
        targetTone={targetTone} setTargetTone={setTargetTone}
        targetAudience={targetAudience} setTargetAudience={setTargetAudience}
      />
      
      {error && (
        <div style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid var(--danger-color)', color: 'var(--danger-color)', padding: '16px', borderRadius: '8px', marginBottom: '24px' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      <div className="grid-2">
        {/* Left Pane - Input */}
        <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column' }}>
          <div className="flex-between" style={{ marginBottom: '16px' }}>
            <h2 style={{ color: 'var(--accent-primary)' }}>Original Text</h2>
            <span style={{ fontSize: '0.85rem', color: inputText.length > 50000 ? 'var(--danger-color)' : 'var(--text-secondary)' }}>
              {inputText.length.toLocaleString()} / 50,000 max
            </span>
          </div>
          <textarea 
            className="glass-input" 
            placeholder="Paste your robotic or AI-generated text here..."
            style={{ flexGrow: 1, minHeight: '400px' }}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
          />
        </div>

        {/* Right Pane - Output */}
        <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', position: 'relative' }}>
          <div className="flex-between" style={{ marginBottom: '16px' }}>
            <h2 className="text-gradient">Humanized Output</h2>
            {/* Show scores if available */}
            {qualityScore > 0 && (
               <div style={{ display: 'flex', gap: '24px' }}>
                 <ScoreDial score={qualityScore} label="Quality" color="var(--accent-primary)" />
                 <ScoreDial score={naturalScore} label="Natural" color="var(--success-color)" />
               </div>
            )}
          </div>
          
          <div 
            className={`glass-input ${isLoading ? 'skeleton' : ''}`}
            style={{ flexGrow: 1, minHeight: '400px', backgroundColor: 'rgba(0,0,0,0.4)', overflowY: 'auto' }}
          >
            {isLoading && !outputText ? (
               <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-secondary)' }}>
                 AI is thinking...
               </div>
            ) : (
               <p style={{ whiteSpace: 'pre-wrap' }}>{outputText}</p>
            )}
          </div>
        </div>
      </div>

      <div className="flex-center" style={{ marginTop: '32px' }}>
        <button 
          className="btn-primary" 
          onClick={handleHumanize}
          disabled={isLoading}
          style={{ fontSize: '1.2rem', padding: '16px 48px', minWidth: '300px' }}
        >
          {isLoading ? 'Humanizing...' : 'Humanize Text ✨'}
        </button>
      </div>
    </div>
  );
}
