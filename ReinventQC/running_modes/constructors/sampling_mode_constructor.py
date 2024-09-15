from dacite import from_dict

from ReinventQC.running_modes.constructors.base_running_mode import BaseRunningMode
from ReinventQC.running_modes.configurations import GeneralConfigurationEnvelope, SampleFromModelConfiguration
from ReinventQC.running_modes.sampling.sample_from_model import SampleFromModelRunner
from ReinventQC.running_modes.utils.general import set_default_device_cuda


class SamplingModeConstructor:
    def __new__(self, configuration: GeneralConfigurationEnvelope) -> BaseRunningMode:
        self._configuration = configuration
        config = from_dict(data_class=SampleFromModelConfiguration, data=self._configuration.parameters)
        set_default_device_cuda()
        runner = SampleFromModelRunner(self._configuration, config)
        return runner