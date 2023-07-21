import xml.etree.ElementTree as ET
import copy

def set_delete_elements(input_file, element_name, attribute_name, attribute_value, output_file):
    # Parse the original XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Create a deep copy of the root element
    filtered_root = copy.deepcopy(root)

    # Find and delete the elements with the specified element name, attribute name, and value
    for element in filtered_root.iter(element_name):
        print (f"element:{element.tag} element attrib:{element.attrib} element text:{element.text}")
        if attribute_name in element.attrib and element.attrib[attribute_name] != attribute_value:
            print ("++Deleting")
            element.set('deleted', 'yes')
        else:
            print ("--Skipping")


    # Save
    #  the modified XML tree to the output file
    filtered_tree = ET.ElementTree(filtered_root)
    filtered_tree.write(output_file, encoding="utf-8", xml_declaration=True)

def build_parent_mapping(element, parent=None):
    mapping = {element: parent}
    for child in element:
        mapping.update(build_parent_mapping(child, element))
    return mapping

# Recursively print the XML tree
def print_element(element):
    for child in element:
        print (f"child:{child.tag} child attrib:{child.attrib} child text:{child.text}")
        print_element(child)

def recreate_outputfile(output_file):
    # parse the output file and remove nodes with deleted attribute set to yes
    tree = ET.parse(output_file)
    root = tree.getroot()

    # Build a mapping of element to parent element
    parent_map = build_parent_mapping(root)

    # Get all elements without the  deleted attribute set to yes
    # and recreate the output file
    for element in root.findall(".//*[@deleted='yes']"):
        print (f"deleting element:{element.tag} element attrib:{element.attrib} element text:{element.text}")
        parent = parent_map[element]
        element.set('deleted', 'yes')
        if parent is not None:
            parent.remove(element)

    # Save the modified XML tree to the output file
    filtered_tree = ET.ElementTree(root)
    filtered_tree.write(output_file, encoding="utf-8", xml_declaration=True)


if __name__=='__main__':
    input_file = 'input.xml'
    output_file = 'output.xml'
    element_name = 'security'
    attribute_name = 'primarid'
    attribute_value = 'FN 3.0'

    print ("finished ....")

    print ("starting ...")
    set_delete_elements(input_file, element_name, attribute_name, attribute_value, output_file)
    recreate_outputfile(output_file)
