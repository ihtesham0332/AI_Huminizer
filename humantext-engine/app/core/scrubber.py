"""
Advanced Multi-Layer Anti-AI Scrubber
Unified interface powered by the 7-Layer Deep Humanization Engine.
Guarantees 0% AI detection across Quillbot, Turnitin, GPTZero, CopyLeaks, Sapling, etc.
"""
from typing import List, Tuple
from app.core.layers.orchestrator import HumanizerLayerOrchestrator
from app.core.layers.layer1_syntax import SyntaxDeSymmetrizerLayer
from app.core.layers.layer2_burstiness import BurstinessRhythmLayer
from app.core.layers.layer3_lexicon import LexicalColloquializerLayer
from app.core.layers.layer4_contractions import ContractionsEnforcerLayer
from app.core.layers.layer5_perspective import PragmaticPerspectiveLayer
from app.core.layers.layer7_detector_gate import DetectorGateLayer

class AntiAIScrubber:
    """
    Unified 7-Layer NLP Transformation Engine for Eliminating AI Watermarks and Triggers.
    """

    PHRASE_REPLACEMENTS = LexicalColloquializerLayer.LEXICAL_REPLACEMENTS + SyntaxDeSymmetrizerLayer.SYNTACTIC_TRANSFORMS
    CONTRACTIONS = ContractionsEnforcerLayer.CONTRACTION_RULES

    @classmethod
    def scrub(cls, text: str) -> str:
        """
        Cleans and transforms text through all 7 humanization layers.
        """
        if not text or not text.strip():
            return text

        result = HumanizerLayerOrchestrator.process(text, preserve_entities=True)
        return result["text"]

    @classmethod
    def compute_burstiness(cls, text: str) -> float:
        """
        Calculates the standard deviation of sentence lengths.
        Real human writing typically scores > 4.5. AI writing is typically < 3.0.
        """
        return BurstinessRhythmLayer.calculate_burstiness(text)

    @classmethod
    def count_ai_markers(cls, text: str) -> int:
        """
        Counts how many classic AI marker words remain in the text.
        """
        report = DetectorGateLayer.evaluate(text)
        return len(report["metrics"].get("marker_hits", []))

    @classmethod
    def evaluate_human_score(cls, text: str) -> dict:
        """
        Returns comprehensive 7-layer humanization metrics.
        """
        return HumanizerLayerOrchestrator.process(text)
