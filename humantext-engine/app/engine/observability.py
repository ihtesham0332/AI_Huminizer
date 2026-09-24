import time
from typing import Dict, Any

class ObservabilityEngine:
    """
    Tracks system latency, API costs, model usage, and quality failures.
    Adheres to Master Prompt Sections 51, 52, 53, and 54.
    """
    def __init__(self):
        # In a real system, these would push to Redis Streams, Prometheus, or the DB.
        self.metrics_store = []
        
    def start_timer(self) -> float:
        return time.time()
        
    def end_timer(self, start_time: float) -> float:
        return round((time.time() - start_time) * 1000, 2) # Latency in ms
        
    def log_job_metrics(self, 
                        job_id: str, 
                        model_used: str, 
                        tokens: int, 
                        api_cost: float, 
                        latency_ms: float, 
                        quality_failures: int,
                        cache_hit: bool):
        """
        Logs a single job's telemetry data to the central datastore.
        """
        record = {
            "job_id": job_id,
            "model_used": model_used,
            "tokens": tokens,
            "api_cost": api_cost,
            "latency_ms": latency_ms,
            "quality_failures": quality_failures,
            "cache_hit": cache_hit,
            "timestamp": time.time()
        }
        self.metrics_store.append(record)
        return record
        
    def generate_admin_report(self) -> Dict[str, Any]:
        """
        Aggregates metrics for the React Admin Dashboard.
        """
        if not self.metrics_store:
            return {"status": "No data available."}
            
        total_jobs = len(self.metrics_store)
        total_cost = sum(r["api_cost"] for r in self.metrics_store)
        total_tokens = sum(r["tokens"] for r in self.metrics_store)
        total_failures = sum(r["quality_failures"] for r in self.metrics_store)
        
        # Calculate Latencies
        latencies = sorted([r["latency_ms"] for r in self.metrics_store])
        p50 = latencies[len(latencies)//2] if latencies else 0
        p95 = latencies[int(len(latencies) * 0.95)] if len(latencies) >= 20 else latencies[-1]
        
        cache_hits = sum(1 for r in self.metrics_store if r["cache_hit"])
        cache_savings_pct = (cache_hits / total_jobs) * 100 if total_jobs > 0 else 0
        
        return {
            "cost_dashboard": {
                "total_api_cost_usd": round(total_cost, 4),
                "avg_cost_per_job": round(total_cost / total_jobs, 4),
                "total_tokens": total_tokens,
                "cache_savings_pct": round(cache_savings_pct, 1)
            },
            "performance_dashboard": {
                "p50_latency_ms": p50,
                "p95_latency_ms": p95
            },
            "quality_dashboard": {
                "total_quality_failures": total_failures,
                "semantic_failure_rate_pct": round((total_failures / total_jobs) * 100, 1)
            }
        }
