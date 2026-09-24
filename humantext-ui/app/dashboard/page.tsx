'use client';

import React, { useState } from 'react';
import AdvancedWorkspace from '../../components/AdvancedWorkspace';
import DiffViewer from '../../components/DiffViewer';

export default function Dashboard() {
  const [showDiff, setShowDiff] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [originalText, setOriginalText] = useState('');
  const [humanizedText, setHumanizedText] = useState('');
  const [facts, setFacts] = useState<string[]>([]);
  const [citations, setCitations] = useState<string[]>([]);
  const [showProfileModal, setShowProfileModal] = useState(false);
  const [activeProfile, setActiveProfile] = useState('Default Profile');
  const [profileInstructions, setProfileInstructions] = useState('');
  const [processingMode, setProcessingMode] = useState('Balanced (Standard Humanize)');
  const [outputLength, setOutputLength] = useState('Maintain Original Length');
  const [modalInputName, setModalInputName] = useState('');
  const [modalInputInstr, setModalInputInstr] = useState('');

  const handleRewriteRequest = async (text: string) => {
    setOriginalText(text);
    setIsProcessing(true);
    
    const payload = {
      text: text,
      mode: processingMode.split(' ')[0].toLowerCase(), // e.g. "balanced", "ghost", "deep", "creative"
      length: outputLength.split(' ')[0].toLowerCase(), // e.g. "maintain", "condense", "expand"
      profile_instructions: activeProfile === 'Custom Profile' ? profileInstructions : null
    };

    try {
      // Primary: Use internal Next.js API proxy for stable, resilient routing
      let response = await fetch('/api/humanize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });
      
      // Fallback: Direct backend call if proxy is unreachable
      if (!response.ok && response.status === 502) {
        try {
          response = await fetch('http://localhost:8000/api/v1/humanize/v5', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
          });
        } catch {
          // Keep initial response if direct call also fails
        }
      }

      const data = await response.json();
      
      if (response.ok) {
        setHumanizedText(data.humanized_text);
        setFacts(data.facts_protected || []);
        setCitations(data.citations_protected || []);
      } else {
        setHumanizedText(`Error: ${data.error || data.detail || 'Failed to process document'}`);
      }
    } catch (error: any) {
      setHumanizedText(`Network Error: ${error?.message || 'Please ensure the backend is running on http://localhost:8000'}`);
    } finally {
      setIsProcessing(false);
      setShowDiff(true);
    }
  };

  return (
    <div className="min-h-screen bg-[var(--bg-primary)] font-sans">
      
      {/* Header */}
      <header className="px-4 md:px-8 py-5 border-b border-gray-800 flex justify-between items-center bg-[var(--bg-secondary)] sticky top-0 z-50">
        <div className="flex items-center gap-2 md:gap-3">
          <div className="w-8 h-8 rounded bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold text-lg md:text-xl">
            H
          </div>
          <h1 className="text-xl md:text-2xl font-bold text-white tracking-tight">
            HumanText <span className="hidden sm:inline text-gray-500 font-light">Workspace</span>
          </h1>
        </div>
        
      </header>

      {/* Main Layout */}
      <div className="flex flex-col lg:grid lg:grid-cols-12 gap-6 p-4 md:p-8 max-w-[1800px] mx-auto">
        
        {/* Left Sidebar: Controls */}
        <div className="w-full lg:col-span-3 space-y-6">
          


          <div className="glass-panel p-5">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider">Writing DNA Profile</h3>
              <button 
                onClick={() => setShowProfileModal(true)}
                className="text-xs text-blue-400 hover:text-blue-300 transition-colors"
              >
                + Configure
              </button>
            </div>
            <select 
              className="w-full bg-gray-900 border border-gray-700 text-gray-200 rounded-lg p-3 outline-none focus:border-blue-500 transition-colors cursor-pointer"
              value={activeProfile}
              onChange={(e) => setActiveProfile(e.target.value)}
            >
              <option>Default Profile</option>
              <option>Academic Thesis (Formal)</option>
              <option>LinkedIn Post (Casual)</option>
            </select>
            <p className="text-xs text-gray-500 mt-3 leading-relaxed">
              The Engine will inject your vocabulary and formatting preferences directly into the prompt.
            </p>
          </div>

          <div className="glass-panel p-5">
            <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-4">Processing Mode</h3>
            <select 
              className="w-full bg-gray-900 border border-gray-700 text-gray-200 rounded-lg p-3 outline-none focus:border-purple-500 transition-colors cursor-pointer"
              value={processingMode}
              onChange={(e) => setProcessingMode(e.target.value)}
            >
              <option>Balanced (Standard Humanize)</option>
              <option>Ghost Mode (Aggressive Bypass)</option>
              <option>Deep Structure (Academic)</option>
              <option>Creative (Storytelling)</option>
            </select>
            <p className="text-xs text-gray-500 mt-3 leading-relaxed">
              Adjust how aggressively the multi-agent system reconstructs your document.
            </p>
          </div>

          <div className="glass-panel p-5">
            <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-4">Output Length</h3>
            <select 
              className="w-full bg-gray-900 border border-gray-700 text-gray-200 rounded-lg p-3 outline-none focus:border-green-500 transition-colors cursor-pointer"
              value={outputLength}
              onChange={(e) => setOutputLength(e.target.value)}
            >
              <option>Maintain Original Length</option>
              <option>Condense (Shorter)</option>
              <option>Expand (More Detail)</option>
            </select>
            <p className="text-xs text-gray-500 mt-3 leading-relaxed">
              Instruct the LLM on how to manage the word count of the final rewrite.
            </p>
          </div>
          
        </div>

        {/* Right Main Area */}
        <div className="w-full lg:col-span-9">
          {isProcessing ? (
            <div className="h-[600px] glass-panel flex flex-col items-center justify-center animate-fade-in">
              <div className="w-16 h-16 border-4 border-blue-500/20 border-t-blue-500 rounded-full animate-spin mb-6"></div>
              <h2 className="text-xl font-bold text-white mb-2">LangGraph Orchestrator Running</h2>
              <p className="text-gray-400 animate-pulse">Extracting Facts & Citations...</p>
            </div>
          ) : !showDiff ? (
            <AdvancedWorkspace onRewrite={handleRewriteRequest} />
          ) : (
            <div className="space-y-4 animate-fade-in">
              <button 
                onClick={() => setShowDiff(false)}
                className="text-gray-400 hover:text-white flex items-center gap-2 text-sm transition-colors"
              >
                ← Back to Editor
              </button>
              <DiffViewer 
                originalText={originalText}
                humanizedText={humanizedText}
                qualityScore={99}
                facts={facts}
                citations={citations}
                onRegenerate={() => handleRewriteRequest(originalText)}
              />
            </div>
          )}
        </div>

      </div>

      {/* Profile Manager Modal */}
      {showProfileModal && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-[100] animate-fade-in p-4">
          <div className="glass-panel p-6 md:p-8 w-full max-w-md bg-[#050507]">
            <h2 className="text-xl font-bold text-white mb-4">Configure DNA Profile</h2>
            <p className="text-gray-400 text-sm mb-6">Train the AI on your personal writing style.</p>
            
            <div className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Profile Name</label>
                <input 
                  type="text" 
                  placeholder="e.g., Casual Twitter" 
                  className="w-full bg-gray-900 border border-gray-700 text-white rounded p-3"
                  value={modalInputName}
                  onChange={(e) => setModalInputName(e.target.value)}
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">System Prompt Instructions</label>
                <textarea 
                  rows={4} 
                  placeholder="e.g., Use emojis, keep it punchy, short sentences..." 
                  className="w-full bg-gray-900 border border-gray-700 text-white rounded p-3 resize-none"
                  value={modalInputInstr}
                  onChange={(e) => setModalInputInstr(e.target.value)}
                ></textarea>
              </div>
            </div>
            
            <div className="flex justify-end gap-3 mt-8">
              <button 
                onClick={() => setShowProfileModal(false)}
                className="px-4 py-2 rounded text-gray-400 hover:text-white transition-colors"
              >
                Cancel
              </button>
              <button 
                onClick={() => {
                  if (modalInputName && modalInputInstr) {
                    setActiveProfile("Custom Profile");
                    setProfileInstructions(modalInputInstr);
                  }
                  setShowProfileModal(false);
                }}
                className="px-6 py-2 rounded bg-blue-600 text-white font-medium hover:bg-blue-500 transition-colors"
              >
                Save Profile
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
