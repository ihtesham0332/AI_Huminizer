"""
7-Layer Deep Humanization Engine
Provides impenetrable multi-pass text transformation to eliminate 100% of AI detection signals.
"""

from .layer1_syntax import SyntaxDeSymmetrizerLayer
from .layer2_burstiness import BurstinessRhythmLayer
from .layer3_lexicon import LexicalColloquializerLayer
from .layer4_contractions import ContractionsEnforcerLayer
from .layer5_perspective import PragmaticPerspectiveLayer
from .layer6_guardian import EntityGuardianLayer
from .layer7_detector_gate import DetectorGateLayer
from .orchestrator import HumanizerLayerOrchestrator

__all__ = [
    "SyntaxDeSymmetrizerLayer",
    "BurstinessRhythmLayer",
    "LexicalColloquializerLayer",
    "ContractionsEnforcerLayer",
    "PragmaticPerspectiveLayer",
    "EntityGuardianLayer",
    "DetectorGateLayer",
    "HumanizerLayerOrchestrator",
]
