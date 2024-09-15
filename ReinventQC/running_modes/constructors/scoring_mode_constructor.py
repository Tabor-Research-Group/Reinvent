from dacite import from_dict
from ReinventQC.reinvent_scoring.scoring import ScoringFunctionFactory

from ReinventQC.running_modes.constructors.base_running_mode import BaseRunningMode
from ReinventQC.running_modes.configurations import GeneralConfigurationEnvelope, ScoringRunnerComponents
from ReinventQC.running_modes.scoring.scoring_runner import ScoringRunner


class ScoringModeConstructor:
    def __new__(self, configuration: GeneralConfigurationEnvelope) -> BaseRunningMode:
        self._configuration = configuration
        config = from_dict(data_class=ScoringRunnerComponents, data=self._configuration.parameters)
        scoring_function = ScoringFunctionFactory(config.scoring_function)
        runner = ScoringRunner(configuration=self._configuration,
                               config=config.scoring,
                               scoring_function=scoring_function)
        return runner