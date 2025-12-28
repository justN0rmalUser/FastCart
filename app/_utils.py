import json
from multiprocessing import Queue
from pathlib import Path
import logging as log


class JSONQueue:
    """Очередь, автоматически преобразующая словари в JSON и обратно."""
    def __init__(self):
        self.q = Queue()
    
    def put(self, data: dict):
        self.q.put(json.dumps(data))
    
    def get(self) -> dict:
        return json.loads(self.q.get())
    
    def close(self):
        self.q.close()


def open_config(fpath: str | Path) -> dict:
    fpath = Path(fpath)        
   
    with open(fpath, 'r', encoding="utf-8") as file:
        config = json.load(file)
    
    return config

def write_config(fpath: str | Path, config: dict):
    fpath = Path(fpath)        

    with open(fpath, 'w', encoding="utf-8") as file:
        json.dump(config, file)

def logger(*, name: str, fpath: Path | str):
    if not isinstance(fpath, Path):
        fpath = Path(fpath)

    try:
        abstract_logger = log.getLogger(name)
        abstract_logger.setLevel(log.DEBUG)

        abstract_logger_hand = log.FileHandler(filename=fpath, encoding='utf-8')
        abstract_logger_hand.setFormatter(log.Formatter('[%(asctime)s] %(levelname)s | %(message)s'))

        abstract_logger.addHandler(abstract_logger_hand)
    except Exception as exc:
        print(exc)
        raise
    else:
        return abstract_logger

def std(word: str) -> str:
    if isinstance(word, str):
        return word.upper().replace('-', '').replace(' ', '').replace('.', '').replace('/', '').replace(',', '').strip()
    