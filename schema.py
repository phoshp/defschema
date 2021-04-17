import json
from jsmin import jsmin


class SchemaEntry(object):
    name: str
    candidates: list
    object_list: bool

    def __init__(self, name: str, candidates: list, object_list: bool = False):
        self.name = name
        self.candidates = candidates
        self.object_list = object_list

    def get_name(self) -> str:
        return self.name

    def get_candidates(self) -> list:
        return self.candidates

    def add_candidate(self, candidate: object):
        self.candidates.append(candidate)

    def get_types(self) -> set[str]:
        return set(map(lambda c: type(c).__name__, self.candidates))

    def is_object_list(self) -> bool:
        return self.object_list


class DefinitionSchema(object):
    name: str
    entries: dict

    def __init__(self, name: str, entries: dict):
        self.name = name
        self.entries = entries

    def get_name(self) -> str:
        return self.name

    def get_entries(self) -> dict:
        return self.entries


def create_definition_schema(name: str, paths: list[str]) -> DefinitionSchema:
    entries = dict()

    for path in paths:
        with open(path) as file:
            data: dict = json.loads(jsmin(file.read()))
            schema_recv(data, entries)

    return DefinitionSchema(name, entries)


def schema_recv(data: dict, entries: dict):
    for key, value in data.items():
        if key in entries:
            entry = entries[key]

            if isinstance(entry, dict) and isinstance(value, dict):
                schema_recv(value, entry)
            elif isinstance(entry, SchemaEntry):
                entry.add_candidate(value)
            else:
                entries[key] = SchemaEntry(key, [entry, value])
        elif isinstance(value, dict):
            sub = dict()
            schema_recv(value, sub)
            entries[key] = sub
        elif isinstance(value, list) and isinstance(value[0], dict):
            cand = dict()
            schema_recv(value[0], cand)
            entries[key] = SchemaEntry(key, [cand], True)
        else:
            entries[key] = SchemaEntry(key, [value])
