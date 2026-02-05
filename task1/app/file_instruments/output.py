import json
import xml.etree.ElementTree as ET
from datetime import datetime
from xml.dom import minidom


class OutputHandler:

    @staticmethod
    def display(data, format):
        if data is None or format is None:
            return

        if format == "json":
            print("json format")

            filename = f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
            return f"Data saved to {filename}"

        elif format == "xml":
            print("xml format")

            if not isinstance(data, list):
                return f"Console Message: {data}"

            # 1. Create the root element
            root = ET.Element("QueryResult")

            # 2. Iterate through each row (now a dictionary)
            for row_dict in data:
                row_element = ET.SubElement(root, "Row")

                # 3. Create a tag for every column name
                for column_name, value in row_dict.items():
                    # Clean column name (replace spaces with underscores if they exist)
                    tag_name = str(column_name).replace(" ", "_")
                    child = ET.SubElement(row_element, tag_name)
                    child.text = str(value)

            # 4. Pretty-print formatting
            xml_string = ET.tostring(root, encoding="utf-8")
            pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="  ")

            # 5. Save to file
            filename = f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(pretty_xml)

            return f"Data saved successfully to {filename}"

        elif format == "console":

            if isinstance(data, list):
                print("\n--- QUERY RESULTS ---")
                for row in data:
                    print(row)
                print("---------------------\n")
            else:
                print(data)
