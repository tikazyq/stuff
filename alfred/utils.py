import alfred


def _render(items):
    """
    Render a sequence of Alfred items into a complete XML document.
    """
    root = alfred.E.items(*[item.element() for item in items])
    return alfred.et.tostring(root, pretty_print=True, xml_declaration=True, encoding='utf-8')