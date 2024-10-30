"""Dashboards."""

from dataclasses import dataclass, field

from supersetapiclient.base import Object, ObjectFactories


@dataclass
class Dataset(Object):
    """Dataset."""

    JSON_FIELDS = []

    id: int | None = None
    table_name: str = ""
    schema: str = ""
    columns: list = field(default_factory=list)
    description: str = ""
    kind: str = ""
    database_id: int | None = None
    sql: str = ""

    @classmethod
    def from_json(cls, json: dict):
        """Create a dataset from a JSON object."""
        res = super().from_json(json)
        database = json.get("database")
        if database:
            res.database_id = database.get("id")
        return res

    def to_json(self, *args, **kwargs):
        """Convert the dataset to a JSON object."""
        o = super().to_json(*args, **kwargs)
        o.pop("columns", None)
        if self.id:
            o["database_id"] = self.database_id
        else:
            o["database"] = self.database_id
        return o

    def run(self, query_limit=None):
        """Run the dataset."""
        if not self.sql:
            raise ValueError("Cannot run a dataset with no SQL")
        return self._parent.client.run(
            database_id=self.database_id, query=self.sql, query_limit=query_limit
        )


class Datasets(ObjectFactories):
    """Datasets."""

    endpoint = "dataset/"
    base_object = Dataset
