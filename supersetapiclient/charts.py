"""Charts."""

from dataclasses import dataclass, field

from supersetapiclient.base import Object, ObjectFactories, default_string, json_field


@dataclass
class Chart(Object):
    """Chart."""

    JSON_FIELDS = ["params"]

    id: int | None = None
    description: str = default_string()
    slice_name: str = default_string()
    params: dict = json_field()
    datasource_id: int | None = None
    datasource_type: str = default_string()
    viz_type: str = ""
    dashboards: list[int] = field(default_factory=list)

    def to_json(self, columns):
        """Convert the chart to a JSON object."""
        o = super().to_json(columns)
        o["dashboards"] = self.dashboards
        return o


class Charts(ObjectFactories):
    """Charts."""

    endpoint = "chart/"
    base_object = Chart

    @property
    def add_columns(self):
        """Get the columns to add to a chart."""
        # Due to the design of the superset API,
        # get /chart/_info only returns 'slice_name'
        # For chart adds to work,
        # we require the additional attributes:
        #   'datasource_id',
        #   'datasource_type'
        return [
            "datasource_id",
            "datasource_type",
            "slice_name",
            "params",
            "viz_type",
            "description",
        ]
