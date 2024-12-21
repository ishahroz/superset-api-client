"""Delete a dashboard."""

import os

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

from supersetapiclient.client import SupersetClient

client = SupersetClient(
    host="http://localhost:8088",
    username="admin",
    password="admin",
)
# Get a dashboard by id
dashboard = client.dashboards.delete(object_id=141)

print(dashboard)
