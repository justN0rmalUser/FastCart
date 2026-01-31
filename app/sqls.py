from datetime import datetime


def document_registry(cur, *):
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
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
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
        POSITION_NUMBER
    )
    VALUES(
        ?,
        ?,
        0,
        ?,
        ?,
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