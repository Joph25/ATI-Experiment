import xmltodict import parse

with open('config.xml') as fd:
    doc = xmltodict.parse(fd.read())
print(doc)
