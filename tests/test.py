from datagweb import gemweb, ENDPOINTS
from datetime import datetime
import json
f = open("../config.json", "r")
config = json.load(f)


gemweb.connection(config['gemweb']['username'], config['gemweb']['password'], timezone="Europe/Madrid")
x = gemweb.gemweb_query(ENDPOINTS.GET_INVENTORY, category="entitats")
x = gemweb.gemweb_query(ENDPOINTS.GET_INVENTORY, category="centres_consum")
x = gemweb.gemweb_query(ENDPOINTS.GET_INVENTORY, category="instalacions_solars")
x = gemweb.gemweb_query(ENDPOINTS.GET_INVENTORY, category="factures")

x = gemweb.gemweb_query(ENDPOINTS.GET_INVENTORY, category="subministraments")
x1 = gemweb.gemweb_query(ENDPOINTS.GET_METERING, id_=x[0]['id'],
                         date_from=datetime(2020, 1, 1), date_to=datetime.now(), period="diari")
x2 = gemweb.gemweb_query(ENDPOINTS.GET_METERING, id_=x[0]['id'],
                         date_from=datetime(2020, 1, 1), date_to=datetime.now(), period="horari")
x3 = gemweb.gemweb_query(ENDPOINTS.GET_METERING, id_=x[0]['id'],
                         date_from=datetime(2020, 1, 1), date_to=datetime.now(), period="mensual")