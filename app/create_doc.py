import fdb
from app.utils._utils import logger, open_config, std
from app.utils.sqls import document_registry, document_calculation, goods_calculation, find_shopnom_id, new_nom, directory_registry, nom_attribute, shop_price
from app.utils.fmt import fmt_code, fmt_firm


LOG = logger(name="Request", fpath="logs\\req.log")
ERRDATA = logger(name="Errors", fpath="logs\\corrupt_data.log")
cfg = open_config("app\\config.json")


def create_document(TITLE, DESCRIPTION, ITEMS):
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

    # Курсор
    try:
        LOG.debug("Создание курсора")
        cur = con.cursor()
    except Exception as exc:
        LOG.critical(f"Ошибка установки курсора: {exc}")
        con.close()
        raise
    else:
        LOG.info("Курсор установлен успешно")

    try:
        doc_reg = document_registry(cur)
        doc_calc = document_calculation(cur, title=TITLE, descript=DESCRIPTION, doc_reg_id=doc_reg)
        con.commit()
        print("Доки созданы")

        for n, item in enumerate(ITEMS, start=1):
            sid, count, price = item
            LOG.info(item)
            goods_calculation(cur, calc_id=doc_calc, sin_id=sid, count=count, price=price, pos=n)

        con.commit()
    except Exception as exc:
        LOG.error(exc)
        con.rollback()
        con.close()
        raise
    else:
        con.close()
        return doc_calc
