import json
import os
from datetime import date

profiles_dir_path = "C:/Users/Anthony/documents/MarkProject/profiles/"


def create_profile_json(profile_name, account_names):
    file_name = profile_name + ".json"
    data = {"Profile": profile_name}
    creation_date = date.today().strftime("%m/%d/%y")
    data["Creation Date"] = creation_date
    data["Rolling Total"] = 0
    data["Current Mark"] = 0
    data["Accounts"] = {}
    data["Entries"] = {}
    for x in account_names:
        data["Accounts"][x] = \
                {
                    "Current Mark": 0,
                    "Total Entries": 0,
                    "Entries": {}
                }
    path_name = os.path.join(profiles_dir_path + file_name)
    with open(path_name, "w") as write_file:
        json.dump(data, write_file)
        write_file.close()
        print(f"create_json({profile_name}, {account_names}) -> File saved successfully")
    return


def save_json(file_name, data):
    path_name = os.path.join(profiles_dir_path + file_name + ".json")
    with open(path_name, "w") as write_file:
        json.dump(data, write_file)
        write_file.close()
        print(f"save_json({path_name}, data) -> File saved successfully")
    return


def delete_json(file_name):
    path_name = os.path.join(profiles_dir_path + file_name + ".json")
    if os.path.isfile(path_name):
        os.remove(path_name)
        print(f"delete_file({path_name}) -> File deleted successfully!")
    else:
        print(f"delete_file({path_name}) -> Error -> File not found!")
    return


def decode_json(profile_name):
    path_name = os.path.join(profiles_dir_path + profile_name)
    if os.path.isfile(path_name):
        with open(path_name, "r") as read_file:
            data = json.load(read_file)
            read_file.close()
            print(f"decode_json({path_name}) -> File Found! -> File loaded to dictionary")
        return data
    else:
        print(f"decode_file({path_name}) -> File not found!")
        return -1


def get_profiles():
    if os.path.lexists(profiles_dir_path):
        print(f"get_profiles() -> Directory Found -> Directory loaded to list")
        files = os.listdir(profiles_dir_path)
        return files
    print(f"get_profiles() -> Directory not found")
    return -1
