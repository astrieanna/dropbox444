import xml.etree.ElementTree as ET

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
    ET.dump(e)
    return Resource()

# buildResource :: Resource -> ET.Element
def buildResource(resource):
    e = ET.Element('Resource',{'category' => resource.category})
    e.append(ET.Element('ResourceName', {'text' => resource.name}))
    ET.dump(e)
    return e