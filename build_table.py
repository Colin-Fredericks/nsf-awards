#!usr/bin/python3

import os
import csv
import json


def BuildTable():
    """
    Gathers year, title, and PI from all json files in all directories.

    Structure:
    {
        "awd_id": number,
        "pi": {
            "pi_role": "Principal Investigator",
            "pi_full_name": string,
        },
    }
    Year comes from the folder name.
    """
    # Get the current working directory
    cwd = os.getcwd()

    data = []

    # walk the directory structure
    for root, dirs, files in os.walk(cwd):
        for file in files:
            if file.endswith(".json"):
                # Get the year from the folder name
                year = os.path.basename(root)
                # Get the full path to the file
                file_path = os.path.join(root, file)
                # Read the json file
                with open(file_path, "r") as f:
                    json_data = json.load(f)
                    # Get the PI name
                    pis = json_data.get("pi", [])
                    pi_priority_list = []

                    if pis:
                        # If there's a single PI, get the name
                        if len(pis) == 1:
                            pi_priority_list.append(pis[0].get("pi_full_name", ""))
                        # If there's a list of PIs, get the first PI with the role "Principal Investigator"
                        if len(pis) > 1:
                            primary = [
                                x
                                for x in pis
                                if x.get("pi_role") == "Principal Investigator"
                            ]
                            pi_priority_list.append(
                                primary[0].get("pi_full_name", "") if primary else ""
                            )
                    else:
                        pi_priority_list.append("")

                    # There are a few possible "no PI" cases:
                    if pi_priority_list[0] == "":
                        # print(file_path)
                        pi_priority_list.append(
                            json_data.get("inst", {}).get("inst_name", "")
                        )
                        pi_priority_list.append(
                            json_data.get("perf_inst", {}).get("perf_inst_name", "")
                        )
                        pi_priority_list.append(json_data.get("org_dir_long_name", ""))
                        pi_priority_list.append(json_data.get("awd_titl_txt", ""))
                        pi_priority_list.append(json_data.get("unavailable"))

                    # Get the first PI name that isn't either empty or "DATA NOT AVAILABLE"
                    for pi in pi_priority_list:
                        if pi and pi != "" and pi != "DATA NOT AVAILABLE":
                            pi_name = pi
                            break

                    # Append the data to the list
                    data.append([year, json_data.get("awd_id", ""), pi_name])
    # Write the data to a csv file
    with open("table.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["year", "award_id", "pi_name"])
        writer.writerows(data)
    print("Table built successfully.")


if __name__ == "__main__":
    BuildTable()
