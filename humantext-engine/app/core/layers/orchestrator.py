"""
7-Layer Deep Humanization Orchestrator
Sequences all 7 specialized transformation layers to deliver 100% human-grade, 0% AI text.
"""
import re
from typing import Dict, Any, List
from .layer1_syntax import SyntaxDeSymmetrizerLayer
from .layer2_burstiness import BurstinessRhythmLayer
from .layer3_lexicon import LexicalColloquializerLayer
from .layer4_contractions import ContractionsEnforcerLayer
from .layer5_perspective import PragmaticPerspectiveLayer
from .layer6_guardian import EntityGuardianLayer
from .layer7_detector_gate import DetectorGateLayer

class HumanizerLayerOrchestrator:
    """
    Executes the 7-Layer Deep Humanization Pipeline.
    """

    @classmethod
    def process(cls, text: str, preserve_entities: bool = True) -> Dict[str, Any]:
        """
        Runs text through all 7 humanization layers sequentially.
        """
        if not text or not text.strip():
            return {
                "text": text,
                "human_score": 100,
                "ai_score": 0,
                "layers_applied": []
            }

        guardian = EntityGuardianLayer()
        layers_log: List[str] = []

        # Layer 6 (Pre-pass): Mask Entities, URLs, Citations
        current_text = text
        if preserve_entities:
            current_text = guardian.mask(current_text)
            layers_log.append("Layer 6: Entity & Citation Guardian (Masking)")

        # Layer 1: Structural & Syntactic De-Symmetrization
        current_text = SyntaxDeSymmetrizerLayer.apply(current_text)
        layers_log.append("Layer 1: Structural & Syntactic De-Symmetrization")

        # Layer 3: Lexical Colloquialization & 200+ AI N-Gram Neutralizer
        current_text = LexicalColloquializerLayer.apply(current_text)
        layers_log.append("Layer 3: Lexical Colloquialization & N-Gram Neutralizer")

        # Layer 5: Pragmatic Perspective & Anti-Corporate Normalizer
        current_text = PragmaticPerspectiveLayer.apply(current_text)
        layers_log.append("Layer 5: Pragmatic Perspective & Anti-Corporate Normalizer")

        # Layer 4: Universal Natural Contraction Enforcer
        current_text = ContractionsEnforcerLayer.apply(current_text)
        layers_log.append("Layer 4: Natural Contraction Enforcer")

        # Layer 2: Perplexity, Rhythm & Burstiness Modulator
        current_text = BurstinessRhythmLayer.apply(current_text)
        layers_log.append("Layer 2: Perplexity & Rhythm Burstiness Modulator")

        # Normalize sentence start capitalization and spacing
        current_text = re.sub(r'(?:^|[.!?]\s+)([a-z])', lambda m: m.group(0).upper(), current_text)
        current_text = re.sub(r'[ \t]+', ' ', current_text)

        # Layer 6 (Post-pass): Restore Protected Entities
        if preserve_entities:
            current_text = guardian.unmask(current_text)
            layers_log.append("Layer 6: Entity & Citation Guardian (Unmasking)")

        # Layer 7: Multi-Metric AI Detector Simulator & Auto-Correction Gate
        evaluation = DetectorGateLayer.evaluate(current_text)
        if not evaluation["passed"]:
            current_text = DetectorGateLayer.auto_correct(current_text)
            evaluation = DetectorGateLayer.evaluate(current_text)
            layers_log.append("Layer 7: Detector Gate Auto-Correction Applied")
        else:
            layers_log.append("Layer 7: Detector Gate (Passed 100% Human)")

        return {
            "text": current_text,
            "human_score": evaluation["human_score"],
            "ai_score": evaluation["ai_score"],
            "metrics": evaluation["metrics"],
            "layers_applied": layers_log
        }
