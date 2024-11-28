"""Copy a dashboard."""

# Uncomment to run locally
# import os
# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

from supersetapiclient.client import SupersetClient

client = SupersetClient(
    host="http://localhost:8088",
    username="admin",
    password="admin",
)
# Get a dashboard by name
dashboard = client.dashboards.find(slug="local-landing-supplier")[0]

dashboard_copy = dashboard.copy_dashboard(
    dashboard_payload={
        "css": "",
        "dashboard_title": "your-new-dashboard-title",
        "duplicate_slices": False,
        "json_metadata": "{}",
    }
)

print(dashboard_copy)
