import sys

from dateutil.relativedelta import relativedelta

sys.path.insert(1, 'src/gemweb')
from datagweb import gemweb, ENDPOINTS
from datetime import datetime
import json
f = open("config.json", "r")
config = json.load(f)
gemweb.connection(config['gemweb']['username'], config['gemweb']['password'], timezone="Europe/Madrid")
x = gemweb.gemweb_query(ENDPOINTS.GET_INVENTORY, category="subministraments")
date_from = datetime(2017, 1, 1)
date_to = datetime.now()
xxx = []
while date_from < date_to:
    date_to2 = date_from + relativedelta(months=1)
    try:
        x2 = gemweb.gemweb_query(ENDPOINTS.GET_METERING, id_="100792",
                                 date_from=date_from, date_to=date_to2, period="horari")
    except Exception as e:
        print(e)
        x2 = []
    date_from = date_to2 + relativedelta(days=1)
    print(date_from)
    xxx.append(x2)

data = []
[data.extend(x) for x in xxx]

gemweb.connection(config['gemweb']['username'], config['gemweb']['password'], timezone="Europe/Madrid")
x = gemweb.gemweb_query(ENDPOINTS.GET_INVENTORY, category="entitats")
x = gemweb.gemweb_query(ENDPOINTS.GET_INVENTORY, category="centres_consum")
x = gemweb.gemweb_query(ENDPOINTS.GET_INVENTORY, category="instalacions_solars")
x = gemweb.gemweb_query(ENDPOINTS.GET_INVENTORY, category="factures", search_by="data_creacio")

x = gemweb.gemweb_query(ENDPOINTS.GET_INVENTORY, category="subministraments")
x1 = gemweb.gemweb_query(ENDPOINTS.GET_METERING, id_=x[0]['id'],
                         date_from=datetime(2020, 1, 1), date_to=datetime.now(), period="anual")
x2 = gemweb.gemweb_query(ENDPOINTS.GET_METERING, id_=x[0]['id'],
                         date_from=datetime(2020, 1, 1), date_to=datetime.now(), period="horari")
x3 = gemweb.gemweb_query(ENDPOINTS.GET_METERING, id_=x[0]['id'],
                         date_from=datetime(2020, 1, 1), date_to=datetime.now(), period="mensual")