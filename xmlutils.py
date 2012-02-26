import xml.etree.ElementTree as ET
from resource import Resource
from resource import urlToPath
import datetime as DT

# parseResponse :: String -> (False, Resource) | (True, [Resource])
def parseResponse(xmlstring):
    e = ET.fromstring(xmlstring)
    if e.text == 'ResourceList':
        return (True, _parseResourceList(e))
    else:
        return (False, _parseResourceDownload(e))


# parseResourceList :: ET.Element -> [Resource]
def _parseResourceList(e):
    output = []
    for child in list(e):
        output.append(parseResource(child))
    return output

# parseResourceList :: ET.Element -> [Resource]
def parseResourceList(xmlstring):
    e = ET.fromstring(xmlstring)
    output = []
    for child in list(e):
        output.append(parseResource(child))
    return output


# buildResourceList :: [Resource] -> String
def buildResourceList(resources):
    e = ET.Element('ResourceList')
    for r in resources:
        e.append(buildResource(r))
    return ET.tostring(e)

# parseResourceDownload :: ET.Element -> Resource
def _parseResourceDownload(e):
    return parseResource(e.find('Resource'))

# parseResourceDownload :: ET.Element -> Resource
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
propertiesToTags = {
    'name':'ResourceName',
    'url':'ResourceURL',
    'encoding':'ResourceEncoding',
    'content':'ResourceContent',
    'resourceType':'ResourceType'
}


# parseResource :: ET.Element -> Resource
def parseResource(e):
    r = Resource()
    ETtoObject(e,r,propertiesToTags)
    r.category = e.get('category')
    if r.category == 'directory':
        if e.findtext('ResourceNumItems') is not None:
            r.numItems = int(e.findtext('ResourceNumItems'))
    elif e.findtext('ResourceSize') is not None:
        r.size = int(e.findtext('ResourceSize'))
    if hasattr(r,'url'):
        r.path = urlToPath(r.url)
    r.resourceDate = parseDate(e.find('ResourceDate'))
    return r

def ETtoObject(et, obj, ptot):
    for (prop, tag) in ptot.iteritems():
        val = et.findtext(tag)
        if val is not None:
            setattr(obj, prop, val)

# buildResource :: Resource -> ET.Element
def buildResource(resource):
    e = ET.Element('Resource',{'category' : resource.category})
    e.extend(objectToET(resource,propertiesToTags))
    ec = None
    if resource.category == 'directory':
        if hasattr(resource,'numItems'):
            ec = ET.Element('ResourceNumItems')
            ec.text = str(resource.numItems)
    elif hasattr(resource, 'size'):
        ec = ET.Element('ResourceSize')
        ec.text = str(resource.size)
    if ec is not None:
        e.append(ec)

    if hasattr(resource, 'resourceDate') and resource.resourceDate is not None:
        e.append(buildDate(resource.resourceDate))

    return e

def objectToET(obj, propertiesToTags):
    ets = []
    for (prop, tag) in propertiesToTags.iteritems():
        if hasattr(obj, prop):
            ec = ET.Element(tag)
            ec.text = getattr(obj, prop)
            ets.append(ec)
    return ets

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
