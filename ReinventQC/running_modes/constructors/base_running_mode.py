from abc import abstractmethod, ABC


class BaseRunningMode(ABC):

    @abstractmethod
    def run(self):
        raise NotImplementedError("run method is not implemented")

class BaseMode:
    configuration_key:str = None
    registry:dict = None
    @classmethod
    def register(cls, config_key, constructor=None):
        if isinstance(config_key, str):
            if constructor is None:
                return lambda const, cls=cls, key=config_key: cls.register(key, const)
            else:
                cls.registry[config_key] = constructor
        else:
            constructor = config_key
            run_type = getattr(constructor, cls.configuration_key)
            cls.registry[run_type] = constructor
        return constructor
    @classmethod
    def get_default_constructor(cls, configuration):
        return cls.registry.get(getattr(configuration, cls.configuration_key))