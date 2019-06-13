from lxml.etree import Element, SubElement, tostring


def top_html(root_path, book_name, top_info, isMulti):
    html = Element('html', attrib={'xmlns': 'http://www.w3.org/1999/xhtml'})
    head = SubElement(html, 'head')
    SubElement(head, 'title').text = 'TOC'
    SubElement(head, 'link', attrib={'type': 'text/css', 'href': 'style.css', 'rel': 'Stylesheet'})
    body = SubElement(html, 'body')
    SubElement(body, 'h1', attrib={'id': 'toc'}).text = book_name
    if isMulti:
        ul = SubElement(body, 'ul')
        for top in top_info:
            li = SubElement(ul, 'li')
            SubElement(li, 'a', attrib={'href': top['book_url']}).text = top['book_title']
            child_ul = SubElement(li, 'ul')
            for child_top in top['child_tops']:
                SubElement(SubElement(child_ul, 'li'), 'a', attrib={'href': child_top['chap_url']}).text = child_top[
                    'chap_title']
    else:
        ul = SubElement(body, 'ul')
        for top in top_info:
            SubElement(SubElement(ul, 'li'), 'a', attrib={'href': top['chap_url']}).text = top['chap_title']

    top_html = tostring(html, pretty_print=True)
    top_html = '%s\n%s' % ('<!DOCTYPE html>', top_html.decode('utf-8'))
    with open('%s\\toc.html' % (root_path), 'w') as f:
        f.write(top_html)
