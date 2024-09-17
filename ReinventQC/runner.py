"""
A helper class for configuring REINVENT runs
"""

import re, json, os

__all__ = [
    'ConfigurationHandler',
    'run_job'
]

class ConfigurationHandler:
    CONFIGURATION_PATHS = []
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
    def load(cls, config:'dict|str', **overrides):
        if isinstance(config, str):
            config = cls.load_config(config)
        config.update(overrides)
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

def run(config, templates=None, **overrides):
    from .running_modes.manager import Manager

    config = ConfigurationHandler.load(config, **overrides)
    base_config = ConfigurationHandler.load_default_configs()

    if templates is not None:
        config = ConfigurationHandler.apply_templates(config, templates)
        base_config = ConfigurationHandler.apply_templates(base_config, templates)

    log_data = dict(
        base_config.get("logging", {}),
        **config.get("logging", {})
    )



    configuration["logging"] = {
        "sender": "http://0.0.0.1",  # only relevant if "recipient" is set to "remote"
        "recipient": "local",  # either to local logging or use a remote REST-interface
        "logging_frequency": 10,  # log every x-th steps
        "logging_path": os.path.join(output_dir, "progress.log"),  # load this folder in tensorboard
        "result_folder": os.path.join(output_dir, "results"),  # will hold the compounds (SMILES) and summaries
        "job_name": "Reinforcement learning demo",  # set an arbitrary job name for identification
        "job_id": "demo"  # only relevant if "recipient" is set to a specific REST endpoint
    }

    result_folder = base_config.load

    base_dir = os.path.dirname(self.config.log_data.opts['result_folder'])
    os.makedirs(base_dir, exist_ok=True)

    manager = Manager(base_config, config)
    manager.run()


def run_job(**config):
    Runner.from_parameters(**config).run_job()

