import yaml

def read_yaml(): 
    path = str(input("Please Enter file path: "))

    try:
        with open(path, 'r') as file:
            yaml_data = yaml.safe_load(file)
        print(yaml_data)

    except FileNotFoundError:
        print("File not Found")

    except yaml.YAMLError as error:
        print("Error: Invalid YAML format.")
        print(error)

read_yaml()