from lxml.etree import Element, SubElement, tostring


def opf(root_path, dc_info, item_info):
    opf = 'http://www.idpf.org/2007/opf'
    asd = 'http://www.idpf.org/asdfaf'
    nsmap = {'opf': opf, 'asd': asd}
    dc = 'http://purl.org/metadata/dublin_core'
    oebpackage = 'http://openebook.org/namespaces/oeb-package/1.0/'
    nsdc = {'dc': dc, 'oebpackage': oebpackage}
    package = Element('package', nsmap=nsmap, attrib={'unique-identifier': 'uid'})
    metadata = SubElement(package, 'metadata')
    dc_metadata = SubElement(metadata, 'dc-metadata', nsmap=nsdc)
    SubElement(dc_metadata, '{%s}Title' % dc).text = dc_info['Title']
    SubElement(dc_metadata, '{%s}Language' % dc).text = dc_info['Language']
    SubElement(dc_metadata, '{%s}Creator' % dc).text = dc_info['Creator']
    SubElement(dc_metadata, '{%s}Copyrights' % dc).text = dc_info['Copyrights']
    SubElement(dc_metadata, '{%s}Publisher' % dc).text = dc_info['Publisher']
    SubElement(SubElement(dc_metadata, 'x-metadata'), 'EmbeddedCover').text = 'images/cover.jpg'
    manifest = SubElement(package, 'manifest')
    SubElement(manifest, 'item', attrib={'id': 'content', 'media-type': 'text/x-oeb1-document', 'href': 'toc.html'})
    SubElement(manifest, 'item', attrib={'id': 'ncx', 'media-type': 'application/x-dtbncx+xml', 'href': 'toc.ncx'})
    for item in item_info:
        SubElement(manifest, 'item',
                   attrib={'id': item['id'], 'media-type': 'text/x-oeb1-document', 'href': item['href']})
    spine = SubElement(package, 'spine', attrib={'toc': 'ncx'})
    SubElement(spine, 'itemref', attrib={'idref': 'content'})
    for item in item_info:
        SubElement(spine, 'itemref', attrib={'idref': item['id']})
    guide = SubElement(package, 'guide')
    SubElement(guide, 'reference', attrib={'type': 'toc', 'title': 'Table of Contents', 'href': 'toc.html'})
    SubElement(guide, 'reference', attrib={'type': 'text', 'title': 'Book', 'href': item_info[0]['href']})

    opf_xml = tostring(package, encoding="utf-8", pretty_print=True, method="html")
    with open('%s\\%s.opf' % (root_path, dc_info['Title']), 'wb') as f:
        f.write(opf_xml)


