'use client';

import React, { useState } from 'react';

interface AdvancedWorkspaceProps {
  onRewrite: (text: string) => void;
}

export default function AdvancedWorkspace({ onRewrite }: AdvancedWorkspaceProps) {
  const [text, setText] = useState('');
  
  return (
    <div className="glass-panel p-6 animate-fade-in">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-white">Input Document</h2>
        <span className="text-xs font-mono bg-blue-500/10 text-blue-400 px-3 py-1 rounded-full border border-blue-500/20">
          Ready for Analysis
        </span>
      </div>
      
      <textarea
        className="w-full h-[300px] md:h-[400px] bg-black/40 border border-gray-800 rounded-lg p-4 md:p-6 text-gray-200 text-base md:text-lg leading-relaxed focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 resize-none"
        placeholder="Paste your report, essay, or email here. Our Fact & Citation Guardians will automatically lock your data before humanizing..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      
      <div className="mt-6 flex flex-col sm:flex-row justify-between items-center gap-4 border-t border-gray-800 pt-6">
        <div className="text-gray-400 text-sm w-full sm:w-auto text-center sm:text-left">
          <span className="font-mono text-white">{text.split(/\s+/).filter(w => w.length > 0).length}</span> 
          <span className="font-mono"> / 2500</span> max words accepted.
        </div>
        <button 
          onClick={() => onRewrite(text)}
          disabled={!text}
          className="bg-gradient-hover px-8 py-3 rounded-lg font-bold text-white disabled:opacity-50 disabled:cursor-not-allowed w-full sm:w-auto"
        >
          Analyze & Humanize
        </button>
      </div>
    </div>
  );
}
