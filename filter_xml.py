import xml.etree.ElementTree as ET

# Recursively traverse the original XML tree and add necessary elements to the filtered XML tree
def add_elements(element, filtered_element, element_name, attribute_name, attribute_value):
    # Check if the element has the specified attribute name and value

    if element_name in element.tag:
       print (f"element:{element.tag} element attrib:{element.attrib}")
       if attribute_name in element.attrib and element.attrib[attribute_name] == attribute_value:
            print (f"Adding element:{element.tag} element attrib:{element.attrib}")
            # Add the element to the filtered XML tree
            filtered_element_copy = ET.Element(element.tag, element.attrib)
            filtered_element_copy.extend(element)
            filtered_element.append(filtered_element_copy)
       else:
            print (f"Skipping element:{element.tag} element attrib:{element.attrib}")
    else:
        for child in element:
            print (f"Adding child:{child.tag} child attrib:{child.attrib}")
            child_filtered_element = ET.Element(child.tag, child.attrib)
            child_filtered_element.extend(child)
            filtered_element.append(child_filtered_element)
            add_elements(child, child_filtered_element, element_name, attribute_name, attribute_value)
            #if len(child_filtered_element) > 0:
            #    filtered_element.append(child_filtered_element)



def recreate_filtered_xml(input_file, element_name, attribute_name, attribute_value, output_file):
    tree = ET.parse(input_file)  # Parse the original XML file
    root = tree.getroot()  # Get the root element

    filtered_root = ET.Element(root.tag)  # Create a new root element for the filtered XML tree

    add_elements(root, filtered_root, element_name, attribute_name, attribute_value)

    filtered_tree = ET.ElementTree(filtered_root)

    # Save the filtered XML tree to the output file
    filtered_tree.write(output_file, encoding="utf-8", xml_declaration=True)

# Usage example
#recreate_filtered_xml("input.xml", "attribute_name", "attribute_value", "output.xml")

if __name__=='__main__':

    input_file = 'input.xml'
    output_file = 'output.xml'
    element_name = 'portfolio'
    attribute_name = 'state'
    attribute_value = 'ny'

    print ("starting ...")
    recreate_filtered_xml(input_file, element_name,  attribute_name, attribute_value, output_file)
    print ("finished ....")