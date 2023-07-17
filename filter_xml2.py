import xml.etree.ElementTree as ET

# Recursively traverse the original XML tree and add necessary elements to the filtered XML tree
def add_elements(element, filtered_element, element_name, attribute_name, attribute_value):
    #bool_tag_found = False

    for child in element:
        print (f"child:{child.tag} child attrib:{child.attrib} child text:{child.text}")

        # Recursively call this function for each child element
        if child.tag==element_name:
            #bool_tag_found = True
            # Check if the element has the specified attribute name and value
            if attribute_name in child.attrib and child.attrib[attribute_name] == attribute_value:
                print ("++Adding")
                # Add the element to the filtered XML tree
                filtered_element_copy = ET.Element(child.tag, child.attrib)
                filtered_element_copy.text = child.text  # Include child text
                filtered_element_copy.extend(child)
                filtered_element.append(filtered_element_copy)
            else:
                print ("--Skipping")
        else:
            # Add the child element to the filtered XML tree
            child_element = ET.Element(child.tag, child.attrib)
            child_element.text = child.text  # Include child text
            #child_element.extend(child)
            filtered_element.append(child_element)

            #if len(child_element) > 0:
            #    filtered_element.append(child_element)
            add_elements(child, filtered_element, element_name, attribute_name, attribute_value)

# Recursively print the XML tree
def print_element(element):
    for child in element:
        print (f"child:{child.tag} child attrib:{child.attrib} child text:{child.text}")
        print_element(child)


# Recreate the filtered XML tree
def recreate_filtered_xml(input_file, element_name, attribute_name, attribute_value, output_file):
    tree = ET.parse(input_file)  # Parse the original XML file
    root = tree.getroot()  # Get the root element

    filtered_root = ET.Element(root.tag)  # Create a new root element for the filtered XML tree

    add_elements(root, filtered_root, element_name, attribute_name, attribute_value)
    #print("print root:")
    #print_element(root)

    #print("print filtered root:")
    #print_element(filtered_root)

    filtered_tree = ET.ElementTree(filtered_root)

    # Save the filtered XML tree to the output file
    filtered_tree.write(output_file, encoding="utf-8", xml_declaration=True)


if __name__=='__main__':
    input_file = 'input.xml'
    output_file = 'output.xml'
    element_name = 'security'
    attribute_name = 'primarid'
    attribute_value = 'FN 1.0'

    print ("starting ...")
    recreate_filtered_xml(input_file, element_name, attribute_name, attribute_value, output_file)
    print ("finished ....")