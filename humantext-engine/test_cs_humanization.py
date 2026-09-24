"""
Test humanization for Computer Science / Technical overview text flagged in Quillbot
"""
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import requests
from app.core.scrubber import AntiAIScrubber
from app.core.layers.orchestrator import HumanizerLayerOrchestrator

CS_AI_TEXT = """Computer Science is a crucial field that covers a lot, from how computers work to creating useful programs and apps. It's all about understanding technology and processing information. It's everywhere - education, medicine, business, and even entertainment. It helps solve big problems and makes things more efficient. In today's world, knowing about computers is super important. For students, it's a great field to study because it opens up many career paths like software dev, web dev, cybersecurity, data science, and AI. It's really all about making our tech world better."""

def test_cs():
    print("=" * 70)
    print("TESTING COMPUTER SCIENCE TEXT HUMANIZATION")
    print("=" * 70)
    print("\nORIGINAL TEXT:\n", CS_AI_TEXT)

    # 1. Test 7-Layer Engine
    res = HumanizerLayerOrchestrator.process(CS_AI_TEXT)
    print("\n7-LAYER HUMANIZED OUTPUT:\n", res["text"])
    print(f"\nHuman Score: {res['human_score']}% | AI Score: {res['ai_score']}%")
    print(f"Metrics: {res['metrics']}")
    print(f"Layers Applied: {res['layers_applied']}")

    # 2. Test AntiAIScrubber
    scrubbed = AntiAIScrubber.scrub(CS_AI_TEXT)
    print("\nSCRUBBER OUTPUT:\n", scrubbed)

    # 3. Test API /api/v1/humanize/v5
    print("\nTESTING LIVE API ENDPOINT...")
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/humanize/v5",
            json={"text": CS_AI_TEXT, "mode": "ghost"}
        )
        if response.status_code == 200:
            data = response.json()
            print("\nAPI RESPONSE SUCCESS:")
            print("Humanized Text:\n", data["humanized_text"])
            print("Quality Score:", data["quality_score"])
        else:
            print(f"API Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"API connection error: {e}")

if __name__ == "__main__":
    test_cs()
