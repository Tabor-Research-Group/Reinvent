from dataclasses import dataclass

from ReinventQC.reinvent_scoring import ScoringFunctionParameters


@dataclass
class ScoringStrategyConfiguration:
    scoring_function: ScoringFunctionParameters
    name: str