import schema
import os
import glob


def find_components(a: dict) -> dict:
    result = a
    for key, value in a.items():
        if key == 'components':
            return value
        elif isinstance(value, dict):
            result = find_components(value)

    return result

def print_enum(a: list[str]) -> None:
    for value in a:
        name = value.replace('minecraft:', '').replace('.', '_').upper()
        print('public static final String ' + name + ' = "' + value + '";')


print('Enter path: ')
path = input()
if os.path.isdir(path):
    sc = schema.create_definition_schema('compids', glob.glob(path + '/*.json'))
    print_enum(list(find_components(sc.get_entries()).keys()))
else:
    print("Path is invalid")
