import yaml

from app._utils import open_config, write_config


cfg = open_config("config.yaml")

print(cfg['users']['other_pc'])
