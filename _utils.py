import yaml
from pathlib import Path


def open_config(fpath: str | Path) -> dict:
    fpath = Path(fpath)        
   
    with open(fpath, 'r', encoding="utf-8") as file:
        config = yaml.safe_load(file)
    
    return config

def write_config(fpath: str | Path, config: dict):
    fpath = Path(fpath)        

    with open(fpath, 'w', encoding="utf-8") as file:
        yaml.dump(config, file)
