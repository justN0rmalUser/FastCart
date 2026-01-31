from datetime import timedelta, datetime
from zeep import Client
from zeep.helpers import serialize_object
import json
from pprint import pprint as pp


client = Client("http://api.rossko.ru/service/v2.1/GetSettlements")
result = serialize_object(client.service.GetSettlements(
    KEY1="29a962af3ba240b014147bc6271e9de6",
    KEY2="9e1f5e4bfbb91f2359a897fc8664a643"
    # start_date=datetime.now() - timedelta(3),
    # end_date=datetime.now()
))
pp(result)
# with open("js_res.json", 'w', encoding='utf-8') as js:
#     js.write(json.dumps(result, ensure_ascii=False, indent=4))
