# Splunk Fundamentals

All course material in this repository is **offline-capable**: the presentations,
labs, lab PDFs and sample datasets work with no network connection. The one piece
that needs internet is the initial Splunk setup — see **Offline preparation** below.

## Setup: Choose your splunk implementation

### Option 1 — Docker (works offline once the image is pulled)

```bash
docker run -d -p 8000:8000 \
  -e SPLUNK_GENERAL_TERMS=--accept-sgt-current-at-splunk-com \
  -e SPLUNK_START_ARGS=--accept-license \
  --platform linux/amd64 \
  -e "SPLUNK_PASSWORD=password" \
  --name splunk splunk/splunk:latest
```

Splunk Web is then at <http://localhost:8000> (user `admin`, password `password`).

### Option 2 — Splunk Cloud eval (requires internet for the whole class)

Request a free eval instance at
<https://www.splunk.com/en_us/download/splunk-cloud.html>

> **Note**: When there have been issues in the signup process, some users have
> created a temporary gmail account to use to get around it.

> **Not suitable for an offline class.** Splunk Cloud is hosted, so it needs a
> live connection for every search. Use Option 1 if the room may be offline.

## Offline preparation

Do this **while you still have internet**, ideally the day before:

1. **Pull the Splunk image** (several GB — do not leave this to class time):
   ```bash
   docker pull --platform linux/amd64 splunk/splunk:latest
   ```
2. **Verify it is cached locally**:
   ```bash
   docker images splunk/splunk
   ```
   If this prints a row, the container will start with no network.
3. **Start it once and log in** at <http://localhost:8000> to confirm it works
   before you are offline.
4. **Regenerate the sample data** if it is more than a few days old — see
   `labs/data/README.md`. The generator runs fully offline.

> **Pinning the version**: `:latest` means different machines may get different
> Splunk builds. For a consistent classroom, pull a specific tag instead
> (check available tags on Docker Hub) and use that same tag everywhere.

## What works with no network

| Material | Offline | Notes |
|---|---|---|
| `presentations/*.html` | Yes | reveal.js, theme and fonts are embedded in each file |
| `labs/*.md` | Yes | No external assets |
| `labs/pdf/*.pdf` | Yes | Self-contained |
| `labs/data/*` | Yes | Generated locally by `generate_course_data.py` |
| Splunk itself | Yes, via Docker | Image must be pulled in advance (see above) |

`notes.md` is a list of reference links to Splunk documentation; those pages
need internet, but nothing in the labs depends on them.
