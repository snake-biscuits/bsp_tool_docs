import markdown
from lxml import etree


def markdown_as_element(md_filename: str) -> etree.Element:
    with open(md_filename) as md_file:
        md_text = markdown.markdown(md_file.read())
    return etree.fromstring(md_text)


def compose(head: etree.Element, nav: etree.Element, content: etree.Element) -> etree.Element
    # NOTE: head should import css
    root = etree.Element("html")
    root.append(head)
    body = etree.SubElement(root, "body")
    # TODO: nav & content grid nodes
    body.append(content)
    return root
