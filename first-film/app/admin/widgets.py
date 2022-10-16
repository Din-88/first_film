import json
from wtforms.widgets import Select, CheckboxInput, html_params
from markupsafe import escape
from markupsafe import Markup


class ListWidget:

    def __init__(self, html_tag="ul", prefix_label=True):
        assert html_tag in ("ol", "ul")
        self.html_tag = html_tag
        self.prefix_label = prefix_label

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        html = [f"<div class='multi_select'><textarea class='textarea' readonly></textarea>\n<{self.html_tag} {html_params(**kwargs)}>"]
        for subfield in field:
            if self.prefix_label:
                html.append(f"<li>{subfield.label} {subfield()}</li>")
            else:
                html.append(f"<li>{subfield()} {subfield.label}</li>")
        html.append("</%s>" % self.html_tag)
        html.append("\n</div>")
        return Markup("".join(html))