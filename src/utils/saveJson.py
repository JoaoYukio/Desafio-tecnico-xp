import json


def load_uploaded_files():
    try:
        with open("./data/pdf_files/uploaded_files.json", "r") as f:
            data = f.read()
            if not data:
                return []
            return json.loads(data)
    except FileNotFoundError:
        return []


def save_uploaded_files(files_list):
    #! O path precisa ser em relação ao arquivo que está sendo executado
    with open("./data/pdf_files/uploaded_files.json", "w") as f:
        json.dump(files_list, f)
