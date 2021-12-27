import os
import argparse
import json


def add_variable(variable_dict: dict) -> dict:
    variable_name = input(
        "What is the standardized name of the variable?\n"
    )
    other_names = input(
        "Does the variable have other names? Separate input by commas. e.g. water, h2o, liquid ice\n"
    )
    other_names = other_names.split(',')
    other_names = [name.strip() for name in other_names]
    i_or_o = input(
        "Is this variable an input or output variable? (input/output)\n"
    )
    include = input(
        "Should this variable be included in the training dataset? (y/n)\n"
    )
    label = input(
        "What is the description of this variable?\n"
    )
    unique = input(
        "Should the variable be unique per subject? (y/n)\n"
    )
    numeric_or_factor = input(
        "Is the variable numeric or a factor? (numeric/factor)\n"
    )
    if numeric_or_factor == 'numeric':
        unit = input("What is the unit of the variable? (e.g. grams)\n"
                     )
        quantile_min = 0.0005
        quantile_max = 0.9995
        value_min = input(
            "What is the minimum value this variable can take on? (n/a if no lower bound)\n"
        )
        value_max = input(
            "What is the maximum value this variable can take on? (n/a if no upper bound)\n"
        )
        forward_impute = 0
        backward_impute = 0
        info_dict = {
            'unit': unit,
            'cutoff': {
                'quantile_min': quantile_min,
                'quantile_max': quantile_max,
                'value_min': value_min,
                'value_max': value_max,
            },
            'impute_per_sbj': {
                'forward': forward_impute,
                'backward': backward_impute
            }
        }
    elif numeric_or_factor == 'factor':
        levels = input(
            "What categories can this variable take on? Separate input with commas. (e.g. cat, dog, mouse)\n"
        )
        levels = levels.split(',')
        levels = [level.strip() for level in levels]
        info_dict = {
            'levels': {
                level: [level.lower(), level.capitalize(), i] for i, level in enumerate(levels)
            }
        }

    if include == "y":
        include = True
    elif include == "n":
        include = False

    if unique == "y":
        unique = True
    elif include == "n":
        unique = False

    if value_min == "n/a":
        value_min = None 
    if value_max == "n/a":
        value_max = None

    internal_dict = {
        i_or_o: include,
        'src_names': other_names,
        'label': label,
        'unique_per_sbj': unique,
        numeric_or_factor: info_dict,
    }

    print(internal_dict)

    variable_dict[variable_name] = internal_dict

    return variable_dict


def remove_variable(variable_dict: dict):
    variable_name = input(
        "What is the name of the variable to remove?\n"
    )
    variable_dict.pop(variable_name)
    return variable_dict


if __name__ == "__main__":
    os.chdir('../../')

    project_dir = input(
        "Project directory name (e.g. project1_hourly): "
    )
    project_dir = os.path.normpath(project_dir)

    if not os.path.exists(project_dir):
        raise FileNotFoundError('Project directory not found.')

    metadata_dir = os.path.join(project_dir, 'metadata')
    variable_dict_path = os.path.join(metadata_dir, 'variable_dict.json')

    with open(variable_dict_path) as variable_dict_json:
        variable_dict = json.load(variable_dict_json)

    while True:
        add_or_remove = input(
            "Would you like to `add` or `remove` variables from the dictionary? (input quit to end session)\n"
        )
        if add_or_remove == 'add':
            variable_dict = add_variable(variable_dict)
        elif add_or_remove == 'remove':
            variable_dict = remove_variable(variable_dict)
        elif add_or_remove == 'quit':
            break
        else:
            print("Input must be either `add` or `remove`.")
            continue
    
    with open(metadata_dir) as metadata_write:
        json.dump(variable_dict, metadata_write)