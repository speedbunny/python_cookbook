from lxml import etree
from pandas.io.parsers import LongestRepeatedPrefixMatcher
from collections import namedtuple
import re

class XML2DataFrame(object):

    def __init__(self, xml_data):
        self.root = etree.XML(xml_data)

    @staticmethod
    def _check_valid_element(element):
        """Check for valid element."""
        if element.text is None and len(element) == 0:
            return False
        else:
            return True

    def parse_root(self, root=None):
        """Parse the root elements"""
        if root is None:
            root = self.root
        return [self._parse_element(child) for child in iter(root)]

    def _parse_element(self, element, parsed=None, parent=None):
        """ Parse each element recursively and check for list of elements to avoid empty dataframes"""
        if parsed is None:
            parsed = dict()
        # If current node has a text then add it to dictionary as attribute
        if element.text:
            parsed[element.tag] = element.text
        # Iterate over children and go into recursive call
        for child in list(element):
            # Check whether this tag already exists or not
            if child.tag in parsed:
                # If yes, then convert that tag value into array so that it can hold multiple values
                if not isinstance(parsed[child.tag], list):
                    parsed[child.tag] = [parsed[child.tag]]
                # Append new value to existing array/list
                parsed[child.tag].append(self._parse_element(child))
            else:
                parsed[child.tag] = self._parse_element(child)
        return parsed

    def process_data(self):
        """Parse the root element and return list of dictionaries."""
        structure_data = self.parse_root()

        # If this is a feed then all data is in 'entry' tag, so filter those entries only
        if self.root.tag == "feed":
            structure_data = [x["entry"] for x in structure_data]

        # Flatten dictionary into individual arrays/lists to be converted into column headers later on
        flattened_structure = []
        for i in range(0, len(structure_data)):
            temp = {}
            for k, v in structure_data[i].items():
                if isinstance(v, list):
                    temp[k] = None
                    # Check whether any item of given array has value or not
                    if len([item for item in v if XML2DataFrame._check_valid_element(item)]) > 0:
                        temp[k] = v
                elif v is not None:
                    temp[k] = v
            flattened_structure.append(temp)
        return flattened_structure

class Dict2DataFrame(object):

    @staticmethod
    def _lstrip_colnames(df):
        """Strip left spaces from column names"""
        df.columns = map(str.lstrip, df.columns)
        return df

    def convert(self, dic):
        """Convert nested dictionary into pandas dataframe."""
        # Iterate over all keys of dictionary and create attributes named same as that key
        # Then assign values to those attribute dynamically (this will help us to easily convert dictionary into dataframe)
        container = namedtuple("Container", dic.keys())
        # Create an object with attribute name and value pair
        row = container(*(dic[key] for key in container._fields))
        # Convert tuple into dataframe and transpose it to get rows as columns
        df = pd.DataFrame([row._asdict()]).T
        # Strip left spaces from column names for consistent behaviour across most of the feeds
        df = Dict2DataFrame._lstrip_colnames(df)
        return df

def parse_XML(xml_file, xml_attribs=None):
    """Parses an xml file and stores in a list of dictionaries."""
    xtree = etree.parse(xml_file)
    xroot = xtree.getroot()
    rows = []

    # Get root element's children tags
    nodes = list(xroot)
    # Iterate through each tag and collect attrib information
    for node in nodes:
        res = {}
        # Check if tag has attributes
        if xml_attribs is None:
            res = {child.tag: child.text for child in list(node)}
        else:
            for attr in node.attrib.keys():
                # If tag has specified attribute then get the data out of that attribute and add it as column to our dataframe
                if attr in xml_attribs:
                    res[attr] = node.attrib.get(attr)

        # Iterate through each child tag and collect values
        children = list(node)
        for child in children:
            # Check whether current tag contains list of elements or not
            if len(list(child)) > 1:
                # If this is a list of items, then create a new dictionary called 'items'
                # And insert all child tags inside it
                temp = {}
                for item in list(child):
                    try:
                        temp[item.tag].append(item.text)
                    except KeyError:
                        temp[item.tag] = [item.text]
                res[child.tag] = pd.DataFrame(temp)
            else:
                # Else just simply store the text value of that tag into parent dictionary
                res[child.tag] = child.text

        rows.append(res)

    return rows

def parse_XML2DF(xml_file):
    """Parses an XML file and stores in a pandas DataFrame."""
    xtree = etree.parse(xml_file)
    xroot = xtree.getroot()

    parser = LongestRepeatedPrefixMatcher()
    parser.feed(etree.tostring(xroot))
    matcher = parser.close()
    lst = []

    for _, elem in etree.iterparse(xml_file, events=('end',), tag=(matcher.element,)):
        dic = {}
        for e in elem.iterchildren():
            if e.tag == matcher.namespace + "link":
                continue
            if e.text is None:
                dic[e.tag] = np.nan
            elif re.match("^\d+?\.\d+?$", e.text) is not None:
                dic[e.tag] = float(e.text)
            elif re.match("^\d+?$", e.text) is not None:
                dic[e.tag] = int(e.text)
            else:
                dic[e.tag] = e.text
        lst.append(dic)
        elem.clear()
    return pd.DataFrame(lst)

def flatten_XML(nested_xml):
    """Converts nested XML into a tabular format."""
    flattened = []

    for sublist in nested_xml:
        for k, v in sublist.items():
            temp = {'parent': k}
            try:
                if isinstance(v[0], collections.OrderedDict):
                    child = v[0]
                    for key, val in child.items():
                        temp[key] = val
                else:
                    temp['value'] = v
            except (IndexError, TypeError):
                temp['value'] = v
            flattened.append(temp)

    return pd.DataFrame(flattened)

def xml2df(xml_data):
    """Parses an XML file or string."""
    if not isinstance(xml_data, str):
        with open (xml_data, 'rb') as f:
            return xmltodict.parse(f)

    return xmltodict.parse(xml_data)

if __name__ == "__main__":
    # Use parse function to load needed data into a list of dictionaries
    rows = parse_XML('sample.xml', ['id'])
    print("Rows parsed from sample.xml: ", len(rows))
    print("First row: ", rows[0])
    df = parse_XML2DF('sample.xml')
    flattened_xml = flatten_XML(rows)
    print(flattened_xml)

    # Use xml2df function to load needed data into a DataFrame
    rows = xml2df('sample.xml')['feed']['entry']
    flattened_xml = flatten_XML(rows)
    print(flattened_xml)

    # Use XML2DataFrame class to convert nested xml into dataframe
    xml2df = XML2DataFrame(xml_data)
    xml_dataframe = pd.DataFrame(xml2df.process_data())

    # Use Dict2DataFrame class to convert dictionary into dataframe
    dic2df = Dict2DataFrame()
    for i in range(0, len(xml_dataframe)):
        print("Converting row ", i + 1)
        df = dic2df.convert(xml_dataframe.loc[i])
        if i == 0:
            final_df = df
        else:
            final_df = final_df.append(df)
    print(final_df)
