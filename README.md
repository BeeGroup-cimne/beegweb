# Gemweb
This library is used to obtain the data available from gemweb at the current version on 6-04-2021

Only the GET_INVENTORY and GET METERING requests can be used with the tested credentials.

To get information about the parameters, visit "http://manual.gemweb.es"
#### Usage

- import the library
```
from datagweb import gemweb, ENDPOINTS
```

- connect using gemweb credentials

```
gemweb.connection('username', 'password', timezone="UTC")
```

- use the different endpoints available in the datadis api

```
gemweb.gemweb_query(endpoint, **kwargs)
```

#### ENDPOINTS
params with * are required

GET_INVENTORY:

Request to get elements from the platform. 

    params:
        - category *: str
        - search_by: str
        - search_values: str
        - search_operator: str
        - order_by: str
        - limit: str

GET_METERING: 

Request to get data from the supply.

    params:
        - id_ *: int
        - date_from *: datetime
        - date_to *: datetime 
        - data_source: str = "comptador"
        - period: str 
        - field: str 
        - language: str

GET_INVOICE_INCONCISTENCIES: 

Petició per obtenir incoherències de factures.

    params:
 


GET_POWER_OPTIMIZATION:

Petició per obtenir optimitzacions de potències.

    params:
        
GET_COST_CONSUMPTION: 

Petició per obtenir l'anàlisi de cost o consum d'un subministrament.

    params:

GET_CALCULATED_INVOICE: 

Petició per generar una factura per un període especific agafant com a valors de consums les dades de telelectures.

    params:

GET_CONSUMPTION_BY_PERIOD: 

Petició per obtenir un anàlisi de consums separats per períodes.

    params:

GET_CONTRACT_SIMULATION: 

Petició per simular un canvi contractual sobre un subministrament.
 
    params:

PUT_METERING: 

Petició per enviar dades de telelectures al gemweb.

    params: