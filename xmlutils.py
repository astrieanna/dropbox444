import xml.etree.ElementTree as ET
from resource import Resource
import datetime as DT

# parseResourceList :: String -> [Resource]
def parseResourceList(xmlstring):
    output = []
    e = ET.fromstring(xmlstring)
    for child in list(e):
        output.append(parseResource(child))
    return output

# buildResourceList :: [Resource] -> String
def buildResourceList(resources):
    e = ET.Element('ResourceList')
    for r in resources:
        e.append(buildResource(r))
    return ET.tostring(e)

# parseResourceDownload :: String -> Resource
def parseResourceDownload(xmlstring):
    e = ET.fromstring(xmlstring)
    return parseResource(e.find('Resource'))

# buildResourceDownload :: Resource -> String
def buildResourceDownload(resource):
    e = ET.Element('ResourceDownload')
    e.insert(0,buildResource(resource))
    return ET.tostring(e)

# parseResourceUpload :: String -> Resource
def parseResourceUpload(xmlstring):
    e = ET.fromstring(xmlstring)
    return parseResource(e.find('Resource'))

# buildResourceDownload :: Resource -> String
def buildResourceDownload(resource):
    e = ET.Element('ResourceUpload')
    e.insert(0,buildResource(resource))
    return ET.tostring(e)


#HELPERS:
# parseResource :: ET.Element -> Resource
def parseResource(e):
    r = Resource()
    r.category = e.get('category')
    r.name = e.findtext('ResourceName')
    if(r.category == 'directory'):
        r.numItems = e.findtext('ResourceNumItems')
    else:
        r.size = e.findtext('ResourceSize')
    r.url = e.findtext('ResourceURL')
    # r.path = urlToPath(r.url)
    r.resourceDate = parseDate(e.find('ResourceDate'))
    r.resourceType = e.findtext('ResourceType')
    return r

# parseDate :: ET.Element -> DT.DateTime
def parseDate(e):
    year = int(e.findtext('year'))
    month = int(e.findtext('month'))
    day = int(e.findtext('day'))
    hour = int(e.findtext('hour'))
    minu = int(e.findtext('min'))
    sec = int(e.findtext('sec'))
    return DT.datetime(year, month, day, hour, minu, sec)

# buildDate :: DT.DateTime -> ET.Element
def buildDate(dt):
    e = ET.Element('ResourceDate')
    e.append(ET.Element('year', {'text':dt.year}))
    e.append(ET.Element('month', {'text':dt.month}))
    e.append(ET.Element('day', {'text':dt.day}))
    e.append(ET.Element('hour', {'text':dt.hour}))
    e.append(ET.Element('min', {'text':dt.minute}))
    e.append(ET.Element('sec', {'text':dt.second}))
    return e

# buildResource :: Resource -> ET.Element
def buildResource(resource):
    e = ET.Element('Resource',{'category' : resource.category})
    e.append(ET.Element('ResourceName', {'text' : resource.name}))
    ET.dump(e)
    return e

if __name__ == "__main__":
    rl_xmlstr = "<ResourceList>\
                <Resource category=\"file\">\
                <ResourceName> test.pdf</ResourceName>\
                <ResourceSize> 128 </ResourceSize>\
                <ResourceURL> http://Dbox-sample.com/sampleuser/test.pdf </ResourceURL>\
                <ResourceDate>\
                <year>2010</year>\
                <month>10</month>\
                <day>13</day>\
                <hour>06</hour>\
                <min>24</min>\
                <sec>10</sec>\
                </ResourceDate>\
                <ResourceType> application/pdf </ResourceType>\
                </Resource>\
                </ResourceList>"
    rs = parseResourceList(rl_xmlstr)
    rl_xml = buildResourceList(rs)

