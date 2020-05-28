import json
import dash_html_components as html
import dash_bootstrap_components as dbc
from utils.organization_chart import OrganizationChart, Entity


from anytree import LevelGroupOrderIter, PreOrderIter
from anytree.search import find as find_tree
from anytree.exporter import JsonExporter
from anytree.importer import JsonImporter
from anytree.importer import DictImporter


def oc_to_ochw(organization_chart):
    root = EntityHtmlWrapper(id="root", label="root", activated=True)
    elements = {}
    elements["root"] = root
    for entity in PreOrderIter(organization_chart._root):
        if entity.id == "root":
            continue
        parent_id = entity.parent.id
        entity = EntityHtmlWrapper(
            **{k: v for k, v in entity.__dict__.items() if (("parent" not in k) and ("children" not in k))},
            expand=False,
        )
        # Only displaying first level elements

        entity.parent = elements[parent_id]

        if entity.parent.id == "root":
            entity.visible = True

        elements[entity.id] = entity
    ochw = OrganizationChartHtmlWrapper()
    ochw._root = root
    return ochw


def ochw_to_oc(organization_chart_html_wrapper):

    root = Entity(id="root", label="root", activated=True)
    elements = {}
    elements["root"] = root
    for entity_wrapper in PreOrderIter(organization_chart_html_wrapper._root):
        if entity_wrapper.id == "root":
            continue
        parent_id = entity_wrapper.parent.id
        entity = Entity(
            id=entity_wrapper.id,
            label=entity_wrapper.label,
            code_chorus=entity_wrapper.code_chorus,
            code_osfi=entity_wrapper.code_osfi,
            code_odrive=entity_wrapper.code_odrive,
            activated=entity_wrapper.activated,
        )

        entity.parent = elements[parent_id]
        elements[entity.id] = entity
    oc = OrganizationChart()
    oc._root = root
    return oc


class EntityHtmlWrapper(Entity):
    def __init__(
        self,
        id,
        label,
        code_chorus=None,
        code_osfi=None,
        code_odrive=None,
        parent=None,
        activated=False,
        expand=False,
        valid=False,
        selected=False,
        visible=False,
    ):
        super().__init__(
            id=id,
            label=label,
            code_chorus=code_chorus,
            code_osfi=code_osfi,
            code_odrive=code_odrive,
            parent=parent,
            activated=activated,
        )
        self.expand = expand
        self.valid = valid
        self.selected = selected
        self.visible = visible

    def get_expand_element(self):
        if self.children:
            if self.expand == True:
                icon_classname = "fa fa-chevron-down fa-1x"
            else:
                icon_classname = "fa fa-chevron-right fa-1x"

            return html.Div(
                id={"type": "back-office-entity-expand", "id": self.id},
                children=[html.I(className=icon_classname)],
                style={"height": "100%", "width": "100%"},
                className="d-flex align-items-center justify-content-center back-office-entity-expand",
            )
        else:
            return html.Div()

    def get_title_element(self):
        return html.P(" -- " * self.depth + self.label)

    def get_active_element(self):
        return dbc.FormGroup(
            dbc.Checklist(
                id={"type": "back-office-entity-activated", "id": self.id},
                options=[{"label": "Active", "value": "1", "disabled": not self.parent.activated}],
                value=["1"] if self.activated else [],
            )
        )

    def get_update_button_element(self):

        return dbc.Button(
            "Modifier",
            id={"type": "back-office-entity-update-open-button", "id": self.id},
            block=True,
            style={"vertical-align": "middle"},
            color="primary",
        )

    def to_html(self):
        classname = "back_office_entity"
        return html.Div(
            id={"type": "back-office-entity", "id": self.id},
            children=[
                dbc.Row(
                    [
                        # The expand button
                        dbc.Col(self.get_expand_element(), width={"size": 1}),
                        dbc.Col(self.get_title_element(), width={"size": 3}),
                        dbc.Col([html.P("OSFI:\n"), html.P(self.code_osfi)], width=2),
                        dbc.Col([html.P("Odrive:\n"), html.P(self.code_odrive)], width=2),
                        dbc.Col([html.P("Chorus:\n"), html.P(self.code_chorus)], width=2),
                        dbc.Col(self.get_active_element(), width=1),
                        dbc.Col(
                            self.get_update_button_element(),
                            width=1,
                            # className="mx-0",
                        ),
                    ]
                )
            ],
            className=classname,
        )


class OrganizationChartHtmlWrapper:
    def __init__(self):
        self._root = None

    def get_html_elements(self):
        elements = []
        for entity in PreOrderIter(self._root):
            if entity.id == "root":
                continue
            if entity.visible:
                elements.append(entity.to_html())
        return elements

    def load_json(self, tree_json):
        dict_importer = DictImporter(nodecls=EntityHtmlWrapper)
        self._root = JsonImporter(dict_importer).import_(tree_json)

    def to_json(self):
        return JsonExporter().export(self._root)

    def get_parent_options(self, entity_id=None) -> dict:
        options = []
        entity = self.get_entity_by_id(entity_id)
        for other_entity in PreOrderIter(self._root):
            if other_entity.id == "root":
                options.append({"label": "Pas de parent", "value": other_entity.id})
            elif entity_id and (other_entity.id == entity_id):
                continue
            else:
                if entity is None:
                    options.append({"label": other_entity.label, "value": other_entity.id})
                elif other_entity not in entity.descendants:
                    options.append({"label": other_entity.label, "value": other_entity.id})
        return options

    def get_entity_by_id(self, entity_id) -> Entity:
        return find_tree(self._root, lambda entity: entity.id == entity_id)

    def toggle_activation(self, entity_id):
        entity = self.get_entity_by_id(entity_id)
        entity.activated = not entity.activated
        # Unactivate all descents
        if not entity.activated:
            for other_entity in entity.descendants:
                other_entity.activated = False

    def toggle_expand(self, entity_id):
        entity = self.get_entity_by_id(entity_id)
        if entity.expand == False:
            entity.expand = True
            for child in entity.children:
                child.visible = True
        else:
            entity.expand = False
            for descendor in PreOrderIter(entity):
                if descendor.id == entity.id:
                    continue
                descendor.visible = False
                descendor.expand = False

    def toggle_entity_visible(self, entity_id):
        entity = self.get_entity_by_id(entity_id)
        entity_ancestors = entity.ancestors
        for other_entity in PreOrderIter(self._root):
            if other_entity.id == "root":
                continue
            elif other_entity.parent.id == "root":
                other_entity.visible = True
                other_entity.expand = False
            else:
                other_entity.visible = False
                other_entity.expand = False
        for other_entity in entity_ancestors[::-1]:
            if other_entity.id == "root":
                continue
            else:
                self.toggle_expand(other_entity.id)


if __name__ == "__main__":
    organization_chart = OrganizationChart("/data/entities_test_tree_2.tsv")
    och = OrganizationChartHtmlWrapper(organization_chart)

    tree_json = json.dumps(PreOrderIter(organization_chart._root), cls=OrganizationChartJsonEncoder)
    # oc = OrganizationChartJsonEncoder().from_json(tree_json)
