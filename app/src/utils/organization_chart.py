import csv
import os
from pathlib import Path
import json

from anytree import NodeMixin, RenderTree
from anytree.search import find as find_tree
from anytree.exporter import JsonExporter
from anytree.importer import JsonImporter
from anytree.importer import DictImporter

ORGANIZATION_CHART_DIR = Path("/data/entities")
ORGANIZATION_CHART_DIR.mkdir(parents=True, exist_ok=True)


class Entity(NodeMixin):
    def __init__(
        self, id, label, code_chorus=None, code_osfi=None, code_odrive=None, parent=None, children=None, activated=False
    ):
        self.id = id
        self.label = label
        self.code_chorus = code_chorus
        self.code_osfi = code_osfi
        self.code_odrive = code_odrive
        self.activated = activated

        self.parent = parent

    def __repr__(self):
        return_string = "%s: %s" % (self.id, self.label)
        return_string += "(%s, %s, %s)" % (self.code_chorus, self.code_osfi, self.code_odrive)
        return return_string

    def to_json(self):
        to_return_dict = {k: v for k, v in self.__dict__.items() if (("parent" not in k) and ("children" not in k))}
        to_return_dict["parent"] = self.parent.id
        return json.dumps(to_return_dict)


class OrganizationChart:
    def __init__(self):
        self._root = Entity(id="root", label="root")

    def load_json(self, json_tree):
        dict_importer = DictImporter(nodecls=Entity)
        self._root = JsonImporter(dict_importer).import_(json_tree)

    def load_json_file(self, filename):
        with open(ORGANIZATION_CHART_DIR / filename) as file_id:
            json_tree = file_id.read()
            self.load_json(json_tree)

    def to_json(self):
        return JsonExporter().export(self._root)

    def save_json(self, filename):
        with open(ORGANIZATION_CHART_DIR / filename, "w") as file_id:
            json_tree = self.to_json()
            file_id.write(json_tree)

    def set_current(self, filename):
        with open(ORGANIZATION_CHART_DIR / "current", "w") as file_id:
            file_id.write(filename)

    def load_current(self):
        # If there is no current file, we will create one with the default entity tree
        if not os.path.isfile(ORGANIZATION_CHART_DIR / "current"):
            self.set_current("default")

        with open(ORGANIZATION_CHART_DIR / "current") as file_id:
            filename = file_id.read().strip()
            self.load_json_file(filename)

    def load_tsv(self, tsv_path):
        entities = {}
        entities["root"] = self._root
        with open(tsv_path, "r") as file_id:
            reader = csv.DictReader(file_id, delimiter="\t")
            for entity_dict in reader:
                entity_dict["parent"] = entities[entity_dict["parent"]]
                entity = Entity(**entity_dict)
                entities[entity.id] = entity

    def render_tree(self):
        print("Organization chart: ")
        print(RenderTree(self._root))

    def get_entity_by_id(self, id):
        return find_tree(self._root, lambda entity: entity.id == id)

    def get_level_1_dropdown_items(self):
        return self.get_children_dropdown_items()

    def get_level_2_dropdown_items(self, level_1_id):
        return self.get_children_dropdown_items(level_1_id)

    def get_children_dropdown_items(self, entity_id="root"):
        return [{"value": entity.id, "label": entity.label} for entity in self.get_entity_by_id(entity_id).children]

    def get_organization_service(self, selected_entity):
        organization_id, service_id = selected_entity.split(";")
        return self.get_entity_by_id(organization_id), self.get_entity_by_id(service_id)

    def get_leaves(self):
        return self._root.leaves
