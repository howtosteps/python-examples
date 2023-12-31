import xml.etree.ElementTree as ET

#filter xml file by attribute key and value. Result is written to output file that only contains elements with the specified attribute key and value along with parents and child nodes
def filter_xmlfile(input_file, output_file, attribute_name, attribute_value):
    tree = ET.parse(input_file)
    root = tree.getroot()
    filtered_elements = []

    # Find the filtered elements based on attribute key and value
    for element in root.iter():
        if attribute_name in element.attrib and element.attrib[attribute_name] == attribute_value:
            filtered_elements.append(element)

    filtered_root = ET.Element(root.tag)

    #Add all the parent hierarchy of the filtered elements to the filtered root
    for element in filtered_elements:
        # get the parent of the element
        parent = element.find("..")
        attrib_id="id"
        parent_id="id"
        
        while parent is not None:
            if parent not in filtered_root:
                filtered_root.append(parent)
            parent = parent.find("..")
            
        if parent is not None:
            print (f"element:{element.tag} element attrib:{element.attrib[attrib_id]} parent:{parent.tag} parent attrib:{parent.attrib[parent_id]}")
        else:
            print (f"element:{element.tag} element attrib:{element.attrib[attrib_id]} parent:{parent}")


    # Now add all the elements to the filtered root
    for element in filtered_elements:
        if element not in filtered_root:
            filtered_root.append(element)


    filtered_tree = ET.ElementTree(filtered_root)

    #Now write the filtered root to the output file
    filtered_tree.write(output_file)


if __name__=='__main__':

    input_file = 'input.xml'
    output_file = 'output.xml'
    attribute_name = 'state'
    attribute_value = 'ny'

    print ("starting ...")
    filter_xmlfile(input_file, output_file, attribute_name, attribute_value)
    print ("finished ....")