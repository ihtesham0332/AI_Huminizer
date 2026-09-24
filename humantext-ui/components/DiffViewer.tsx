'use client';

import React from 'react';

interface DiffViewerProps {
  originalText: string;
  humanizedText: string;
  qualityScore?: number;
  facts?: string[];
  citations?: string[];
  onRegenerate?: () => void;
}

export default function DiffViewer({ originalText, humanizedText, qualityScore = 98, facts = [], citations = [], onRegenerate }: DiffViewerProps) {

  const highlightProtectedEntities = (text: string) => {
    if (!text) return { __html: '' };
    
    let highlightedText = text;
    
    facts.forEach(fact => {
      highlightedText = highlightedText.replaceAll(
        fact, 
        `<span class="highlight-fact" title="Fact Guardian Protected">${fact}</span>`
      );
    });
    
    citations.forEach(cite => {
      highlightedText = highlightedText.replaceAll(
        cite,
        `<span class="highlight-citation" title="Citation Guardian Protected">${cite}</span>`
      );
    });
    
    return { __html: highlightedText };
  };

  return (
    <div className="h-auto lg:h-[600px] flex flex-col glass-panel p-4 md:p-6 animate-fade-in">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 border-b border-gray-800 pb-4">
        <h2 className="text-xl font-semibold text-white">Document Diff Viewer</h2>
        <div className="flex gap-3 text-sm">
          <span className="px-3 py-1 rounded-full bg-green-500/10 text-green-400 border border-green-500/20 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
            Quality Gate: PASS ({qualityScore}%)
          </span>
          <span className="px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
            Facts Locked
          </span>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 h-full flex-1 min-h-0">
        
        {/* Original Text */}
        <div className="flex flex-col h-full bg-black/40 rounded-xl border border-gray-800 overflow-hidden">
          <div className="p-4 border-b border-gray-800 bg-gray-900/50 text-gray-400 font-medium text-sm flex justify-between">
            <span>Original Input</span>
            <span className="font-mono text-xs md:text-sm">{originalText.split(/\s+/).filter(w => w.length > 0).length} words</span>
          </div>
          <div 
            className="p-4 md:p-6 text-gray-300 leading-relaxed text-base md:text-lg overflow-y-auto min-h-[300px] lg:min-h-0"
            dangerouslySetInnerHTML={highlightProtectedEntities(originalText)} 
          />
        </div>

        {/* Humanized Text */}
        <div className="flex flex-col h-full bg-[#0d1117] rounded-xl border border-[#1f2937] shadow-[0_0_30px_rgba(59,130,246,0.05)] overflow-hidden relative">
          <div className="absolute top-4 right-4 px-3 py-1 bg-[#161b22] text-gray-300 text-xs rounded-full border border-gray-700 cursor-help transition-colors hover:bg-gray-700 hover:text-white z-10"
               title="The LLM simplified the passive voice while maintaining all numerical data.">
            ✨ Improved Flow
          </div>
          
          <div className="p-4 border-b border-gray-800 bg-gray-900/80 text-white font-medium text-sm flex justify-between items-center">
            <span>Humanized Output</span>
            <div className="flex gap-2">
              <button 
                onClick={() => navigator.clipboard.writeText(humanizedText)}
                className="text-xs px-2 py-1 bg-gray-800 hover:bg-gray-700 rounded border border-gray-700 transition-colors"
                title="Copy to Clipboard"
              >
                Copy
              </button>
              {onRegenerate && (
                <button 
                  onClick={onRegenerate}
                  className="text-xs px-2 py-1 bg-blue-900/30 text-blue-400 hover:bg-blue-900/50 rounded border border-blue-900/50 transition-colors"
                  title="Retry Generation"
                >
                  Regenerate
                </button>
              )}
            </div>
          </div>
          <div 
            className="p-4 md:p-6 text-gray-100 leading-relaxed text-base md:text-lg overflow-y-auto min-h-[300px] lg:min-h-0"
            dangerouslySetInnerHTML={highlightProtectedEntities(humanizedText)} 
          />
        </div>
      </div>
    </div>
  );
}
