import requests

requests.post(url='http://10.0.2.117:8080/api', {e'A':{        'Total':1000,        'Available':2,        'Occupancy':1    },    'B':{        'Total':1000,        'Available':2,        'Occupancy':1    },   'C':{'Total':1000,       'Available':2,        'Occupancy':1}})