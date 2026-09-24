'use client';
import React, { useState, useMemo } from 'react';
import ControlPanel from './ControlPanel';
import ScoreDial from './ScoreDial';
import { humanizeText, streamHumanizeText, rewriteSentence, scanTextProbability } from '../lib/api';

export default function Workspace() {
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [viewDiff, setViewDiff] = useState(false);
  
  const [documentType, setDocumentType] = useState('business');
  const [targetMode, setTargetMode] = useState('natural');
  const [targetTone, setTargetTone] = useState('clear');
  const [targetAudience, setTargetAudience] = useState('general');
  const [bypassStrength, setBypassStrength] = useState('standard');

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  
  const [qualityScore, setQualityScore] = useState(0);
  const [naturalScore, setNaturalScore] = useState(0);

  const [activeSentenceIndex, setActiveSentenceIndex] = useState<number | null>(null);
  const [variations, setVariations] = useState<string[]>([]);
  const [isVariationsLoading, setIsVariationsLoading] = useState(false);

  const [scanResult, setScanResult] = useState<{ai_probability: number, human_probability: number, verdict: string, burstiness_score: number} | null>(null);
  const [isScanning, setIsScanning] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(outputText);
    alert("Copied to clipboard!");
  };

  const handleDownload = () => {
    const element = document.createElement("a");
    const file = new Blob([outputText], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = "humanized_text.txt";
    document.body.appendChild(element);
    element.click();
  };

  const handleScan = async () => {
    if (!outputText) return;
    setIsScanning(true);
    setScanResult(null);
    try {
      const res = await scanTextProbability(outputText);
      setScanResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsScanning(false);
    }
  };

  const handleSentenceClick = async (sentence: string, index: number) => {
    // If it's just whitespace, ignore
    if (!sentence.trim()) return;
    
    if (activeSentenceIndex === index) {
      setActiveSentenceIndex(null); // toggle off
      return;
    }

    setActiveSentenceIndex(index);
    setVariations([]);
    setIsVariationsLoading(true);
    
    try {
       const ctx = outputText.substring(0, 500); 
       const vars = await rewriteSentence(sentence, ctx, targetTone);
       setVariations(vars);
    } catch (err) {
       console.error("Failed to load variations", err);
    } finally {
       setIsVariationsLoading(false);
    }
  };

  const replaceSentence = (index: number, newVar: string, originalFrags: string[]) => {
     const newFrags = [...originalFrags];
     const hasSpace = newFrags[index].endsWith(' ') || newFrags[index].endsWith('\n');
     newFrags[index] = newVar + (hasSpace && !newVar.endsWith(' ') ? ' ' : '');
     setOutputText(newFrags.join(""));
     setActiveSentenceIndex(null);
  };

  const outputFragments = useMemo(() => {
     return outputText.match(/[^.?!]+[.?!]+(?:\s+|$)|[^.?!]+$/g) || [outputText];
  }, [outputText]);

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
    setViewDiff(false);

    try {
      const stream = streamHumanizeText({
        text: inputText,
        document_type: documentType,
        target_mode: targetMode,
        target_tone: targetTone,
        target_audience: targetAudience,
        bypass_strength: bypassStrength
      });
      
      for await (const data of stream) {
        if (data.event === 'start') {
          // Stream started
        } else if (data.event === 'token') {
          setOutputText(prev => prev + data.text);
        } else if (data.event === 'complete') {
          setQualityScore(data.quality_score);
          setNaturalScore(data.naturalness_score);
        } else if (data.event === 'error') {
          setError(data.message || 'Stream encountered an error.');
        }
      }
      
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred. Is the API running?');
    } finally {
      setIsLoading(false);
    }
  };

  // Zero-Bloat O(N) Fast Set Diff Algorithm
  const renderDiff = () => {
    if (!outputText) return null;
    
    const originalWords = new Set(inputText.split(/\s+/).filter(w => w.length > 0).map(w => w.toLowerCase().replace(/[.,!?;:()[\]]/g, '')));
    const humanizedTokens = outputText.split(/(\s+)/);
    
    return humanizedTokens.map((token, i) => {
        if (!token.trim()) return <span key={i}>{token}</span>; // whitespace
        const cleanWord = token.toLowerCase().replace(/[.,!?;:()[\]]/g, '');
        if (!originalWords.has(cleanWord) && cleanWord.length > 0) {
            return <span key={i} className="diff-added">{token}</span>;
        }
        return <span key={i}>{token}</span>;
    });
  };

  const renderDeletedDiff = () => {
    if (!outputText) return null;
    
    const outputWords = new Set(outputText.split(/\s+/).filter(w => w.length > 0).map(w => w.toLowerCase().replace(/[.,!?;:()[\]]/g, '')));
    const inputTokens = inputText.split(/(\s+)/);
    
    return inputTokens.map((token, i) => {
        if (!token.trim()) return <span key={i}>{token}</span>; // whitespace
        const cleanWord = token.toLowerCase().replace(/[.,!?;:()[\]]/g, '');
        if (!outputWords.has(cleanWord) && cleanWord.length > 0) {
            return <span key={i} className="diff-removed">{token}</span>;
        }
        return <span key={i}>{token}</span>;
    });
  };

  return (
    <div className="container animate-fade-up">
      <ControlPanel 
        documentType={documentType} setDocumentType={setDocumentType}
        targetMode={targetMode} setTargetMode={setTargetMode}
        targetTone={targetTone} setTargetTone={setTargetTone}
        targetAudience={targetAudience} setTargetAudience={setTargetAudience}
        bypassStrength={bypassStrength} setBypassStrength={setBypassStrength}
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
            <div className="flex-between" style={{ marginBottom: '16px', alignItems: 'center' }}>
            <h2 className="text-gradient">Humanized Output</h2>
            {/* Show scores and toggle if available */}
            <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
              {outputText && (
                <button 
                  onClick={() => setViewDiff(!viewDiff)}
                  style={{
                    padding: '6px 12px',
                    borderRadius: '4px',
                    border: '1px solid var(--border-light)',
                    background: viewDiff ? 'var(--accent-primary)' : 'rgba(255,255,255,0.05)',
                    color: viewDiff ? '#000' : 'var(--text-primary)',
                    cursor: 'pointer',
                    fontSize: '0.85rem',
                    transition: 'all 0.2s ease'
                  }}
                >
                  {viewDiff ? 'Standard View' : 'View Changes'}
                </button>
              )}
              {qualityScore > 0 && (
                 <div style={{ display: 'flex', gap: '24px' }}>
                   <ScoreDial score={qualityScore} label="Quality" color="var(--accent-primary)" />
                   <ScoreDial score={naturalScore} label="Natural" color="var(--success-color)" />
                 </div>
              )}
            </div>
          </div>
          
          <div 
            className={`glass-input ${isLoading ? 'skeleton' : ''}`}
            style={{ flexGrow: 1, minHeight: '400px', backgroundColor: 'rgba(0,0,0,0.4)', overflowY: 'auto', padding: '16px', whiteSpace: 'pre-wrap' }}
          >
            {isLoading && !outputText ? (
               <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-secondary)' }}>
                 AI is thinking...
               </div>
            ) : viewDiff ? (
              <div className="diff-view" style={{ fontSize: '1.05rem', lineHeight: '1.6' }}>
                <div style={{ marginBottom: '24px', padding: '12px', background: 'rgba(239, 68, 68, 0.05)', borderLeft: '4px solid #ef4444' }}>
                  <h4 style={{ color: '#ef4444', marginBottom: '8px', fontSize: '0.9rem', textTransform: 'uppercase' }}>Deleted Original Words</h4>
                  <div>{renderDeletedDiff()}</div>
                </div>
                <div style={{ padding: '12px', background: 'rgba(16, 185, 129, 0.05)', borderLeft: '4px solid #10b981' }}>
                  <h4 style={{ color: '#10b981', marginBottom: '8px', fontSize: '0.9rem', textTransform: 'uppercase' }}>Added Humanized Words</h4>
                  <div>{renderDiff()}</div>
                </div>
              </div>
            ) : (
               <div style={{ position: 'relative' }}>
                  {outputText ? outputFragments.map((frag, idx) => (
                    <React.Fragment key={idx}>
                      <span 
                        className="interactive-sentence"
                        onClick={() => handleSentenceClick(frag, idx)}
                        title="Click to rewrite this sentence"
                      >
                        {frag}
                      </span>
                      {activeSentenceIndex === idx && (
                        <div className="sentence-modal">
                          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px' }}>
                            <strong style={{ color: 'var(--accent-primary)' }}>Rewrite Variations</strong>
                            <button onClick={(e) => { e.stopPropagation(); setActiveSentenceIndex(null); }} style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer', fontSize: '1.2rem' }}>✕</button>
                          </div>
                          
                          {isVariationsLoading ? (
                            <div style={{ padding: '24px 16px', textAlign: 'center', color: 'var(--text-secondary)' }}>
                              <div className="skeleton" style={{ height: '20px', width: '100%', marginBottom: '8px' }}></div>
                              <div className="skeleton" style={{ height: '20px', width: '90%', marginBottom: '8px' }}></div>
                              <div className="skeleton" style={{ height: '20px', width: '95%' }}></div>
                            </div>
                          ) : (
                            variations.map((v, i) => (
                              <button key={i} className="variation-btn" onClick={() => replaceSentence(idx, v, outputFragments)}>
                                {v}
                              </button>
                            ))
                          )}
                        </div>
                      )}
                    </React.Fragment>
                  )) : (
                    <span style={{ color: 'var(--text-secondary)' }}>Your human-sounding text will appear here.</span>
                  )}
               </div>
            )}
          </div>

          {/* Action Bar */}
          {outputText && (
            <div style={{ marginTop: '16px', display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
              <button className="action-btn-small" onClick={handleCopy}>📋 Copy to Clipboard</button>
              <button className="action-btn-small" onClick={handleDownload}>💾 Download .txt</button>
              <button 
                className="action-btn-small" 
                style={{ background: 'var(--accent-primary)', color: 'white', border: 'none', marginLeft: 'auto' }}
                onClick={handleScan}
                disabled={isScanning}
              >
                {isScanning ? '🔍 Scanning...' : '🔍 Scan for AI'}
              </button>
            </div>
          )}
        </div>
        
        {/* Scan Results */}
        {scanResult && (
          <div className="glass-panel" style={{ marginTop: '16px', animation: 'fadeUp 0.3s ease' }}>
            <h3 style={{ marginBottom: '12px' }}>Integrated AI Detector Scan</h3>
            <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
              <div style={{ flex: 1 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <span style={{ color: 'var(--success-color)' }}>Human: {Math.round(scanResult.human_probability * 100)}%</span>
                  <span style={{ color: 'var(--danger-color)' }}>AI: {Math.round(scanResult.ai_probability * 100)}%</span>
                </div>
                <div style={{ width: '100%', height: '12px', background: 'var(--danger-color)', borderRadius: '6px', overflow: 'hidden' }}>
                  <div style={{ width: `${scanResult.human_probability * 100}%`, height: '100%', background: 'var(--success-color)', transition: 'width 1s ease' }}></div>
                </div>
              </div>
              <div style={{ textAlign: 'right', minWidth: '150px' }}>
                <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: scanResult.human_probability > 0.6 ? 'var(--success-color)' : 'var(--warning-color)' }}>
                  {scanResult.verdict}
                </div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                  Burstiness: {scanResult.burstiness_score}
                </div>
              </div>
            </div>
          </div>
        )}
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
