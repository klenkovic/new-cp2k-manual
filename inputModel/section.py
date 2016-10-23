from keyword import Keyword

class Section:

    dataTypeKind = []

    def __init__(self, lxml_element_section):

        self.lxml_element = lxml_element_section

        self.name = self.lxml_element.NAME.text
        self.description = self.lxml_element.DESCRIPTION.text
        self.repeats = True if (self.lxml_element.get("repeats") == "yes") else False

        self._find_ancestors()
        path = ''.join(self.ancestors)
        self.path = path + self.lxml_element.NAME.text
        self.pathHtml = "/CP2K_INPUT/" + self.path + ".html"
        self.dirPath = self.path
        self.fileName = self.name + ".html"

        self.keywords = []
        self.subsections = []
        self.references = []

        for r in self.lxml_element.iterchildren("REFERENCE"):
            ref = {
                "name": r.NAME.text,
                "number": r.NUMBER.text
            }
            self.references.append(ref)

        for s in self.lxml_element.iterchildren("SECTION"):
            sub = {
                "name": s.NAME.text,
                "path": self.path + "/" + s.NAME.text,
                "htmlPath": "/CP2K_INPUT/" + self.path + "/" + s.NAME.text + ".html"
            }
            self.subsections.append(sub)

        # SECTION_PARAMETERS
        if hasattr(self.lxml_element, "SECTION_PARAMETERS"):
            self.keywords.append(Keyword(self.lxml_element.SECTION_PARAMETERS))

        # DEFAULT_KEYWORD
        if hasattr(self.lxml_element, "DEFAULT_KEYWORD"):
            self.keywords.append(Keyword(self.lxml_element.DEFAULT_KEYWORD))

        # OTHER KEYWORDS
        for k in self.lxml_element.iterchildren("KEYWORD"):
            if not k.NAME.text.startswith("__CONTROL"):
                keyword = Keyword(k)
                if keyword.dataType not in Section.dataTypeKind:
                    Section.dataTypeKind.append(keyword.dataType)
                self.keywords.append(keyword)

        self.keywords.sort(key=lambda x: x.name, reverse=False)
        self.subsections.sort(key=lambda x: x['name'], reverse=False)

    def _find_ancestors(self):
        l = []
        n = []
        self.relativePath = "../"
        for p in self.lxml_element.iterancestors("SECTION"):
            nDir = {
                "name": p.NAME.text,
                "path": self.relativePath
            }
            n.append(nDir)
            l.append(p.NAME.text + "/")
            self.relativePath += "../"
        l.reverse()
        n.reverse()
        self.ancestors = l
        self.ancestorsNames = n

    def __check_section_attribs(self):
        section_attributes = []
        for c in self.lxml_element.iterchildren():
            if c.tag not in section_attributes:
                section_attributes.append([c.tag, c.attrib])
        return section_attributes

    def dump(self):
        print("Section name: {}").format(self.name)
        print("Section repeats? {}").format(self.repeats)
        print("Section path: {}").format(self.path)
        print("Section HTML path: {}").format(self.pathHtml)
        print("Subsections:")
        print(self.subsections)
        print("References:")
        print(self.references)
        print("Keywords:")
        for k in self.keywords:
            k.dump()
