"""
A helper class for configuring REINVENT runs
"""

import re, json, os

__all__ = [
    'ConfigurationHandler',
    'run'
]

class ConfigurationHandler:
    CONFIGURATION_PATHS = [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs')]
    CONFIGURATION_PATHS_ENV = "REINVENTQC_CONFIG_PATH"
    @classmethod
    def get_configuration_paths(cls):
        return list(cls.CONFIGURATION_PATHS) + os.environ.get(cls.CONFIGURATION_PATHS_ENV, '').split(":")

    @classmethod
    def load_config(self, path):
        # directly from REINVENT
        with open(path) as f:
            json_input = f.read().replace('\r', '').replace('\n', '')
        try:
            return json.loads(json_input)
        except (ValueError, KeyError, TypeError) as e:
            print(f"JSON format error in file ${path}: \n ${e}")

    @classmethod
    def load_default_configs(cls):
        opts = {}
        for dir in reversed(cls.get_configuration_paths()):
            cfg = os.path.join(dir, "config.json")
            if os.path.isfile(cfg):
                opts.update(cls.load_config(cfg))
        return opts
    @classmethod
    def update_config_overrides(cls, config, overrides):
        config = config.copy() # shallow copy for safetyp
        for k,v in overrides.items():
            if k not in config or not isinstance(v, dict):
                config[k] = v
            else:
                cls.update_config_overrides(config[k], v)
        return config
    @classmethod
    def load(cls, config:'dict|str', **overrides):
        if isinstance(config, str):
            config = cls.load_config(config)
        config = cls.update_config_overrides(config, overrides)
        return config

    @classmethod
    def apply_templates(cls, config:dict, template_vars:dict, template_re=None):
        config = config.copy()
        if template_re is None:
            template_patterns = [
                ["{" + k + "}", "{" + k + ":"]
                for k in template_vars.keys()
            ]
            template_re = re.compile("|".join(k for p in template_patterns for k in p))
        elif isinstance(template_re, str):
            template_re = re.compile(template_re)
        for k,v in config.items():
            if isinstance(v, str) and template_re.match(v):
                v = v.format_map(template_vars)
                config[k] = v
            elif isinstance(v, dict):
                config[k] = cls.apply_templates(v, template_vars, template_re=template_re)
        return config

def run(config, output_dir=None, templates=None, **overrides):
    from .running_modes.manager import Manager

    base_config = ConfigurationHandler.load_default_configs() # default log settings
    config = ConfigurationHandler.load(config, **overrides)

    if templates is not None:
        config = ConfigurationHandler.apply_templates(config, templates)
        base_config = ConfigurationHandler.apply_templates(base_config, templates)

    log_data = dict(
        base_config.get("logging", {}),
        **config.get("logging", {})
    )
    result_folder = log_data.get('result_folder')
    if result_folder is None:
        result_folder = os.path.join(os.getcwd(), 'results')
        log_data['result_folder'] = result_folder
    os.makedirs(result_folder, exist_ok=True)

    manager = Manager(base_config, config)
    manager.run()