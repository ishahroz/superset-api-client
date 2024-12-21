"""CSS templates example."""

# Uncomment to run locally
# import os
# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

from supersetapiclient.client import SupersetClient

client = SupersetClient(
    host="http://localhost:8088",
    username="admin",
    password="admin",
)
# Get a CSS template by name
css_template = client.css_templates.find(template_name="Template CSS")[0]

print(css_template.css)
