__author__ = 'David Ramsay'
__maintainer__ = 'Rebeca Pop, David Ramsay'


class ParsedTable:

    def __init__(self, caption : str, headings, data):
        self.__caption = caption
        self.__headings = headings
        self.__data = data


    @property
    def caption(self):
        return self.__caption

    @property
    def headings(self):
        return self.__headings

    @property
    def data(self):
        return self.__data

    def toJSON(self) -> str:
        table_dict = {
            "caption": self.caption,
            "headers": self.headings,
            "rows": self.data
        }
        return table_dict


