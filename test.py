__author__ = 'b.gzr'
import functions as f
import requests
import pyproj
import time


def action():
    o = f.ContextBroker('http://130.206.85.12:1026')
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    response = requests.get('http://datos.santander.es/api/rest/datasets/control_flotas_posiciones.json', headers=headers)
    
    #saving all the data in files
#    filename = "files/"+str(int(time.time()))
#    print filename

    file = open(filename,"w")
    file.write(response.text)
    file.close()

    epsg23030 = pyproj.Proj(init='EPSG:23030')
    wgs84 = pyproj.Proj(init='EPSG:4326')

    for i in range(len(response.json()['resources'])):
        entity_id = "bus.%s" % response.json()['resources'][i]['ayto:coche']
        o.entity.entity_add(entity_id,'device')

        for attrib in response.json()['resources'][i]:

            if attrib == 'ayto:geolon':
                pos = pyproj.transform(epsg23030,wgs84, float(response.json()['resources'][i]['ayto:geolat']),float(response.json()['resources'][i]['ayto:geolon']))
                position = "%s,%s" %(str(pos[1]), str(pos[0]))
                o.entity.attribute.attribute_add('position','coords',value=position)
                o.entity.attribute.metadata.metadata_add('location', 'string', 'WGS84')
                o.entity.attribute.add_metadatas_to_attrib('position')
                o.entity.attribute.metadata.metadata_list_purge()

            elif attrib == 'ayto:instante':
                o.entity.attribute.attribute_add('TimeInstant','ISO8601',value=response.json()['resources'][i][attrib])

            elif attrib == 'dc:modified':
                o.entity.attribute.attribute_add('TimeInstantModified','ISO8601',value=response.json()['resources'][i][attrib])

            elif attrib in ['ayto:coche', 'geom2d:x', 'geom2d:y', 'ayto:geolat']:
                pass
            else:

                s = ['ayto:velocidad', 'ayto:linea', 'ayto:servicio', 'ayto:vehiculo', 'ayto:estado', 'ayto:indice','id']
                d = ['speed', 'line', 'service', 'vehicle', 'status', 'index', 'id']
                index = s.index(attrib)
                attrib_translated = d[index]


                if attrib in ['index', 'speed']:
                    attrib_type = 'number'
                else:
                    attrib_type = 'string'

                o.entity.attribute.attribute_add(attrib_translated, attrib_type, value=response.json()['resources'][i][attrib])

        o.entity.add_attributes_to_entity(entity_id)
        o.entity.attribute.attribute_list_purge()

        o.update_context()
#	print o.update_context().text  #Muestra la respuesta de CB para cada update
#   o.update_context() # hace el update de todas las entidades del json a la vez, muchos warnings por entidades repetidas


if __name__ == '__main__':
    action()
