import csv

from anytree import NodeMixin, RenderTree
from anytree.search import find as find_tree


class Entity(NodeMixin):
    def __init__(self, id, label, code_chorus=None, code_osfi=None, code_odrive=None, parent=None, children=None):
        self.id = id
        self.label = label
        self.code_chorus = code_chorus
        self.code_osfi = code_osfi
        self.code_odrive = code_odrive

        self.parent = parent
        if children:
            self.children = children

    def __repr__(self):
        return_string = "%s: %s" % (self.id, self.label)
        return_string += "(%s, %s, %s)" % (self.code_chorus, self.code_osfi, self.code_odrive)
        return return_string


class OrganizationChart:
    def __init__(self, data_path):
        self.data_path = data_path
        self._root = Entity(id="root", label="root")
        self.load()

    def load(self):
        entities = {}
        entities["root"] = self._root
        with open(self.data_path, "r") as file_id:
            reader = csv.DictReader(file_id, delimiter="\t")
            for entity_dict in reader:
                entity_dict["parent"] = entities[entity_dict["parent"]]
                entity = Entity(**entity_dict)
                entities[entity.id] = entity
        print("Loaded entity tree")
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


oc = OrganizationChart("/data/entities_tree.tsv")
