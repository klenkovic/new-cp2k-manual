class Keyword:
    def __init__(self, lxml_element_keyword):
        self.lxml_element = lxml_element_keyword

        self.aliases = []

        for n in self.lxml_element.iterchildren("NAME"):
            if n.get("type") == "default":
                self.name = n.text
            else:
                self.aliases.append(n.text)

        self.name = self.lxml_element.NAME.text
        self.repeats = True if (self.lxml_element.get("repeats") == "yes") else False
        self.nameType = self.lxml_element.NAME.get("type")
        self.description = self.lxml_element.DESCRIPTION.text

        self.dataType = self.lxml_element.DATA_TYPE.get("kind")
        self.n_var = int(self.lxml_element.DATA_TYPE.N_VAR.text)
        self.defaultValue = self.lxml_element.DEFAULT_VALUE.text if hasattr(self.lxml_element, "DEFAULT_VALUE") else ""
        self.defaultUnit = self.lxml_element.DEFAULT_UNIT.text if hasattr(self.lxml_element, "DEFAULT_UNIT") else ""
        self.usage = self.lxml_element.USAGE.text

        self.references = []
        self.loneKeywordValue = None
        self.enumeration = []

        if hasattr(self.lxml_element, "LONE_KEYWORD_VALUE"):
            self.loneKeywordValue = self.lxml_element.LONE_KEYWORD_VALUE.text

        if hasattr(self.lxml_element, "REFERENCE"):
            for r in self.lxml_element.iterchildren("REFERENCE"):
                ref = {
                    "name": r.NAME.text,
                    "number": r.NUMBER.text
                }
                self.references.append(ref)

        if self.dataType == "keyword":
            for i in self.lxml_element.DATA_TYPE.ENUMERATION.iterchildren("ITEM"):
                item = {
                    "name": i.NAME.text,
                    "description": i.DESCRIPTION.text
                }
                self.enumeration.append(item)

        self.enumeration.sort(key=lambda x: x['name'], reverse=False)


    def __check_keyword_attribs(self):
        keyword_attributes = []
        for c in self.lxml_element.iterchildren():
            if c.tag not in keyword_attributes:
                keyword_attributes.append([c.tag, c.attrib])
        return keyword_attributes

    def dump(self):
        print(" |-----------------------------------------------")
        print(" | Keyword name: {}").format(self.name)
        print(" | Keyword repeats? {}").format(self.repeats)
        print(" | Keyword nametype: {}").format(self.nameType)
        print(" | Keyword datatype: {}").format(self.dataType)
        print(" | Keyword nVar: {}").format(self.n_var)
        print(" | Keyword defaultValue: {}").format(self.defaultValue)
        print(" | Keyword enumeration:")
        print(self.enumeration)
        print(" | Keyword references:")
        print(self.references)
