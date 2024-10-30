"""CSS Templates."""

from dataclasses import dataclass

from supersetapiclient.base import Object, ObjectFactories, default_string


@dataclass
class CssTemplate(Object):
    """CSS template."""

    template_name: str
    id: int | None = None
    css: str = default_string()


class CssTemplates(ObjectFactories):
    """CSS templates."""

    endpoint = "css_template/"
    base_object = CssTemplate
