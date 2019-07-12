from lxml.etree import Element, SubElement, tostring


def ncx(root_path, ncx_title, ncx_list):
    ncx = Element('ncx', attrib={'xmlns': 'http://www.daisy.org/z3986/2005/ncx/', 'version': '2005-1'})
    SubElement(ncx, 'head')
    docTitle = SubElement(ncx, 'docTitle')
    SubElement(docTitle, 'text').text = ncx_title
    navMap = SubElement(ncx, 'navMap')
    i = 1
    for nav in ncx_list:
        navPoint = gen_navPoint(navMap,nav,i)
        i += 1
        if 'child' in nav:
            for child_nav in nav['child']:
                gen_navPoint(navPoint, child_nav, i)
                i += 1

    ncx_xml = tostring(ncx, pretty_print=True)
    with open('%s\\toc.ncx' % (root_path), 'wb') as f:
        f.write(ncx_xml)


def gen_navPoint(parent_ele, nav, i):
    navPoint = SubElement(parent_ele, 'navPoint', attrib={'id': 'navpoint-%s' % (i), 'playOrder': '%s' % i})
    SubElement(SubElement(navPoint, 'navLabel'), 'text').text = nav['text']
    SubElement(navPoint, 'content', attrib={'src': nav['src']})
    return navPoint