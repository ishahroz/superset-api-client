"""Saved queries."""

from dataclasses import dataclass

from supersetapiclient.base import Object, ObjectFactories, default_string


@dataclass
class SavedQuery(Object):
    """Saved query."""

    JSON_FIELDS = []

    label: str
    id: int | None = None
    description: str = default_string()
    sql: str = default_string()
    db_id: int = None
    schema: str = default_string()

    @classmethod
    def from_json(cls, json: dict):
        """Create a saved query from a JSON object."""
        res = super().from_json(json)
        database = json.get("database")
        if database:
            res.db_id = database.get("id")
        return res

    def run(self, query_limit=None):
        """Run the saved query."""
        return self._parent.client.run(
            database_id=self.db_id, query=self.sql, query_limit=query_limit
        )


class SavedQueries(ObjectFactories):
    """Saved queries."""

    endpoint = "saved_query/"
    base_object = SavedQuery
