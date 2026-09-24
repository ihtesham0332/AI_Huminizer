import React from 'react';
import DiffViewer from '../components/DiffViewer';

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white p-8 font-sans">
      
      {/* Header */}
      <header className="flex justify-between items-center mb-12 border-b border-gray-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            HumanText Agentic Platform
          </h1>
          <p className="text-gray-400 mt-2">Zero Meaning Drift. 100% Fact Preservation.</p>
        </div>
        
        {/* Wallet UI */}
        <div className="flex gap-4">
          <div className="bg-gray-900 px-4 py-2 rounded-lg border border-gray-800">
            <span className="text-sm text-gray-400">Words</span>
            <div className="font-mono font-bold text-blue-400">142,500</div>
          </div>
          <div className="bg-gray-900 px-4 py-2 rounded-lg border border-gray-800">
            <span className="text-sm text-gray-400">Credits</span>
            <div className="font-mono font-bold text-purple-400">850</div>
          </div>
        </div>
      </header>

      {/* Main Workspace */}
      <div className="grid grid-cols-12 gap-8">
        
        {/* Sidebar Controls */}
        <div className="col-span-3 space-y-6">
          <div className="bg-gray-900 p-6 rounded-xl border border-gray-800 shadow-2xl">
            <h3 className="text-lg font-semibold mb-4 text-gray-200">Processing Mode</h3>
            
            <div className="space-y-3">
              <label className="flex items-center gap-3 p-3 rounded-lg border border-blue-500/30 bg-blue-500/10 cursor-pointer">
                <input type="radio" name="mode" className="text-blue-500 bg-gray-800 border-gray-700" defaultChecked />
                <div>
                  <div className="font-medium">Balanced (Tier 2)</div>
                  <div className="text-xs text-gray-400 mt-1">GPT-4o-mini • 1 Credit</div>
                </div>
              </label>

              <label className="flex items-center gap-3 p-3 rounded-lg border border-gray-700 hover:border-gray-600 cursor-pointer">
                <input type="radio" name="mode" className="text-purple-500 bg-gray-800 border-gray-700" />
                <div>
                  <div className="font-medium text-purple-400">Deep / Academic (Tier 3)</div>
                  <div className="text-xs text-gray-400 mt-1">Gemini 3.1 Pro • 3 Credits</div>
                </div>
              </label>
            </div>
          </div>

          <div className="bg-gray-900 p-6 rounded-xl border border-gray-800">
            <h3 className="text-lg font-semibold mb-4 text-gray-200">Writing DNA Profile</h3>
            <select className="w-full bg-gray-800 border border-gray-700 text-white rounded-lg p-3 outline-none focus:border-blue-500">
              <option>Default Profile</option>
              <option>Academic Thesis (Strict)</option>
              <option>LinkedIn Marketing (Casual)</option>
            </select>
          </div>
          
          <button className="w-full py-4 rounded-xl font-bold text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 shadow-lg shadow-purple-500/20 transition-all transform hover:scale-[1.02]">
            Humanize Document
          </button>
        </div>

        {/* Diff Viewer Area */}
        <div className="col-span-9 bg-gray-900 rounded-xl border border-gray-800 p-6 flex flex-col h-[700px]">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Document Workspace</h2>
            <div className="flex gap-2 text-sm">
              <span className="px-3 py-1 rounded-full bg-green-500/10 text-green-400 border border-green-500/20">Fact Guardian Active</span>
              <span className="px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">Quality Critic: PASS</span>
            </div>
          </div>
          
          <div className="flex-1 overflow-y-auto pr-2">
             <DiffViewer 
               original="The revenue decreased by 15% in Q3 2026. Furthermore, Smith (2024) noted a similar trend."
               humanized="In the third quarter of 2026, revenue fell by 15%. A similar pattern was observed by Smith (2024)."
               facts={["15%", "Q3", "2026"]}
               citations={["Smith (2024)"]}
             />
          </div>
        </div>

      </div>
    </div>
  );
}
