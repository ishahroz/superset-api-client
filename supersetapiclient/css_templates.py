"""CSS Templates."""

from dataclasses import dataclass
from typing import Optional

from supersetapiclient.base import Object, ObjectFactories, default_string


@dataclass
class CssTemplate(Object):
    template_name: str
    id: Optional[int] = None
    css: str = default_string()


class CssTemplates(ObjectFactories):
    endpoint = "css_template/"
    base_object = CssTemplate
