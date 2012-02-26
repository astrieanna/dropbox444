import xml.etree.ElementTree as ET
from resource import Resource
from resource import urlToPath
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
    if r.category == 'directory':
        r.numItems = int(e.findtext('ResourceNumItems'))
    else:
        r.size = int(e.findtext('ResourceSize'))
    r.url = e.findtext('ResourceURL')
    if r.url:
        r.path = urlToPath(r.url)
    r.resourceDate = parseDate(e.find('ResourceDate'))
    r.resourceType = e.findtext('ResourceType')
    r.encoding = e.findtext('ResourceEncoding')
    r.content = e.findtext('ResourceContent')
    return r

# buildResource :: Resource -> ET.Element
def buildResource(resource):
    e = ET.Element('Resource',{'category' : resource.category})
    if resource.category == 'directory':
        ec = ET.Element('ResourceNumItems')
        ec.text = str(resource.numItems)
    else:
        ec = ET.Element('ResourceSize')
        ec.text = str(resource.size)
    e.append(ec)

    ec = ET.Element('ResourceName')
    ec.text = resource.name
    e.append(ec)

    ec = ET.Element('ResourceURL')
    ec.text = resource.url
    e.append(ec)

    if hasattr(resource, 'resourceDate'):
        e.append(buildDate(resource.resourceDate))

    if hasattr(resource, 'encoding'):
        ec = ET.Element('ResourceEncoding')
        ec.text = resource.encoding
        e.append(ec)
    if hasattr(resource, 'content'):
        ec = ET.Element('ResourceContent')
        ec.text = resource.content
        e.append(ec)

    ec = ET.Element('ResourceType')
    ec.text = resource.resourceType
    e.append(ec)
    return e

# parseDate :: ET.Element -> DT.DateTime
def parseDate(e):
    if e is None:
        return None
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
    y = ET.Element('year')
    y.text = str(dt.year)
    e.append(y)
    m = ET.Element('month')
    m.text = str(dt.month)
    e.append(m)
    d = ET.Element('day')
    d.text = str(dt.day)
    e.append(d)
    h = ET.Element('hour')
    h.text = str(dt.hour)
    e.append(h)
    mi = ET.Element('min')
    mi.text = str(dt.minute)
    e.append(mi)
    s = ET.Element('sec')
    s.text = str(dt.second)
    e.append(s)
    
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
                <Resource category=\"directory\">\
                <ResourceName>mymusic </ResourceName>\
                </Resource>\
                </ResourceList>"
    rs = parseResourceList(rl_xmlstr)
    print "RS:"
    for r in rs:
        print "\t%s" % (r.name)
    rl_xml = buildResourceList(rs)
    rs2 = parseResourceList(rl_xml)
    print "RS2:"
    for r2 in rs2:
        print "\t%s" % (r2.name)
