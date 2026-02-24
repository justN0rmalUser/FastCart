from datetime import datetime


def document_registry(cur):
    # time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    GET_REG_ID = "SELECT MAX(DOCUMENT_REGISTRY_ID) FROM DOCUMENT_REGISTRY WHERE METATABLE_ID = 42 AND CREATE_USER_ID = 1"
    CALC_REG = """
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
        ?,
        1,
        ?,
        26
    )
    """
    try:
        cur.execute(CALC_REG, (datetime.now(), datetime.now()))
        
    except Exception as exc:
        print("doc_reg:", exc)
        raise
    else:
        return cur.execute(GET_REG_ID).fetchone()[0]


def document_calculation(cur, *, title: str, descript: str, doc_reg_id: int):
    # time_stamp = datetime.now().strftime("%Y-%m-%d")
    
    GET_CALC_ID = "SELECT MAX(SERVICE_CALCULATION_ITEM_ID) FROM SERVICE_CALCULATION_ITEM WHERE DOCUMENT_REGISTRY_ID = ?"
    CALC_DOC = """
    INSERT INTO SERVICE_CALCULATION_ITEM(
        NAME,
        PRICE_NORM_ID, 
        NOTES,
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
        ?,
        CURRENT_DATE,
        ?,
        26,
        16,
        0,
        0
    )
    """

    try:
        cur.execute(CALC_DOC, (title, descript, doc_reg_id))
    except Exception as exc:
        print("doc_calc:", exc)
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
        print("goods:", exc)
        raise
    

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


def directory_registry(cur):
    # time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    GET_REG_ID = "SELECT MAX(DIRECTORY_REGISTRY_ID) FROM DIRECTORY_REGISTRY WHERE METATABLE_ID = 13 AND CREATE_USER_ID = 1"
    CALC_REG = """
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
        ?,
        1,
        ?
    )
    """
    try:
        cur.execute(CALC_REG, (datetime.now(), datetime.now()))
        
    except Exception as exc:
        print("dir_reg:", exc)
        raise
    else:
        return cur.execute(GET_REG_ID).fetchone()[0]

def new_nom(cur, *, dir_reg, name: str, code, firm_id, cost, margin, firm_value):
    search_text = f"{name.upper().replace(' ', '')}*{name.upper().replace(' ', '')}**{firm_value.upper().replace(' ', '')}"
    search_nums = f"{code.replace(' ', '')}**{code.replace(' ', '')}"
    SHOP_NEW = """
    INSERT INTO SHOP_NOMENCLATURE(
        SHOP_NOMENCLATURE_ID,
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
        gen = cur.execute("SELECT NEXT VALUE FOR GEN_SHOP_NOMENCLATURE FROM RDB$DATABASE").fetchone()[0]
        cur.execute(SHOP_NEW, (gen, dir_reg, name, name, code, code, firm_id, cost, margin, search_text, search_nums, code))
        print(search_text, search_nums)
    except Exception as exc:
        print(exc)
        raise
    else:
        return gen



def nom_attribute(cur, *, dir_reg):
    ATTR = "INSERT INTO SHOP_NOMENCLATURE_ATTRIBUTE(DIRECTORY_REGISTRY_ID) VALUES(?)"
    try:
        cur.execute(ATTR, (dir_reg, ))
    except Exception as exc:
        print(exc)
        raise

def shop_price(cur, *, snid, price):
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
    except Exception as exc:
        print(exc)
        raise

