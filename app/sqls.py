from datetime import datetime


def document_registry(cur):
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    GET_REG_ID = "SELECT MAX(DOCUMENT_REGISTRY_ID) FROM DOCUMENT_REGISTRY WHERE METATABLE_ID = 42 AND CREATE_USER_ID = 1"
    CALC_REG = f"""
    INSERT INTO DOCUMENT_REGISTRY(
        METATABLE_ID,
        CREATE_USER_ID, 
        CREATE_DATE,
        CHANGE_USER_ID,
        CHANGE_DATE, 
        DOCUMENT_TYPE_ID_CACHE
    )
    VALUES(
        42,
        1,
        '{time_stamp}',
        1,
        '{time_stamp}',
        26
    )
    """
    try:
        cur.execute(CALC_REG)
        
    except Exception as exc:
        print(exc)
        raise
    else:
        return cur.execute(GET_REG_ID).fetchone()[0]


def document_calculation(cur, *, title: str, doc_reg_id: int):
    time_stamp = datetime.now().strftime("%Y-%m-%d")
    
    GET_CALC_ID = "SELECT MAX(SERVICE_CALCULATION_ITEM_ID) FROM SERVICE_CALCULATION_ITEM WHERE DOCUMENT_REGISTRY_ID = ?"
    CALC_DOC = f"""
    INSERT INTO SERVICE_CALCULATION_ITEM(
        NAME,
        PRICE_NORM_ID, 
        DATE_CREATE,
        DOCUMENT_REGISTRY_ID,
        DOCUMENT_TYPE_ID,
        FLAG,
        DISCOUNT_WORK,
        DISCOUNT_GOODS
    )
    VALUES(
        ?,
        6,
        '{time_stamp}',
        ?,
        26,
        16,
        0,
        0
    )
    """

    try:
        cur.execute(CALC_DOC, (title, doc_reg_id))
        
    except Exception as exc:
        print(exc)
        raise
    else:
        return cur.execute(GET_CALC_ID, (doc_reg_id, )).fetchone()[0]


def goods_calculation (cur, *, calc_id: int, sin_id: int, count: float, price: float, pos: int):
    CALC_DOC_GOODS = """
    INSERT INTO SERVICE_CALCULATION_GOODS(
        SERVICE_CALCULATION_ITEM_ID,
        SHOP_NOMENCLATURE_ID,
        DISCOUNT,
        GOODS_COUNT,
        COST,
        DISCOUNT_FIX,
        POSITION_NUMBER
    )
    VALUES(
        ?,
        ?,
        0,
        ?,
        ?,
        0,
        ?
    )
    """
    try:
        cur.execute(CALC_DOC_GOODS, (calc_id, sin_id, count, price, pos))
        
    except Exception as exc:
        print(exc)
        return False
    else:
        return True
    

def find_shopnom_id(cur, *, firm: int, code: str):
    SID_REQUEST = """
    SELECT SHOP_NOMENCLATURE_ID FROM SHOP_NOMENCLATURE
    WHERE PRODUCER_ID = ? AND CODE = ?
    """
    try:
        sid = cur.execute(SID_REQUEST, (firm, code)).fetchone()[0]
    except Exception as exc:
        print(exc)
        return None
    else:
        return sid


def directory_registry(cur, con):
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    GET_REG_ID = "SELECT MAX(DIRECTORY_REGISTRY_ID) FROM DIRECTORY_REGISTRY WHERE METATABLE_ID = 13 AND CREATE_USER_ID = 1"
    CALC_REG = f"""
    INSERT INTO DIRECTORY_REGISTRY(
        METATABLE_ID,
        CREATE_USER_ID, 
        CREATE_DATE,
        CHANGE_USER_ID,
        CHANGE_DATE
    )
    VALUES(
        13,
        1,
        '{time_stamp}',
        1,
        '{time_stamp}'
    )
    """
    try:
        cur.execute(CALC_REG)
        con.commit()
    except Exception as exc:
        print(exc)
        raise
    else:
        return cur.execute(GET_REG_ID).fetchone()[0]

def new_nom(cur, con, *, dir_reg, name: str, code, firm_id, cost, margin, firm_value):
    search_text = f"{name.upper()}*{name.upper()}**{firm_value.upper()}"
    search_nums = f"{code}**{code}"
    SHOP_NEW = """
    INSERT INTO SHOP_NOMENCLATURE(
        DIRECTORY_REGISTRY_ID,
        SHOP_NOMENCLATURE_TREE_ID,
        SHORTNAME,
        FULLNAME,
        CODE,
        NUMBER_MANUFACTURE,
        GOODS_TYPE_ID,
        UNIT_ID,
        TAX_SCHEMES_ID,
        PRODUCER_ID,
        DEFAULT_COST,
        DEFAULT_MARGIN,
        DEFAULT_COUNT,
        BARCODE_TYPE,
        DEFAULT_COUNT_IN,
        TAX_SCHEMES_MATERIAL_ID,
        SEARCH_VALUE_TEXT,
        SEARCH_VALUE_NUMS,
        SEARCH_VALUE_NUMBER_MANUFACTURE
    )
    VALUES(
        ?, 
        82,
        ?,
        ?,
        ?,
        ?,
        1,
        1,
        2,
        ?, 
        ?,
        ?,
        1,
        14,
        1,
        2,
        ?,
        ?,
        ?
    )
    """
    try:
        cur.execute(SHOP_NEW, (dir_reg, name, name, code, code, firm_id, cost, margin, search_text, search_nums, code))
        con.commit()
    except Exception as exc:
        print(exc)
        raise

def get_shop_num(cur, name: str, code, firm_value):
    search_text = f"{name.upper()}*{name.upper()}**{firm_value.upper()}"
    search_nums = f"{code}**{code}"
    GET_SHOP = "SELECT MAX(SHOP_NOMENCLATURE_ID) FROM SHOP_NOMENCLATURE WHERE SEARCH_VALUE_TEXT = ? AND SEARCH_VALUE_NUMS = ?"
    return cur.execute(GET_SHOP, (search_text, search_nums)).fetchone()[0]


def nom_attribute(cur, con, *, dir_reg):
    ATTR = "INSERT INTO SHOP_NOMENCLATURE_ATTRIBUTE(DIRECTORY_REGISTRY_ID) VALUES(?)"
    try:
        cur.execute(ATTR, (dir_reg, ))
        con.commit()
    except Exception as exc:
        print(exc)
        raise

def shop_price(cur, con, *, snid, price):
    SHOP_PRICE = """
    INSERT INTO SHOP_PRICE(
        SHOP_PRICE_LIST_ID,
        SHOP_NOMENCLATURE_ID,
        PRICE_POSITION,
        PRICE1
    ) 
    VALUES(
        3,
        ?,
        1,
        ?
    )"""
    try:
        cur.execute(SHOP_PRICE, (snid, price))
        con.commit()
    except Exception as exc:
        print(exc)
        raise

