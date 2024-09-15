from ReinventQC.running_modes.configurations.automated_curriculum_learning.base_configuration import BaseConfiguration
from ReinventQC.running_modes.configurations.automated_curriculum_learning.curriculum_strategy_configuration import \
    CurriculumStrategyConfiguration
from ReinventQC.running_modes.configurations.automated_curriculum_learning.production_strategy_configuration import \
    ProductionStrategyConfiguration


class AutomatedCLConfiguration(BaseConfiguration):
    prior: str
    agent: str
    curriculum_strategy: CurriculumStrategyConfiguration
    production_strategy: ProductionStrategyConfiguration