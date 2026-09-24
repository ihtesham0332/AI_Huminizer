import httpx
import time
import json

sample_ai_text = (
    "Today, I had a great session with Sir Muhammad Akif on an important topic: Networking and Relationships. "
    "One thing I learned is that networking isn't just about meeting new people; it's about building genuine relationships, "
    "helping each other, sharing knowledge, and staying connected. Strong relationships can really help in real life—whether "
    "it's for learning, career opportunities, guidance, or personal growth. A strong network is built on trust, respect, and consistency. "
    "Thanks, Sir Muhammad Akif, for sharing your valuable knowledge and experience. #Networking #Growth #ProfessionalDevelopment"
)

payload = {
    "text": sample_ai_text,
    "mode": "ghost",
    "length": "maintain"
}

t0 = time.time()
print(f"Calling http://localhost:8000/api/v1/humanize/v5 with mode={payload['mode']}...")
try:
    with httpx.Client(timeout=120.0) as client:
        res = client.post("http://localhost:8000/api/v1/humanize/v5", json=payload)
        elapsed = time.time() - t0
        print(f"Status: {res.status_code} in {elapsed:.2f}s")
        if res.status_code == 200:
            data = res.json()
            print("\n--- HUMANIZED TEXT OUTPUT ---")
            print(data.get("humanized_text"))
            print("-----------------------------\n")
            print(f"Facts protected: {data.get('facts_protected')}")
            print(f"Citations protected: {data.get('citations_protected')}")
            print(f"Quality score: {data.get('quality_score')}")
        else:
            print("Error response:", res.text)
except Exception as e:
    print(f"Exception: {e}")
