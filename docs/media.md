# Media

Download media files from message URLs.

## Download media

```python
from wazzapi import download_media

result = download_media("https://example.com/media.jpg")
print(result.content_type)
print(result.filename)

with open(result.filename or "media.jpg", "wb") as f:
    f.write(result.content)
```

## MediaDownloadResult

| Attribute | Type | Description |
|-----------|------|-------------|
| `content` | `bytes` | Raw file content |
| `content_type` | `str \| None` | MIME type from the response |
| `filename` | `str \| None` | Filename if available |
