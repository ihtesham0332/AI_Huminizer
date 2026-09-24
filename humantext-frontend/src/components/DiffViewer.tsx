import React from 'react';

interface DiffViewerProps {
  original: string;
  humanized: string;
  facts: string[];
  citations: string[];
}

export default function DiffViewer({ original, humanized, facts, citations }: DiffViewerProps) {
  
  // A very basic highlight function for MVP demonstration
  // In production, this would use a robust diffing library like 'diff' or 'react-diff-viewer'
  const highlightProtectedEntities = (text: string) => {
    let highlightedText = text;
    
    facts.forEach(fact => {
      highlightedText = highlightedText.replace(
        fact, 
        `<span class="bg-blue-500/20 text-blue-300 px-1 rounded font-mono text-sm border border-blue-500/30" title="Protected Fact">${fact}</span>`
      );
    });
    
    citations.forEach(cite => {
      highlightedText = highlightedText.replace(
        cite,
        `<span class="bg-purple-500/20 text-purple-300 px-1 rounded font-mono text-sm border border-purple-500/30" title="Protected Citation">${cite}</span>`
      );
    });
    
    return { __html: highlightedText };
  };

  return (
    <div className="grid grid-cols-2 gap-6 h-full">
      {/* Original Side */}
      <div className="flex flex-col bg-black/40 rounded-lg border border-gray-800">
        <div className="p-3 border-b border-gray-800 text-sm text-gray-400 font-medium bg-gray-900/50 rounded-t-lg">
          Original Input
        </div>
        <div className="p-6 text-gray-300 leading-relaxed text-lg" 
             dangerouslySetInnerHTML={highlightProtectedEntities(original)} />
      </div>

      {/* Humanized Side */}
      <div className="flex flex-col bg-black/40 rounded-lg border border-gray-800 shadow-[0_0_15px_rgba(59,130,246,0.05)] relative">
        {/* Explainability Tag */}
        <div className="absolute top-3 right-4 px-3 py-1 bg-gray-800 text-gray-300 text-xs rounded-full border border-gray-700 cursor-help transition-colors hover:bg-gray-700 hover:text-white"
             title="The LLM simplified the passive voice while maintaining all numerical data.">
          ✨ Improved Flow
        </div>
        
        <div className="p-3 border-b border-gray-800 text-sm font-medium bg-gray-900/50 rounded-t-lg text-white">
          Humanized Output
        </div>
        <div className="p-6 text-gray-200 leading-relaxed text-lg"
             dangerouslySetInnerHTML={highlightProtectedEntities(humanized)} />
      </div>
    </div>
  );
}
