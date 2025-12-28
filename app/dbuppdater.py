from _utils import logger, open_config
import fdb


cfg = open_config("app\config.json")

LOG = logger(name="Request", fpath="logs\\req.log")
ERRDATA = logger(name="Errors", fpath="logs\\corrupt_data.log")


def main():
    # Подключение к базе данных
    try:
        LOG.debug("Подключение к базе данных")
        con = fdb.connect(dsn=      cfg["Database"]["db_path"],
                          user=     cfg["Database"]["db_user"], 
                          password= cfg["Database"]["db_password"])
    except Exception as e:
        LOG.critical(f"Ошибка подключения к базе: {e}")
        raise
    else:
        LOG.info("База данных подключена успешно")

    # Курсор
    try:
        LOG.debug("Создание курсора")
        cur = con.cursor()
    except Exception as e:
        LOG.critical(f"Ошибка установки курсора: {e}")
        raise
    else:
        LOG.info("Курсор установлен успешно")
    
    