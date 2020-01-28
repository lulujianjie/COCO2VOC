DIFFICULT = '0'
TRUNCATED = '0'
POSE = 'Unspecified'


def create_element_node(doc, tag, attr):
    element_node = doc.createElement(tag)
    text_node = doc.createTextNode(attr)
    element_node.appendChild(text_node)
    return element_node


def create_child_node(doc, tag, attr, parent_node):
    child_node = create_element_node(doc, tag, attr)
    parent_node.appendChild(child_node)


def create_object_node(doc, attrs):
    object_node = doc.createElement('object')
    create_child_node(doc, 'name', attrs['name'], object_node)
    create_child_node(doc, 'pose', POSE, object_node)
    create_child_node(doc, 'truncated', TRUNCATED, object_node)
    create_child_node(doc, 'difficult', DIFFICULT, object_node)
    bndbox_node = doc.createElement('bndbox')
    create_child_node(doc, 'xmin', str(int(attrs['bndbox'][0])), bndbox_node)
    create_child_node(doc, 'ymin', str(int(attrs['bndbox'][1])), bndbox_node)
    create_child_node(doc, 'xmax', str(int(attrs['bndbox'][0] + attrs['bndbox'][2])), bndbox_node)
    create_child_node(doc, 'ymax', str(int(attrs['bndbox'][1] + attrs['bndbox'][3])), bndbox_node)
    object_node.appendChild(bndbox_node)
    return object_node


def write_xml_file(doc, filename):
    tmpfile = open('tmp.xml', 'w')
    doc.writexml(tmpfile, addindent='' * 4, newl='\n', encoding='utf-8')
    tmpfile.close()
    fin = open('tmp.xml')
    fout = open(filename, 'w')
    lines = fin.readlines()
    for line in lines[1:]:
        if line.split():
            fout.writelines(line)
    fin.close()
    fout.close()
