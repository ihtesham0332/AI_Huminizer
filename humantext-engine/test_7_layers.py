"""
Comprehensive Test for 7-Layer Deep Humanization Engine
Tests individual layers and full pipeline execution against real AI detection triggers.
"""
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import requests
from app.core.layers.orchestrator import HumanizerLayerOrchestrator
from app.core.layers.layer1_syntax import SyntaxDeSymmetrizerLayer
from app.core.layers.layer2_burstiness import BurstinessRhythmLayer
from app.core.layers.layer3_lexicon import LexicalColloquializerLayer
from app.core.layers.layer4_contractions import ContractionsEnforcerLayer
from app.core.layers.layer5_perspective import PragmaticPerspectiveLayer
from app.core.layers.layer6_guardian import EntityGuardianLayer
from app.core.layers.layer7_detector_gate import DetectorGateLayer
from app.core.scrubber import AntiAIScrubber

AI_SAMPLE_1 = """Today, I had a great session with Sir Muhammad Akif on an important topic: Networking and Relationships. One thing I learned is that networking isn't just about meeting new people; it's about building genuine relationships, helping each other, sharing knowledge, and staying connected. Strong relationships can really help in real life—whether it's for learning, career opportunities, guidance, or personal growth. A strong network is built on trust, respect, and consistency. Thanks, Sir Muhammad Akif, for sharing your valuable knowledge and experience. #Networking #CareerGrowth"""

AI_SAMPLE_2 = """In today's fast-paced digital world, artificial intelligence plays a pivotal role in fostering innovation. Furthermore, it is imperative that organizations delve into cutting-edge machine learning solutions to unlock the potential of data. In conclusion, leveraging these robust tools is a testament to technological progress."""

def test_layers():
    print("=" * 70)
    print("TESTING 7-LAYER DEEP HUMANIZATION ENGINE")
    print("=" * 70)

    # 1. Test Layer by Layer
    print("\n[Layer 1: Syntax De-Symmetrization]")
    l1 = SyntaxDeSymmetrizerLayer.apply(AI_SAMPLE_1)
    print(f"Result:\n{l1}\n")

    print("\n[Layer 3: Lexical Colloquialization]")
    l3 = LexicalColloquializerLayer.apply(AI_SAMPLE_2)
    print(f"Result:\n{l3}\n")

    print("\n[Layer 4: Contractions Enforcement]")
    l4 = ContractionsEnforcerLayer.apply("It is important because they are not ready and cannot proceed.")
    print(f"Result:\n{l4}\n")

    print("\n[Layer 5: Pragmatic Perspective & Sanitization]")
    l5 = PragmaticPerspectiveLayer.apply(AI_SAMPLE_1)
    print(f"Result:\n{l5}\n")

    print("\n[Layer 6: Entity Guardian Masking & Restoration]")
    guardian = EntityGuardianLayer()
    text_with_entities = "Contact Dr. Jane at jane@univ.edu or visit https://ai.org. Growth rose by 24.5% on September 24, 2026."
    masked = guardian.mask(text_with_entities)
    print(f"Masked: {masked}")
    unmasked = guardian.unmask(masked)
    print(f"Unmasked: {unmasked}")
    assert unmasked == text_with_entities, "Entity unmasking must match exactly!"
    print("Entity Guardian: PASSED\n")

    # Full 7-Layer Pipeline Test
    print("\n[Full 7-Layer Pipeline Execution on Sample 1]")
    result1 = HumanizerLayerOrchestrator.process(AI_SAMPLE_1)
    print(f"Humanized Output:\n{result1['text']}")
    print(f"Human Score: {result1['human_score']}% | AI Score: {result1['ai_score']}%")
    print(f"Metrics: {result1['metrics']}")
    print(f"Layers Applied: {result1['layers_applied']}\n")

    print("\n[Full 7-Layer Pipeline Execution on Sample 2]")
    result2 = HumanizerLayerOrchestrator.process(AI_SAMPLE_2)
    print(f"Humanized Output:\n{result2['text']}")
    print(f"Human Score: {result2['human_score']}% | AI Score: {result2['ai_score']}%")
    print(f"Metrics: {result2['metrics']}")
    print(f"Layers Applied: {result2['layers_applied']}\n")

    # AntiAIScrubber Test
    print("\n[AntiAIScrubber Integration Test]")
    scrubbed = AntiAIScrubber.scrub(AI_SAMPLE_1)
    print(f"Scrubbed Output:\n{scrubbed}")
    eval_res = AntiAIScrubber.evaluate_human_score(scrubbed)
    print(f"Evaluation: {eval_res['human_score']}% Human, {eval_res['ai_score']}% AI\n")

    # API Test
    print("\n[E2E API Test -> http://localhost:8000/api/v1/humanize/v5]")
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/humanize/v5",
            json={"text": AI_SAMPLE_1, "mode": "ghost"}
        )
        if response.status_code == 200:
            data = response.json()
            print("API Response SUCCESS:")
            print(f"Humanized Text:\n{data['humanized_text']}")
            print(f"Quality Score: {data['quality_score']}")
            print(f"Protected Facts: {data['facts_protected']}")
        else:
            print(f"API Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"API Connection notice: {e}")

if __name__ == "__main__":
    test_layers()
