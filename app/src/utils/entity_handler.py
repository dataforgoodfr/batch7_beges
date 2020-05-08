from collections import defaultdict
import csv


class EntityHandler:
    def __init__(self):
        self._entities = None
        self._level_1_labels = None
        self._level_2_labels = None

        self.load_entities()

    def load_entities(self):
        entities = {}
        level_1_labels = {}
        level_2_labels = {}
        with open("/data/entities.tsv") as file_id:
            reader = csv.DictReader(file_id, delimiter="\t")
            for entity in reader:
                print(entity)
                if entity["level_1_code"] not in entities:
                    entities[entity["level_1_code"]] = {
                        "value": entity["level_1_code"],
                        "label": entity["level_1_label"],
                        "children": [],
                    }
                entity["value"] = entity["level_2_code"]
                entity["label"] = entity["level_2_label"]
                entities[entity["level_1_code"]]["children"].append(entity)
                level_1_labels[entity["level_1_code"]] = entity["level_1_label"]
                level_2_labels[entity["level_2_code"]] = entity["level_2_label"]
        self._entities = entities
        self._level_1_labels = level_1_labels
        self._level_2_labels = level_2_labels

    def get_level_1_dropdown_items(self):
        return [{"value": item["value"], "label": item["label"]} for item in self._entities.values()]

    def get_level_2_dropdown_items(self, level_1_value):
        return [{"value": item["value"], "label": item["label"]} for item in self._entities[level_1_value]["children"]]

    def get_level_1_label(self, level_1_code):
        return self._level_1_labels[level_1_code]

    def get_level_2_label(self, level_2_code):
        return self._level_2_labels[level_2_code]

    def get_level_2_code(self, level_2_code, dataset):
        entity = [e for e in self._entities if e["level_2_code"] == level_2_code]
        return entity["level_2_code_%s" % dataset]

    def get_level_2_code_odrive(self, level_2_code):
        return self.get_level_2_code(level_2_code, "odrive")

    def get_level_2_code_osfi(self, level_2_code):
        return self.get_level_2_code(level_2_code, "osfi")

    def get_level_2_code_chorus(self, level_2_code):
        return self.get_level_2_code(level_2_code, "chorus")


eh = EntityHandler()
