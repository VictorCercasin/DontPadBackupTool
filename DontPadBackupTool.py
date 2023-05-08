import requests
import json
import os
import sys
import argparse

def make_dir(path):
    if not os.path.exists(f"{path}"):
        os.makedirs(f"{path}")  
    return 

def store(path, file_name, data):
    # if not os.path.exists(f'{path}/{file_name}'):
    #     os.makedirs(f'{path}/{file_name}')
    with open(f"{path}/{file_name}.txt", 'w', encoding='utf-8') as f:
        f.write(str(data))
    return
        
def get_dontpad_subpath_data(dontpad_subpath, local_subpath, subpath_name):
    dontpad_subpath = f"{dontpad_subpath}/{subpath_name}"
    local_subpath = f"{local_subpath}/{subpath_name}"

    #make local directory for current subpath
    make_dir(local_subpath)

    #get subfolder structure (hub_list)
    response = requests.get(f"https://api.{dontpad_subpath}.menu.json")
    hub_list = response.json()

    #get data from current dontpad document (document_data)
    response = requests.get(f"https://api.{dontpad_subpath}.body.json?lastModified=0")
    document_data = json.loads(response.content.decode('utf-8'))["body"]

    #store data into f"{current_subpath}/{subpath_name}.txt"
    store (local_subpath, subpath_name, document_data)
    
    #for each in hub_list, do get_dontpad_subpath_data(item)
    for subpath in hub_list:
        get_dontpad_subpath_data(dontpad_subpath, local_subpath, subpath)
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="subpath for dontpad web page ('-i exemple' for dontpad.com/example)")
    parser.add_argument("-o", "--output", help="subpath for storing backed up data. (default current directory)")
    args = parser.parse_args()

    if not args.input:
        print("Please set argument -i with the subpath for dontpad web page ('-i exemple' for dontpad.com/example)")
        return

    local_subpath = f"." #default directory for output is working directory
    if args.output:
        local_subpath = args.output

    dontpad_subpath = f"dontpad.com"

    get_dontpad_subpath_data(dontpad_subpath, local_subpath, args.input) 
    return


if __name__ == '__main__':
    main()