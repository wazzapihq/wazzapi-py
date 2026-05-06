# Contacts

Manage contacts and contact groups.

## List contacts

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    response = client.contacts.list(limit=50, search="alice")

for contact in response.contacts:
    print(contact.name, contact.phone_number)
```

## Get a contact

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    contact = client.contacts.get("contact-id")
    print(contact.phone_number, contact.tags)
```

## Create a contact

```python
from wazzapi import ContactCreateRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    contact = client.contacts.create(
        ContactCreateRequest(
            phone_number="+6281234567890",
            name="Alice",
            tags=["customer", "vip"],
        )
    )

print(contact.id)
```

## Update a contact

```python
from wazzapi import ContactUpdateRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    contact = client.contacts.update(
        "contact-id",
        ContactUpdateRequest(name="Alice Smith", tags=["customer"]),
    )

print(contact.name)
```

## Delete a contact

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    client.contacts.delete("contact-id")
```

## Bulk delete

```python
from wazzapi import BulkDeleteRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.contacts.bulk_delete(
        BulkDeleteRequest(contact_ids=["id-1", "id-2"])
    )

print(result.deleted)
```

## Contact groups

### List groups

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    response = client.contacts.list_groups(limit=20)

for group in response.groups:
    print(group.name, group.member_count)
```

### Create a group

```python
from wazzapi import ContactGroupCreateRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    group = client.contacts.create_group(
        ContactGroupCreateRequest(name="VIP Customers", description="Top tier")
    )

print(group.id)
```

### Get a group with members

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    response = client.contacts.get_group("group-id")
    print(response.group.name)
    for contact in response.contacts:
        print(contact.name)
```

### Update a group

```python
from wazzapi import ContactGroupUpdateRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    group = client.contacts.update_group(
        "group-id",
        ContactGroupUpdateRequest(name="Updated Name"),
    )

print(group.name)
```

### Delete a group

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    client.contacts.delete_group("group-id")
```

### Add contacts to a group

```python
from wazzapi import AddToGroupRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.contacts.add_to_group(
        "group-id",
        AddToGroupRequest(contact_ids=["contact-1", "contact-2"]),
    )

print(result.added)
```

### Remove contacts from a group

```python
from wazzapi import RemoveFromGroupRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.contacts.remove_from_group(
        "group-id",
        RemoveFromGroupRequest(contact_ids=["contact-1"]),
    )

print(result.added)
```

## Import and export

### Import from CSV

```python
from wazzapi import CSVImportRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.contacts.import_csv(
        CSVImportRequest(csv_content="phone_number,name\n+6281234567890,Alice", skip_duplicates=True)
    )

print(result.imported, result.updated, result.errors)
```

### Export to CSV

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.contacts.export_csv(group_id="group-id")
    print(result.csv_data)
```

### Get import template

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    template = client.contacts.import_template()
    print(template)
```

## Sync contacts from WhatsApp

### Start sync

```python
from wazzapi import ContactSyncRequest, WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    result = client.contacts.sync(
        ContactSyncRequest(whatsapp_account_id="wa-123", sync_type="full")
    )

print(result.job_id, result.status)
```

### Check sync status

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    statuses = client.contacts.sync_status()
    for s in statuses:
        print(s.account_name, s.last_sync_status, s.contacts_synced_count)
```

### Sync history

```python
from wazzapi import WazzapiClient

with WazzapiClient(api_key="your-api-key") as client:
    response = client.contacts.sync_history(limit=10)
    for item in response.history:
        print(item.account_name, item.status, item.contacts_count)
```
