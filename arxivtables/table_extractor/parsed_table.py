import json


class ParsedTable:

    def __init__(self, table_dict : dict):
        self.__caption = table_dict["caption"]
        self.__headings = table_dict["headings"]
        self.__data = table_dict["data"]


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
        table_dict = dict()
        table_dict["metadata"] = dict()
        table_dict["metadata"]["caption"] = self.caption
        table_dict["headings"] = self.headings
        table_dict["data"] = self.data
        return json.dumps(table_dict, indent=4)
