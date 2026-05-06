# Templates

Create and manage reusable message templates.

## List templates

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    response = client.templates.list(limit=20, category="marketing")

for template in response.data:
    print(template.name, template.variables)
```

## Get a template

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    template = client.templates.get("template-id")
    print(template.content, template.variables)
```

## Create a template

```python
from wazzapi import TemplateCreateRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    template = client.templates.create(
        TemplateCreateRequest(
            name="welcome-message",
            category="marketing",
            content="Hi {{name}}, welcome to WazzAPI!",
        )
    )

print(template.id)
```

## Update a template

```python
from wazzapi import TemplateUpdateRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    template = client.templates.update(
        "template-id",
        TemplateUpdateRequest(content="Hi {{name}}, welcome! Your code is {{code}}."),
    )

print(template.content)
```

## Delete a template

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    client.templates.delete("template-id")
```

## Preview a template

```python
from wazzapi import TemplatePreviewRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    preview = client.templates.preview(
        TemplatePreviewRequest(
            content="Hi {{name}}, your code is {{code}}.",
            custom_variables={"name": "Alice", "code": "WZ-1234"},
        )
    )

print(preview.preview)
print(preview.missing_variables)
```

## Built-in variables

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    response = client.templates.builtin_variables()
    for var in response.variables:
        print(var.name, var.description, var.example)
```
