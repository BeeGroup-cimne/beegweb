import collections
import pytz
from enum import Enum
import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import xmltodict

timezone_source = "Europe/Madrid"


def __dummy_parse__(data: collections.OrderedDict) -> list:
    return list(data)


def __get_access_params__(client_id: str, client_secret: str) -> dict:
    return {
        "request": "get_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }


def __get_inventory_params__(access_token: str, category: str, search_by: str = "", search_values: str = "",
                             search_operator: str = "", order_by: str = "", limit: str = "") -> dict:
    return {
        "request": "get_inventory",
        "access_token": access_token,
        "category": category,
        "search_by": search_by,
        "search_values": search_values,
        "search_operator": search_operator,
        "order_by": order_by,
        "limit": limit
    }


def __get_inventory_parse__(data: collections.OrderedDict) -> list:
    return_value = list(data['registre'].items())[1][1]
    return_value = [dict(x) for x in return_value]
    return return_value


def __get_invoice_inconsistencies_params__(access_token: str, category: str, id_: int, inconsistencies: str = "",
                                           percentages: str = "", language: str = "es") -> dict:
    return {
        "request": "get_invoice_inconsistencies",
        "access_token": access_token,
        "category": category,
        "id": id_,
        "inconsistencies": inconsistencies,
        "percentages": percentages,
        "language": language
    }


def __get_power_optimization_params__(access_token: str, id_: int, date_from: datetime, date_to: datetime,
                                      language: str = "es") -> dict:
    return {
        "request": "get_power_optimization",
        "access_token": access_token,
        "id": id_,
        "date_from": date_from.strftime("%Y-%m-%d"),
        "date_to": date_to.strftime("%Y-%m-%d"),
        "language": language
    }


def __get_cost_consumption_params__(access_token: str, id_: int, type_: str, date_from: datetime, date_to: datetime,
                                    source: str = "", billing_date: bool = False) -> dict:
    return {
        "request": "get_cost_consumption",
        "access_token": access_token,
        "id": id_,
        "date_from": date_from.strftime("%Y-%m-%d"),
        "date_to": date_to.strftime("%Y-%m-%d"),
        "type": type_,
        "source": source,
        "billing_date": 1 if billing_date else 0
    }


def __get_calculated_invoice_params__(access_token: str, id_: int, date_from: datetime, date_to: datetime,
                                      language: str = "es") -> dict:
    return {
        "request": "get_calculated_invoice",
        "access_token": access_token,
        "id": id_,
        "date_from": date_from.strftime("%Y-%m-%d"),
        "date_to": date_to.strftime("%Y-%m-%d"),
        "language": language
    }


def __get_consumption_by_period_params__(access_token: str, id_: int, period: str, date_from: datetime,
                                         date_to: datetime, language: str = "es") -> dict:
    return {
        "request": "get_consumption_by_period",
        "access_token": access_token,
        "id": id_,
        "date_from": date_from.strftime("%Y-%m-%d"),
        "date_to": date_to.strftime("%Y-%m-%d"),
        "period": period,
        "language": language
    }


def __get_contract_simulation_params__(access_token: str, id_: int, contract_date_from: datetime,
                                       contract_date_to: datetime, contract_fields: str, contract_values: str,
                                       date_from: datetime, date_to: datetime, language: str = "es") -> dict:
    return {
        "request": "get_contract_simulation",
        "access_token": access_token,
        "id": id_,
        "contract_date_from": contract_date_from.strftime("%Y-%m-%d"),
        "contract_date_to": contract_date_to.strftime("%Y-%m-%d"),
        "contract_fields": contract_fields,
        "contract_values": contract_values,
        "date_from": date_from.strftime("%Y-%m-%d"),
        "date_to": date_to.strftime("%Y-%m-%d"),
        "language": language
    }


def __get_metering_params__(access_token: str, id_: int, date_from: datetime, date_to: datetime,
                            data_source: str = "comptador", period: str = "diari", field: str = "consum",
                            language: str = "es") -> dict:
    return {
        "request": "get_metering",
        "access_token": access_token,
        "id": id_,
        "date_from": date_from.strftime("%Y-%m-%d"),
        "date_to": date_to.strftime("%Y-%m-%d"),
        "data_source": data_source,
        "period": period,
        "field": field,
        "language": language
    }


def __get_last_sunday__(ts: datetime) -> datetime:
    last_day = ts + relativedelta(day=31)
    offset = (int(last_day.weekday()) - 6) % 7
    return last_day - timedelta(days=offset)


def __get_metering_parse__(data: collections.OrderedDict) -> list:
    # we get the data in local time, we have the problem on timezones...
    # 1- when we skip  1 hour (in mars, 2am becomes 3am) we have the time 2am, but no value
    # 2- when there is 2 hours as the same (in october, 3am becomes 2am again) the values are added on the 3am hour
    dirty_values = data['resultat']['subministrament']['values']['value']
    return_values = []
    timezone = gemweb.timezone
    for item in dirty_values:
        item = dict(item)
        new_item = {}
        try:
            ts = datetime.strptime(item['@date'], "%Y-%m-%d %H:%M")
            hourly = True
        except ValueError:
            try:
                ts = datetime.strptime(item['@date'], "%Y-%m-%d")
                hourly = False
            except ValueError:
                try:
                    ts = datetime.strptime(item['@date'], "%Y-%m")
                    hourly = False
                except ValueError:
                    ts = datetime.strptime(item['@date'], "%Y")
                    hourly = False

        u = data['resultat']['subministrament']['units']
        if ts.month == 3:  # this will ignore the 1 tz problem
            last_sunday = __get_last_sunday__(ts)
            if ts.day == last_sunday.day and ts.hour == 2:
                continue
        if ts.month == 10:  # this will correct the 2 tz problem
            last_sunday = __get_last_sunday__(ts)
            v = float(item['#text'])
            if ts.day == last_sunday.day and ts.hour == 2:
                ts1 = datetime(ts.year, ts.month, ts.day, 0, 0, tzinfo=pytz.utc)
                new_item = [{"timestamp": ts1, "value": v, "unit": u}]
                return_values.extend(new_item)
                continue
            if ts.day == last_sunday.day and ts.hour == 3:
                v = float(item['#text'])
                ts1 = datetime(ts.year, ts.month, ts.day, 1, 0, tzinfo=pytz.utc)
                ts2 = datetime(ts.year, ts.month, ts.day, 2, 0, tzinfo=pytz.utc)
                new_item = [{"timestamp": ts1, "value": v / 2, "unit": u},
                            {"timestamp": ts2, "value": v / 2, "unit": u}]
                return_values.extend(new_item)
                continue
        v = float(item['#text'])
        if hourly:
            new_item['timestamp'] = pytz.timezone(timezone_source).localize(ts).astimezone(pytz.utc)
        else:
            new_item['timestamp'] = ts

        new_item['value'] = v
        new_item['unit'] = u
        return_values.append(new_item)

    for i in return_values:
        i['timestamp'] = i['timestamp'] - timedelta(hours=1)
        i['timestamp'] = i['timestamp'].astimezone(pytz.timezone(timezone))
    return return_values


def __put_metering_params__(access_token: str, category: str, id_: int, datetime_: datetime, frequency: int,
                            values: str, fields: str = "", overwrite: bool = False) -> dict:
    return {
        "request": "put_metering",
        "access_token": access_token,
        "category": category,
        "id": id_,
        "datetime": datetime_.strftime("%Y-%m-%d %H:%M:%S"),
        "frequency": frequency,
        "values": values,
        "fields": fields,
        "overwrite": 1 if overwrite else 0
    }


class ENDPOINTS(Enum):
    class GET_INVENTORY(Enum):
        params = __get_inventory_params__
        parse = __get_inventory_parse__

    class GET_METERING(Enum):
        params = __get_metering_params__
        parse = __get_metering_parse__

    class GET_POWER_OPTIMIZATION(Enum):
        params = __get_power_optimization_params__
        parse = __dummy_parse__

    class GET_CALCULATED_INVOICE(Enum):
        params = __get_calculated_invoice_params__
        parse = __dummy_parse__

    class GET_CONSUMPTION_BY_PERIOD(Enum):
        params = __get_consumption_by_period_params__
        parse = __dummy_parse__

    class GET_CONTRACT_SIMULATION(Enum):
        params = __get_contract_simulation_params__
        parse = __dummy_parse__

    class GET_COST_CONSUMPTION(Enum):
        params = __get_cost_consumption_params__
        parse = __dummy_parse__

    class GET_INVOICE_INCONSISTENCIES(Enum):
        params = __get_invoice_inconsistencies_params__
        parse = __dummy_parse__

    class PUT_METERING(Enum):
        params = __put_metering_params__
        parse = __dummy_parse__


class gemweb(object):
    username = None
    password = None
    token = None
    url = "https://api.gemweb.es"
    timezone = None

    @classmethod
    def __gemweb_request__(cls, params, parse):
        response = cls.__request_xml__(params)
        if 'resultat' in response and 'error' in response['resultat']:
            if response['resultat']['error'].split(":")[0] == "invalid_token":
                cls.__login__()
                response = cls.__request_xml__(params)
            if 'error' in response['resultat']:
                raise Exception(str(response['resultat']['error']))
        return parse(response)

    @classmethod
    def connection(cls, username: str, password: str,  timezone="UTC"):
        cls.username = username
        cls.password = password
        cls.__login__()
        cls.timezone = timezone

    @classmethod
    def __request_xml__(cls, params):
        xml_response = requests.post(cls.url, data=params)
        if xml_response.ok:
            return xmltodict.parse(xml_response.content)
        else:
            raise xml_response.reason

    @classmethod
    def __login__(cls, retries=0):
        response = cls.__request_xml__(__get_access_params__(cls.username, cls.password))
        if 'resultat' not in response or 'access_token' not in response['resultat']:
            if retries >= 20:
                raise Exception(str(response))
            cls.__login__(retries + 1)
        else:
            cls.token = response['resultat']['access_token']

    @classmethod
    def gemweb_query(cls, endpoint, **kwargs):
        endpoint_enum = endpoint.value
        params = endpoint_enum.params(access_token=cls.token, **kwargs)
        data = cls.__gemweb_request__(params=params, parse=endpoint_enum.parse)
        return data
