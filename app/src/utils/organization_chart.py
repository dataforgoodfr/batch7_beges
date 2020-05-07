import dill
import csv


class Entity:
    def __init__(self, id, label, id_chorus=None, id_osfi=None, id_odrive=None, parent=None, children=[]):
        self.id = id
        self.label = label
        self.id_chorus = id_chorus
        self.id_osfi = id_osfi
        self.id_odrive = id_odrive

        self.parent = parent
        self.children = children

    def __str__(self):
        return_str = self.id
        return_str = "\n  - ".join((self.id, self.label, self.parent))
        if len(self.children) > 0:
            return_str = "  - children:"
            for children in self.children:
                return_str = "\n    - ".join((self.id, self.label, self.parent))
        return return_str


class OrganizationChart:
    def __init__(self, data_path):
        self.data_path = data_path
        self._root = Entity(id="root", label="root")
        self._entities = []

        self.load()

    def load(self):
        with open(self.data_path, "r") as file_id:
            reader = csv.DictReader(file_id)
            for entity_dict in reader:
                print(entity_dict)
                entity = Entity(**entity_dict)
                print(entity)
                if entity.parent:
                    pass
                    # parent = self.get_node_by_id(entity.parent)
                    # parent.children.append(entity)
                else:
                    entity.parent = self._root
                    self._root.children.append(self.entity)
                self._entities.append(entity)

    def get_node_by_id(self, node_id):
        return None

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.nodes
