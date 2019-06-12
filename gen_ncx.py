from lxml.etree import Element, SubElement, tostring


def ncx(root_path, ncx_title, ncx_list):
    ncx = Element('ncx', attrib={'xmlns': 'http://www.daisy.org/z3986/2005/ncx/', 'version': '2005-1'})
    SubElement(ncx, 'head')
    docTitle = SubElement(ncx, 'docTitle')
    SubElement(docTitle, 'text').text = ncx_title
    navMap = SubElement(ncx, 'navMap')
    i = 1
    for nav in ncx_list:
        navPoint = SubElement(navMap, 'navPoint', attrib={'id': 'navpoint-%s' % (i), 'playOrder': '%s' % i})
        SubElement(SubElement(navPoint, 'navLabel'), 'text').text = nav['text']
        SubElement(navPoint, 'content', attrib={'src': nav['src']})
        i += 1
    ncx_xml = tostring(ncx, pretty_print=True)
    ncx_xml = '%s\n%s\n%s' % ('<?xml version="1.0" encoding="UTF-8"?>',
                                  '''<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" 
                                  "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">''', ncx_xml)
    with open('%s\\top.ncx' % (root_path),'w') as f:
        f.write(ncx_xml)

