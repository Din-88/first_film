from wtforms import SelectMultipleField
from wtforms import widgets 
from app.admin.widgets import ListWidget

class MySelectMultipleField(SelectMultipleField):

    widget = ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

    def __init__(self, session, query_factory, choices, 
                label=None, validators=None, 
                default=None, **kwargs):
        self.session = session
        self.query_factory = query_factory
        self.choices = choices
        if default is None:
            default = []
        super().__init__(label, validators, default=default, choices=self.choices, **kwargs)


    def process_data(self, value):
        if value:
            choices = self.choices
            choices = [(v.id, v) for v in value]
            choices.extend([c for c in self.choices if c[0] not in [v.id for v in value]])

            self.choices = choices
            self.default = [v.id for v in value]
            self.data = [v.id for v in value]
            pass


    def process_formdata(self, valuelist):
        if valuelist:
            valuelist = [self.coerce(v) for v in valuelist]
            items = self.query_factory(name=self.name, ids=valuelist)

            items = [c[1] for c in self.choices if c[1].id in valuelist]

            # self.default = [self.coerce(v) for v in valuelist]
            # self.default = [v.id for v in items]
            items = [self.session.merge(i) for i in items]
            self.data = items
            pass
        else:
            self.data = []