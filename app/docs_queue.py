import fdb
from app._utils import logger, open_config
from app.sqls import document_registry, document_calculation, goods_calculation


LOG = logger(name="Request", fpath="logs\\req.log")
ERRDATA = logger(name="Errors", fpath="logs\\corrupt_data.log")
cfg = open_config("app\config.json")


def aggregate(jsonData):
    pass


def create_connect():
    # Подключение к базе данных
    try:
        LOG.debug("Подключение к базе данных")
        con = fdb.connect(  dsn=      cfg["Database"]["db_path"],
                            user=     cfg["Database"]["db_user"], 
                            password= cfg["Database"]["db_password"])
    except Exception as e:
        LOG.critical(f"Ошибка подключения к базе: {e}")
        raise
    else:
        LOG.info("База данных подключена успешно")
        return con
    
def create_cursor(connection):
    # Курсор
    try:
        LOG.debug("Создание курсора")
        cur = connection.cursor()
    except Exception as e:
        LOG.critical(f"Ошибка установки курсора: {e}")
        raise
    else:
        LOG.info("Курсор установлен успешно")
        return cur


def create_doc(response):
    try:
        con = create_connect()
        cur = create_cursor(con)
        assert con and cur, "Ошибка открытия базы данных"
    except Exception as exc:
        LOG.error(exc)
        return None
    else:
        aggregate(response)