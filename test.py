from datagweb import gemweb, ENDPOINTS
from datetime import datetime
import json
f = open("config.json", "r")
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

#                          date_from=datetime(2020, 1, 1), date_to=datetime.now(), period="horari")
# x2 = gemweb.gemweb_query(ENDPOINTS.GET_CONSUMPTION_BY_PERIOD, id=x[0]['id'], period="mensual",
#                          date_from=datetime(2020, 1, 1), date_to=datetime.now())
#
# x3 = gemweb.gemweb_query(ENDPOINTS.GET_POWER_OPTIMIZATION, id=x[0]['id'],
#                          date_from=datetime(2020, 1, 1), date_to=datetime.now())
# x4 = gemweb.gemweb_query(ENDPOINTS.GET_CALCULATED_INVOICE, id=x[0]['id'],
#                          date_from=datetime(2020, 1, 1), date_to=datetime.now())
# x5 = gemweb.gemweb_query(ENDPOINTS.GET_INVOICE_INCONSISTENCIES, category="subministraments", id=x[0]['id'])
# x6 = gemweb.gemweb_query(ENDPOINTS.GET_CONTRACT_SIMULATION, id=x[0]['id'], contract_date_from=datetime(2021, 1, 1),
#                          contract_date_to=datetime.now(), contract_fields="preu_ene_p1", contract_values=3,
#                          date_from=datetime(2020, 1, 1), date_to=datetime.now())
# x7 = gemweb.gemweb_query(ENDPOINTS.GET_COST_CONSUMPTION, id=x[0]['id'], type="cost", date_from=datetime(2020, 1, 1),
#                          date_to=datetime.now())
# x8 = gemweb.gemweb_query(ENDPOINTS.PUT_METERING, category="subministraments", id=x[0]['id'],
#                          datetime=datetime(2010, 1, 1), frequency=10, values={})
