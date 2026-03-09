import fdb
from app.utils._utils import logger, open_config, std, store_attribute, five_round
from app.utils.sqls import (
    find_shopnom_id, 
    new_nom, 
    directory_registry, 
    nom_attribute, 
    shop_price
)
from app.utils.fmt import fmt_code, fmt_firm


ItemLOG = logger(name="Check", fpath="logs\\item.log")
ERRDATA = logger(name="Errors", fpath="logs\\corrupt_data.log")
cfg = open_config("app\\config.json")


def get_items(items_list, *, cur):
    products = []
    not_stated_products = []
    for item in items_list:
        name = item["partName"].replace('*', '').replace('$', '').strip()[:29]
        
        firm = item["brand"]
        seek_firm = fmt_firm.get(std(firm))
        code = item["code"]
        seek_code = fmt_code.get(std(code))
        
        count = float(item["count"].replace(' ', '').replace('\xa0', ''))
        price = five_round(float(item["price"].replace(' ', '').replace('\xa0', '')))
        
        match str(int(bool(seek_firm)))+str(int(bool(seek_code))):
            case "11":
                snid = find_shopnom_id(cur, firm=seek_firm, code=seek_code)
                if snid:
                    products.append((snid, count, price))
                else:
                    snid = find_shopnom_id(cur, firm=seek_firm, code=code)
                    if snid:
                        products.append((snid, count, price))
                    else:
                        not_stated_products.append(
                            {
                                "name": name, 
                                "firm": firm,
                                "firm_id": seek_firm, 
                                "code": code,
                                "default_price": price
                            }
                        )
            case "10":
                snid = find_shopnom_id(cur, firm=seek_firm, code=code)
                if snid:
                    products.append((snid, count, price))
                else:
                    not_stated_products.append(
                        {
                            "name": name, 
                            "firm": firm,
                            "firm_id": seek_firm, 
                            "code": code,
                            "default_price": price
                        }
                    )
            case _:
                raise Exception(f"У товара не найдена фирма {firm} в базе")
    return products, not_stated_products


def new_items(ns_items_list, *, cur, trans):
    try:
        for item in ns_items_list:
            shop_tree = store_attribute(item["name"])
            dir_reg = directory_registry(cur)
            nom_attribute(cur, dir_reg=dir_reg)
            nom = new_nom(cur, dir_reg=dir_reg, name=item["name"], shop_tree=shop_tree, code=item["code"], firm_id=item["firm_id"], cost=item["default_price"], margin=65, firm_value=item["firm"])
            shop_price(cur, snid=nom, price=item["default_price"])
    except Exception as exc:
        ItemLOG.critical(exc)
        trans.rollback()
        return False
    else:
        trans.commit()
        return True

def create_list_items(ITEMS):
    # Создание несколько транзакций
    print(ITEMS)
    try:
        ItemLOG.debug("Подключение к базе данных")
        con = fdb.connect(  dsn=      cfg["Database"]["db_path"],
                            user=     cfg["Database"]["db_user"], 
                            password= cfg["Database"]["db_password"])
        newItems = con.trans()
        getItems = con.trans()
    except Exception as exc:
        ItemLOG.critical(f"Ошибка подключения к базе: {exc}")
        raise
    else:
        ItemLOG.info("База данных подключена успешно")

    # Курсор
    try:
        ItemLOG.debug("Создание курсора")
        newItem_cur = newItems.cursor()
        getItem_cur = getItems.cursor()
    except Exception as exc:
        ItemLOG.critical(f"Ошибка установки курсора: {exc}")
        con.close()
        raise
    else:
        ItemLOG.info("Курсор установлен успешно")

    try:
        with con:
            products, not_stated_products = get_items(ITEMS, cur=getItem_cur)
            ItemLOG.info("get_items отработал")

            if not_stated_products:
                try:
                    assert new_items(not_stated_products, cur=newItem_cur, trans=newItems)                
                except AssertionError as value:
                    ERRDATA.error(f"Есть товар, который не создался: {value}")
                    raise AssertionError(f"Есть товар, который не создался: {value}")
                else:
                    getItems.rollback()
            
            products, not_stated_products = get_items(ITEMS, cur=getItem_cur)
            assert not not_stated_products, "До сих пор есть товары после цикла создания"

            con.commit()
            print(products)
    except AssertionError as ass:
        con.rollback()
        ItemLOG.critical(ass)
        raise Exception(ass)
    except Exception as exc:
        ItemLOG.critical(f"Ошибка при выполнении запроса: {exc}")
        raise
    else:
        return products