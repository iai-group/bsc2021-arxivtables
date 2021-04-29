__author__ = 'Rebeca Pop'

import json
import argh
from tabulate import tabulate


def display_tables(paper_id = None, table_id = None):
    if not paper_id:
        paper_id = input("Please input the Arxiv paper ID: ")
    try:
        with open("db/arxiv_papers/" + paper_id + ".json", "r") as f:
            paper_dict = json.load(f)

        tables = paper_dict["tables"]
        if not tables:
            print("There are not any tables in the specified paper.")
        else:
            try:
                if not table_id:
                    print("The current paper contains the following tables:")
                    for index in range(len(tables)):
                        caption = "[No caption found]"
                        if "caption" in tables[index] \
                                and tables[index]["caption"]:
                            caption = tables[index]["caption"]
                        print(index, ":", caption)
                    table_id = int(input("Please enter the table ID (0 - " +
                                         str(len(tables) - 1) + "): "))
                else:
                    table_id = int(table_id)
                table = tables[table_id]

                if "caption" in table and table["caption"]:
                    print("Caption:", table["caption"])

                print("Data:")
                print(tabulate(table["rows"], table["headers"]))
            except (IndexError, ValueError):
                print("Please enter a valid table ID.")

    except FileNotFoundError:
        print("The requested paper ID was not found in the database.")


if __name__ == "__main__":
    argh.dispatch_command(display_tables)
