import json

def save_formulas_to_json(formulas):
    """
    Saves a list of formulas to a JSON file.

    This function takes a list of formulas, constructs a list of dictionaries
    representing each formula with a unique primary key, and saves it to a JSON
    file named 'sample.json' in the '../fixtures/' directory. Each dictionary
    contains the model name, primary key, and fields with the formula's name and
    text. A success message is printed upon completion.

    Args:
        formulas (list): A list of formula strings to be saved.
    """
    filename = 'sample.json'
    data_to_save = [{"model": "editor.Formula", "pk" : index + 1, "fields" : {"name": index + 1, "formula_text": formula}} for index, formula in enumerate(formulas)]
    with open(f'../fixtures/{filename}', 'w') as json_file:
        json.dump(data_to_save, json_file)
    print(f"List saved to {filename} successfully.")