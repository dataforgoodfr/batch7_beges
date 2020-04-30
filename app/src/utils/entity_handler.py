from collections import defaultdict


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
            lines = file_id.readlines()
            for line in lines[1:]:
                print(line)
                level_1_label, level_1_code, level_2_label, level_2_code, level_2_chorus_dt_code = line.strip().split(
                    "\t"
                )
                if level_1_code not in entities:
                    entities[level_1_code] = {"value": level_1_code, "label": level_1_label, "children": []}
                entities[level_1_code]["children"].append(
                    {"value": level_2_code, "label": level_2_label, "chorus_dt_code": level_2_chorus_dt_code}
                )
                level_1_labels[level_1_code] = level_1_label
                level_2_labels[level_2_code] = level_2_label
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