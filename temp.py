import fdb
from app._utils import logger, open_config, std
from app.sqls import document_registry, document_calculation, goods_calculation, find_shopnom_id, new_nom, directory_registry, nom_attribute
from app.fmt import fmt_code, fmt_firm


LOG = logger(name="Request", fpath="logs\\req.log")
ERRDATA = logger(name="Errors", fpath="logs\\corrupt_data.log")
cfg = open_config("app\\config.json")


def get_sid(cur, con, item):
    name, firm, code, count, price, firm_name = item
    name = name[:29]
    sid = find_shopnom_id(cur, firm=firm, code=code)
    if sid:
        LOG.info(f"Здесь есть SID: {sid}")
        return (sid, count, price)
    else:
        dir_reg = directory_registry(cur)
        LOG.info(dir_reg)
        nom_attribute(cur, dir_reg=dir_reg)
        nom = new_nom(cur, dir_reg=dir_reg, name=name, code=code, firm_id=firm, cost=price, margin=65, firm_value=firm_name)
        
        con.commit()
        return (nom, count, price)
    

def filter(material) -> dict:
    result = {
        "title": material['name'],
        "description": material['description']
    }
    itemlist = []
    for item in material["products"]:
        itemlist.append((
                str(item["partName"]).replace('*', '').replace('$', '').strip(),
                fmt_firm.get(std(item["brand"]), ''),
                fmt_code.get(std(item["code"]), item["code"]), 
                float(item["count"].replace(' ', '').replace('\xa0', '')), 
                float(item["price"].replace(' ', '').replace('\xa0', '')),
                item["brand"]
            ))
        
    result['productList'] = itemlist
    return result

def aggregate(cursor, connect, information):
    result = []
    for item in information['productList']:
        fullCell = get_sid(cursor, connect, item)
        if fullCell:
            result.append(fullCell)
        else:
            name, firm, code, count, price, firm_name = item
            LOG.warning(f"<{firm, code}> не добавлен, sid не найден!")
    return tuple(result)


def start_db_cycle(response):
    try:
        LOG.debug("Подключение к базе данных")
        con = fdb.connect(  dsn=      cfg["Database"]["db_path"],
                            user=     cfg["Database"]["db_user"], 
                            password= cfg["Database"]["db_password"])
    except Exception as e:
        LOG.critical(f"Ошибка подключения к базе: {e}")
        return False, None
    else:
        LOG.info("База данных подключена успешно")

    # Курсор
    try:
        LOG.debug("Создание курсора")
        cur = con.cursor()
    except Exception as exc:
        LOG.critical(f"Ошибка установки курсора: {exc}")
        con.close()
        return False, None
    else:
        LOG.info("Курсор установлен успешно")

    try:
        information = filter(response)
    except Exception as exc:
        LOG.critical(f"Ошибка фильтрации: {exc}")
        con.close()
        return False, None
    else:
        LOG.debug("Фильтрация массива данных успешна!")
        
    try:
        data = {
            "title": information['title'],
            "description": information['description']
        }
        data['productList'] = aggregate(cur, con, information)
        assert data['productList'], "Поиск отбросил все данные"
    except Exception as exc:
        LOG.critical(f"Ошибка фильтрации: {exc}")
        con.close()
        return False, None
    else:
        LOG.debug("Поиск и агрегация прошли успешно!")

    try:
        doc_reg = document_registry(cur)
        doc_calc = document_calculation(cur, title=data["title"], doc_reg_id=doc_reg)
        con.commit()

        for n, item in enumerate(data['productList'], start=1):
            sid, count, price = item
            LOG.info(item)
            goods_calculation(cur, calc_id=doc_calc, sin_id=sid, count=count, price=price, pos=n)
            con.commit()

        con.commit()
    except Exception as exc:
        LOG.error(exc)
        print("problems...")
        return False, None

    con.close()
    
    return True, response['name']


input_data = {
    'description': '',
    'name': 'документ',
    'products':
        [
            {
                'brand': 'Riginal',
                'code': 'RG212141006001',
                'count': '1',
                'id': 'Riginal|RG212141006001|1|7551.39',
                'partName': 'Комплект ГРМ ВАЗ-21214,2123 (цепь., звезд., '
                        'натяж., успок., башмак )',
                'price': '7551.39'
            },
            {
                'brand': 'VAG',
                'code': '03L198119D',
                'count': '1',
                'id': 'VAG|03L198119D|1|46818.45',
                'partName': 'Комплект ремня ГРМ',
                'price': '46818.45'
            },
            {
                'brand': 'Victor Reinz',
                'code': '81-40538-00',
                'count': '2',
                'id': 'Victor Reinz|81-40538-00|2|1482.00',
                'partName': 'Сальник распределительного вала',
                'price': '1482.00'
            }
        ]
    }

start_db_cycle(input_data)