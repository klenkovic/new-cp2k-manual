class CP2Kinput:
    def __init__(self, version, year, compile_date, compile_revision):
        self.version = version
        self.year = year
        self.compileDate = compile_date
        self.compileRevision = compile_revision

    @staticmethod
    def __check_input_attribs(lxml_root):
        root_attributes = []
        for c in lxml_root.iterchildren():
            if c.tag not in root_attributes:
                root_attributes.append(c.tag)
        return root_attributes
