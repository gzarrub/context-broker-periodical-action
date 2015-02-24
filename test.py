__author__ = 'b.gzr'
import functions as f
import requests
# import pyproj

# epsg3857 = pyproj.Proj(init='epsg:3857')
# wgs84 = pyproj.Proj(init='EPSG:4326')
# latlng = (45.618, -73.604)
# pyproj.transform(wgs84,epsg3857,latlng[0],latlng[1])
# (5078172.5310075525, -12357511.560866801)



# o = f.ContextBroker('http://orion.lab.fiware.org:1026', 'guillermo-zarzuelo-1', '29Zarzu')
# o = f.ContextBroker('http://127.0.0.1:4000')
o = f.ContextBroker('http://130.206.85.12:1026')
# o = f.ContextBroker('http://130.206.127.30:1026')



# for i in range(1, 5):
#     _id = 'urn::Sevilla:Sevici%s' % str(i)
#     o.entity.entity_add(_id, 'sevici')
# o.entity.entity_add('urn::Sevilla:Sevici26', 'sevici')
# print o.query_context().text

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
response = requests.get('http://datos.santander.es/api/rest/datasets/control_flotas_posiciones.json', headers=headers)

# epsg3857 = pyproj.Proj(init='epsg:3857')
# wgs84 = pyproj.Proj(init='EPSG:4326')

for i in range(len(response.json()['resources'])):
    entity_id = "urn:x-iot:smartsantander:ayto:vehicle:%s" % response.json()['resources'][i]['ayto:vehiculo']
    o.entity.entity_add(entity_id,'test')
    for attrib in response.json()['resources'][i]:
        if attrib in ['ayto:geolon','ayto:geolat'] and 'coords' not in o.entity.attribute.get_attribute_list():
            pos = (0,0)
            # pos = pyproj.transform(epsg3857,wgs84, float(data['ayto:geolat']),float(data['ayto:geolon']))
            position = "%s,%s" %(str(pos[0]), str(pos[1]))
            o.entity.attribute.attribute_add('position','coords',value=position)
            o.entity.attribute.metadata.metadata_add('location', 'string', 'WGS84')
            o.entity.attribute.add_metadatas_to_attrib('location')
            o.entity.attribute.metadata.metadata_list_purge()

        elif attrib in ['ayto:geom2d:x','ayto:geom2d:y'] and 'area' not in o.entity.attribute.get_attribute_list():
            pos = (0,0)
            # pos = pyproj.transform(epsg3857,wgs84, float(data[''geom2d:y'']),float(data[''geom2d:x'']))
            position = "%s,%s" %(str(pos[0]), str(pos[1]))
            o.entity.attribute.attribute_add('area','coords',value=position)
            o.entity.attribute.metadata.metadata_add('area', 'string', 'WGS84')
            o.entity.attribute.add_metadatas_to_attrib('area')
            o.entity.attribute.metadata.metadata_list_purge()

        elif attrib in ['ayto:instante', 'dc:modified']:
            o.entity.attribute.attribute_add(attrib,'urn:x-ogc:def:trs:IDAS:1.0:ISO8601',value=response.json()['resources'][i][attrib])

        elif attrib == 'ayto:vehiculo':
            pass
        else:
            attrib_type = 'string'
            o.entity.attribute.attribute_add(attrib, attrib_type, value=response.json()['resources'][i][attrib])

    o.entity.add_attributes_to_entity(entity_id)
    o.entity.attribute.attribute_list_purge()



print o.entity.get_entity_list()
