import json
from tabulate import tabulate


if __name__ == "__main__":

    paper_id = input("Please input the Arxiv paper ID: ")
    f = None

    try:
        f = open("db/arxiv_papers/" + paper_id + ".json", "r")
        paper_dict = json.load(f)
        f.close()

        tables = paper_dict["tables"]
        if not tables:
            print("There are not any tables in the specified paper.")
        else:
            try:
                table_id = int(input("Please enter the table ID (0 to " + str(len(tables) - 1) + "): "))
                table = tables[table_id]

                if "caption" in table and table["caption"]:
                    print("Caption:", table["caption"])

                print("Data:")
                print(tabulate(table["rows"], table["headers"]))
            except (IndexError, ValueError):
                print("Please enter a valid table ID.")

    except FileNotFoundError:
        print("The requested paper id was not found in our database.")
    finally:
        if f and not f.closed:
            f.close()
