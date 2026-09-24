import sys
import json
import traceback
from typing import Dict, Any

from app.engine.document_intelligence import DocumentIntelligenceEngine
from app.engine.style_intelligence import StyleIntelligenceEngine

class MCPServer:
    """
    A lightweight Model Context Protocol (MCP) server that exposes the 
    HumanText V4 intelligence engines over stdio using JSON-RPC 2.0.
    Adheres to Master Prompt Section 48.
    """
    def __init__(self):
        self.doc_engine = DocumentIntelligenceEngine()
        self.style_engine = StyleIntelligenceEngine()

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        try:
            method = request.get("method")
            params = request.get("params", {})
            
            if method == "analyze_document":
                text = params.get("text", "")
                result = self.doc_engine.parse_plain_text(text)
                return {"result": result}
                
            elif method == "analyze_style":
                text = params.get("text", "")
                result = self.style_engine.analyze_style_metrics(text)
                return {"result": result}
                
            elif method == "humanize_text":
                text = params.get("text", "")
                # Simulate a basic V4 generation for the MCP tool
                humanized = text + " [Humanized by HumanText MCP Server]"
                return {"result": {"original": text, "humanized": humanized}}
                
            else:
                return {"error": {"code": -32601, "message": f"Method {method} not found"}}
                
        except Exception as e:
            return {"error": {"code": -32000, "message": str(e), "data": traceback.format_exc()}}

    def start(self):
        """Listen for JSON-RPC messages on stdin and write responses to stdout."""
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
                
            try:
                request = json.loads(line)
                response = self.handle_request(request)
                
                # Attach JSON-RPC 2.0 wrapper
                response["jsonrpc"] = "2.0"
                if "id" in request:
                    response["id"] = request["id"]
                    
                print(json.dumps(response), flush=True)
                
            except json.JSONDecodeError:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {"code": -32700, "message": "Parse error"}
                }
                print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    server = MCPServer()
    server.start()
