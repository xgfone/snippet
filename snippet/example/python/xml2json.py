import json

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def strip_tag(tag):
    strip_ns_tag = tag
    split_array = tag.split('}')
    if len(split_array) > 1:
        strip_ns_tag = split_array[1]
        tag = strip_ns_tag
    return tag


def elem_to_internal(elem, strip_ns=1, strip=1):
    """Convert an Element into an internal dictionary (not JSON!)."""

    d = {}
    elem_tag = elem.tag
    if strip_ns:
        elem_tag = strip_tag(elem.tag)
    else:
        for key, value in list(elem.attrib.items()):
            d['@' + key] = value

    # loop over subelements to merge them
    for subelem in elem:
        v = elem_to_internal(subelem, strip_ns=strip_ns, strip=strip)

        tag = subelem.tag
        if strip_ns:
            tag = strip_tag(subelem.tag)

        value = v[tag]

        try:
            # add to existing list for this tag
            d[tag].append(value)
        except AttributeError:
            # turn existing entry into a list
            d[tag] = [d[tag], value]
        except KeyError:
            # add a new non-list entry
            d[tag] = value
    text = elem.text
    tail = elem.tail
    if strip:
        # ignore leading and trailing whitespace
        if text:
            text = text.strip()
        if tail:
            tail = tail.strip()

    if tail:
        d['#tail'] = tail

    if d:
        # use #text element if other attributes exist
        if text:
            d["#text"] = text
    else:
        # text is the value if no attributes
        d = text or None
    return {elem_tag: d}


def internal_to_elem(pfsh, factory=ET.Element):
    """Convert an internal dictionary (not JSON!) into an Element.

    Whatever Element implementation we could import will be
    used by default; if you want to use something else, pass the
    Element class as the factory parameter.
    """

    attribs = {}
    text = None
    tail = None
    sublist = []
    tag = list(pfsh.keys())
    if len(tag) != 1:
        raise ValueError("Illegal structure with multiple tags: %s" % tag)
    tag = tag[0]
    value = pfsh[tag]
    if isinstance(value, dict):
        for k, v in list(value.items()):
            if k[:1] == "@":
                attribs[k[1:]] = v
            elif k == "#text":
                text = v
            elif k == "#tail":
                tail = v
            elif isinstance(v, list):
                for v2 in v:
                    sublist.append(internal_to_elem({k: v2}, factory=factory))
            else:
                sublist.append(internal_to_elem({k: v}, factory=factory))
    else:
        text = value
    e = factory(tag, attribs)
    for sub in sublist:
        e.append(sub)
    e.text = text
    e.tail = tail
    return e


def elem2json(elem, pretty=False, strip_ns=1, strip=1):
    """Convert an ElementTree or Element into a JSON string."""

    if hasattr(elem, 'getroot'):
        elem = elem.getroot()

    if pretty:
        return json.dumps(elem_to_internal(elem, strip_ns=strip_ns, strip=strip),
                          sort_keys=True, indent=4, separators=(',', ': '))
    return json.dumps(elem_to_internal(elem, strip_ns=strip_ns, strip=strip))


def json2elem(json_data, factory=ET.Element):
    """Convert a JSON string into an Element.

    Whatever Element implementation we could import will be used by
    default; if you want to use something else, pass the Element class
    as the factory parameter.
    """

    return internal_to_elem(json.loads(json_data), factory)


def xml2json(xmlstring, pretty=False, strip_ns=1, strip=1):
    """Convert an XML string into a JSON string."""

    elem = ET.fromstring(xmlstring)
    return elem2json(elem, pretty, strip_ns=strip_ns, strip=strip)


def json2xml(json_data, factory=ET.Element):
    """Convert a JSON string into an XML string.

    Whatever Element implementation we could import will be used by
    default; if you want to use something else, pass the Element class
    as the factory parameter.
    """
    if not isinstance(json_data, dict):
        json_data = json.loads(json_data)

    elem = internal_to_elem(json_data, factory)
    return ET.tostring(elem)


def xml2dict(xmlstring, strip_ns=1, strip=1):
    elem = ET.fromstring(xmlstring)
    if hasattr(elem, 'getroot'):
        elem = elem.getroot()
    return elem_to_internal(elem, strip_ns=strip_ns, strip=strip)


def dict2xml(dict_data, factory=ET.Element):
    elem = internal_to_elem(dict_data, factory)
    return ET.tostring(elem)
