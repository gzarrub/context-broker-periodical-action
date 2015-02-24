__author__ = 'b.gzr'
import functions as f
import requests
import pyproj
epsg3857 = pyproj.Proj(init='epsg:3857')
wgs84 = pyproj.Proj(init='EPSG:4326')
latlng = (45.618, -73.604)
pyproj.transform(wgs84,epsg3857,latlng[0],latlng[1])
(5078172.5310075525, -12357511.560866801)



# o = f.ContextBroker('http://orion.lab.fiware.org:1026', 'guillermo-zarzuelo-1', '29Zarzu')
# o = f.ContextBroker('http://127.0.0.1:4000')
# o = f.ContextBroker('http://130.206.85.12:1026')
# o = f.ContextBroker('http://130.206.127.30:1026')



# for i in range(1, 5):
#     _id = 'urn::Sevilla:Sevici%s' % str(i)
#     o.entity.entity_add(_id, 'sevici')
# o.entity.entity_add('urn::Sevilla:Sevici26', 'sevici')
# print o.query_context().text

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
response = requests.get('http://datos.santander.es/api/rest/datasets/control_flotas_posiciones.json', headers=headers)

print response.json()['resources'][0]


