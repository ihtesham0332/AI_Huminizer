import httpx
import time

academic_sample = (
    "In 2024, artificial intelligence was utilized by 78.4% of Fortune 500 enterprises according to Smith et al. (2023). "
    "Moreover, it is crucial to understand that machine learning models delve into high-dimensional feature spaces to "
    "foster seamless decision-making [1, 2]. However, the cost of $4.2 million remains a pivotal challenge."
)

payload = {
    "text": academic_sample,
    "mode": "deep",
    "length": "maintain"
}

t0 = time.time()
print(f"Calling http://localhost:8000/api/v1/humanize/v5 with complex entities...")
with httpx.Client(timeout=120.0) as client:
    res = client.post("http://localhost:8000/api/v1/humanize/v5", json=payload)
    elapsed = time.time() - t0
    print(f"Status: {res.status_code} in {elapsed:.2f}s")
    if res.status_code == 200:
        data = res.json()
        print("\n--- HUMANIZED ACADEMIC OUTPUT ---")
        print(data.get("humanized_text"))
        print("---------------------------------\n")
        print(f"Facts protected: {data.get('facts_protected')}")
        print(f"Citations protected: {data.get('citations_protected')}")
        print(f"Quality score: {data.get('quality_score')}")
    else:
        print("Error:", res.text)
