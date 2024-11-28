"""Dashboards."""

from dataclasses import dataclass, field

from supersetapiclient.base import (
    Object,
    ObjectFactories,
    default_string,
    json_field,
    raise_for_status,
)


@dataclass
class DashboardEmbed(Object):
    """Dashboard embed."""

    allowed_domains: list[str] = field(default_factory=list)
    uuid: str = None


@dataclass
class DashboardCopy(Object):
    """Dashboard copy."""

    id: int | None = None


@dataclass
class Dashboard(Object):
    """Dashboard."""

    JSON_FIELDS = ["json_metadata", "position_json"]

    dashboard_title: str
    published: bool
    id: int | None = None
    json_metadata: dict = json_field()
    position_json: dict = json_field()
    changed_by: str = default_string()
    slug: str = default_string()
    changed_by_name: str = default_string()
    changed_by_url: str = default_string()
    css: str = default_string()
    changed_on: str = default_string()
    charts: list[str] = field(default_factory=list)

    @property
    def colors(self) -> dict:
        """Get dashboard color mapping."""
        return self.json_metadata.get("label_colors", {})

    @colors.setter
    def colors(self, value: dict) -> None:
        """Set dashboard color mapping."""
        self.json_metadata["label_colors"] = value

    def update_colors(self, value: dict) -> None:
        """Update dashboard colors."""
        colors = self.colors
        colors.update(value)
        self.colors = colors

    def get_charts(self) -> list[int]:
        """Get chart objects."""
        charts = []
        for slice_name in self.charts:
            c = self._parent.client.charts.find_one(slice_name=slice_name)
            charts.append(c)
        return charts

    def get_embed(self) -> DashboardEmbed:
        """Get the dashboard's embedded configuration."""
        client = self._parent.client
        embed_dashboard_url = client.join_urls(self.base_url, "embedded")
        response = client.get(embed_dashboard_url)
        if response.status_code == 404:
            return None
        return DashboardEmbed().from_json(response.json().get("result"))

    def create_embed(self, allowed_domains: list[str]) -> DashboardEmbed:
        """Set a dashboard's embedded configuration."""
        client = self._parent.client
        embed_dashboard_url = client.join_urls(self.base_url, "embedded")
        response = client.post(
            embed_dashboard_url, json={"allowed_domains": allowed_domains}
        )
        raise_for_status(response)
        return DashboardEmbed().from_json(response.json().get("result"))

    def copy_dashboard(self, dashboard_payload: dict) -> DashboardCopy:
        """Copy the dashboard with the given payload."""
        client = self._parent.client
        copy_dashboard_url = client.join_urls(self.base_url, "copy")
        response = client.post(copy_dashboard_url, json=dashboard_payload)
        raise_for_status(response)
        return DashboardCopy().from_json(response.json().get("result"))


class Dashboards(ObjectFactories):
    """Dashboards."""

    endpoint = "dashboard/"
    base_object = Dashboard
