from lxml.etree import Element, SubElement, tostring


def content_html(root_path, url, chap_list):
    html = Element('html', attrib={'xmlns': 'http://www.w3.org/1999/xhtml'})
    head = SubElement(html, 'head')
    SubElement(head, 'title').text = 'TOC'
    SubElement(head, 'link', attrib={'type': 'text/css', 'href': 'style.css', 'rel': 'Stylesheet'})
    body = SubElement(html, 'body')
    i = 1
    for chap in chap_list:
        SubElement(body, 'h2', attrib={'id': str(i)}).text = chap['chap_name']
        for content in chap['content']:
            SubElement(body, 'p').text = content
        SubElement(body, 'div', attrib={'class': 'pagebreak'})
        i += 1
    top_html = tostring(html, pretty_print=True)
    top_html = '%s\n%s' % ('<!DOCTYPE html>', top_html)
    with open('%s\\%s.html' % (root_path, url), 'w') as f:
        f.write(top_html)
