"""Dashboards example."""

# Uncomment to run locally
import os

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

from supersetapiclient.client import SupersetClient

client = SupersetClient(
    host="http://localhost:8088",
    username="admin",
    password="admin",
)
# Get a dashboard by name
dashboard = client.dashboards.find(slug="local-landing-supplier")[0]

print(type(dashboard.json_metadata))
print(type(dashboard.position_json))
