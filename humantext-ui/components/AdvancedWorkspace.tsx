'use client';

import React, { useState } from 'react';

interface AdvancedWorkspaceProps {
  onRewrite: (text: string) => void;
}

export default function AdvancedWorkspace({ onRewrite }: AdvancedWorkspaceProps) {
  const [text, setText] = useState('');
  
  // Robust word count calculation
  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
  const isOverLimit = wordCount > 2500;
  const isDisabled = wordCount === 0 || isOverLimit;

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
        onInput={(e) => setText((e.target as HTMLTextAreaElement).value)}
      />
      
      <div className="mt-6 flex flex-col sm:flex-row justify-between items-center gap-4 border-t border-gray-800 pt-6">
        <div className={`text-sm w-full sm:w-auto text-center sm:text-left ${isOverLimit ? 'text-red-400' : 'text-gray-400'}`}>
          <span className={`font-mono ${isOverLimit ? 'text-red-500 font-bold' : 'text-white'}`}>{wordCount}</span> 
          <span className="font-mono"> / 2500</span> max words accepted.
        </div>
        <button 
          onClick={() => onRewrite(text)}
          disabled={isDisabled}
          className={`px-8 py-3 rounded-lg font-bold text-white transition-all w-full sm:w-auto ${
            isDisabled 
              ? 'bg-gray-700 opacity-50 cursor-not-allowed' 
              : 'bg-gradient-hover cursor-pointer shadow-lg hover:shadow-blue-500/20'
          }`}
        >
          {isOverLimit ? 'Word Limit Exceeded' : 'Analyze & Humanize'}
        </button>
      </div>
    </div>
  );
}
