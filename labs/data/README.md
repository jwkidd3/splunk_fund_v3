# Splunk Fundamentals Course Data Files

This directory contains synthetic data files for the Splunk Fundamentals course labs.

## Data Files

| File | Size | Records | Description |
|------|------|---------|-------------|
| **access_30DAY.log** | ~35 MB | ~131K | Web application access logs (~26 days) |
| **linux_s_30DAY.log** | ~6.4 MB | ~64K | Linux SSH security logs (~26 days) |
| **db_audit_30DAY.csv** | ~3.6 MB | ~44K | Database audit logs (~26 days) |
| **products.csv** | 750 B | 16 | Product lookup table (static) |

## Data Characteristics

### Web Access Logs (access_30DAY.log)
- **Format:** Apache Combined Log Format with response time
- **Sourcetype:** `access_combined_wcookie`
- **Host:** `web_application` (set during upload)
- **Content:**
  - HTTP requests (GET, POST)
  - Status codes: 200 (successful), 404 (not found), 500 (server error), 403 (forbidden)
  - URLs with query parameters (productId, categoryId, action, JSESSIONID)
  - Various user agents (browsers)
  - Response times (milliseconds)

**Sample Event:**
```
91.214.92.22 - - [30/Aug/2026:17:57:18] "POST /success.do?action=purchase&categoryId=STRATEGY&productId=FS-SG-G03&JSESSIONID=SD6SL42FF11ADFF9850 HTTP 1.1" 200 3270 "http://www.google.com" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" 354
```
> Timestamps shift to the most recent 30 days every time the generator runs; the
> event *values* are fixed by the generator's seed.

**Conversion Funnel**

Events are emitted as per-session customer journeys, so the funnel narrows realistically:

| Stage | Events |
|-------|--------|
| Product views (`/product.screen`) | 55,880 |
| Cart additions (`action=addtocart`) | 11,339 |
| Cart views / removals | 2,532 / 821 |
| Purchases (`action=purchase`) | 3,227 |

Cart-to-purchase conversion is **~28.5%**. Each `JSESSIONID` belongs to exactly one
client IP (18,684 distinct sessions), so `dc(JSESSIONID) by clientip` ranks meaningfully.
The `categoryId` in every purchase URL matches that product's category in `products.csv`.

### Linux Security Logs (linux_s_30DAY.log)
- **Format:** Linux syslog format (SSH daemon logs)
- **Sourcetype:** `linux_secure`
- **Host:** `web_server` (set during upload)
- **Content:**
  - **Failed password, invalid user** (~32%): brute-force attempts with usernames
    that do not exist (admin, test, root, mysql, jenkins, ...)
  - **Accepted password** (~25%): legitimate SSH logins
  - **Session events** (~22%): `session opened` / `session closed`
  - **Failed password, valid user** (~13%): wrong password for a real account
  - **Other** (~8%): SSH daemon status messages

**Sample Events:**
```
Wed Sep 09 2026 00:51:59 www1 sshd[78694]: Accepted password for root from 192.168.1.100 port 22 ssh2
Thu Sep 10 2026 02:58:29 www1 sshd[83479]: Failed password for invalid user test from 202.179.8.245 port 22 ssh2
Tue Sep 29 2026 00:18:55 www1 sshd[38627]: Failed password for invalid user mysql from 198.51.100.42 port 22 ssh2
```

**Key Learning Points:**
- 41,915 events match the phrase "port 22" for the Lab 2 exercises (verified in Splunk)
- Realistic SSH brute force attack patterns
- Mix of failed/successful authentication events
- Various attack usernames and IP addresses

### Database Audit Logs (db_audit_30DAY.csv)
- **Format:** CSV with headers
- **Sourcetype:** `db_audit` (custom, created in Lab 1)
- **Host:** `database` (set during upload)
- **Content:**
  - Query operations (SELECT, INSERT, UPDATE, DELETE)
  - Connection events
  - Query duration in milliseconds
  - Timestamps

**Sample Events:**
```csv
Time,Type,Command,Duration
30/Aug/2026 16:40:48,Connect,admin on BCG using TCP/IP,
07/Sep/2026 21:03:03,Query,SELECT * FROM users WHERE userid = 4395,13
14/Sep/2026 23:08:25,Query,UPDATE products SET stock = stock - 1 WHERE productid = 7962,39
```

### Products Lookup (products.csv)
- **Format:** CSV with headers
- **Type:** Static lookup table
- **Content:** Product catalog (16 products)
- **Fields:** productId, product_name, categoryId, price, Code

**Sample:**
```csv
productId,product_name,categoryId,price,Code
DB-SG-G01,Mediocre Kingdoms,STRATEGY,24.99,A
DC-SG-G02,Dream Crusher,STRATEGY,39.99,B
```

## Regenerating Data

If you need to regenerate the data files (e.g., to change patterns or increase volume):

### Prerequisites
- Python 3.6+
- No external dependencies required

### Steps

1. **Navigate to data directory:**
   ```bash
   cd labs/data
   ```

2. **Run generation script:**
   ```bash
   python3 generate_course_data.py
   ```

3. **Command-line options:**
   ```bash
   python3 generate_course_data.py --days 30 --seed 20240101
   ```
   - `--days N` — size of the rolling window (default 26)
   - `--seed N` — random seed (default 20240101)

   > **The generator is deterministic.** A given seed always produces the same
   > event *values*, so the lab answer keys stay correct across regenerations —
   > only the timestamps roll forward. Change the seed only if you intend to
   > recompute every answer key.

   > **Why 26 days and not 30?** The labs tell students to search with Splunk's
   > **Last 30 days** preset. If the data also spanned a full 30 days, that preset
   > would begin clipping the oldest events as soon as the clock passed generation
   > time, and every count in the answer keys would drift. The 4-day gap means
   > "Last 30 days" captures 100% of the data — and the answer keys stay exact —
   > for **4 days** after you generate it. **Regenerate within 4 days of class.**

4. **Other customization:**
   Edit `generate_course_data.py` to modify:
   - **Event counts:**
     - Web logs: `generate_web_access_logs(count=...)`
     - Database logs: `generate_db_audit_logs(count=...)`
     - Linux logs: `generate_linux_security_logs(count=8000)`
   - **Attack patterns:** Modify weights in `log_patterns`
   - **User/IP lists:** Add to `failed_users`, `suspicious_ips`, etc.

### Generation Time
- Typically completes in 30-60 seconds
- Generates ~180K total events
- Creates ~45 MB of data

## Data Loading in Splunk

### Quick Reference

```spl
# Verify all data loaded (Last 30 days covers the whole dataset)
index=main earliest=-30d
| stats count by sourcetype, host

# Expected results:
# - access_combined_wcookie, web_application: ~131K events
# - linux_secure, web_server: ~64K events
# - db_audit, database: ~44K events
```

### Detailed Instructions
See `lab1_data_loading.md` for complete upload instructions.

## Important Notes

- ⚠️ **products.csv is static** - Do not regenerate; used as lookup table
- 📊 **Rolling ~26-day window** - Timestamps end within minutes of when the script ran
  and sit inside the **Last 30 days** search preset with 4 days of slack. All three
  logs are written in time order.
- ⏰ **Regenerate within 4 days of class** - past that, "Last 30 days" clips the oldest
  events and the lab answer keys no longer match.
- 🔄 **Re-upload required** - After regenerating data, must re-upload to Splunk
- 🎯 **Lab alignment** - Data patterns designed specifically for lab exercises
- 🔒 **Synthetic data only** - All IPs, usernames, and data are fake/synthetic

## Troubleshooting

### "No events found" in Splunk
- Check the time range is set to **Last 30 days** (the window the data covers)
- Verify sourcetype and host values match lab instructions
- Confirm files uploaded successfully

### Generation script fails
```bash
# Check Python version
python3 --version  # Should be 3.6+

# Run with verbose output
python3 -v generate_course_data.py
```

### File size concerns
- Default generation creates ~45 MB total
- Reduce count parameters to generate smaller files
- Or use shorter time range (e.g., `days=7`)

## Lab Coverage

This data supports all course labs:

- ✅ **Lab 1:** Data loading and verification
- ✅ **Lab 2:** Basic searching, Boolean operators, timeline analysis
- ✅ **Lab 3:** Field-based searching and filters
- ✅ **Lab 4:** Commands (fields, table, rename, dedup, sort)
- ✅ **Lab 5:** Transforming commands (stats, top, rare, chart)
- ✅ **Lab 6:** Reports and dashboards
- ✅ **Lab 7:** Pivot tables and datasets
- ✅ **Lab 8:** Lookups and data enrichment
- ✅ **Lab 9:** Alerts and scheduled reports

## Questions?

- See individual lab instructions in `labs/` directory
- Check main course README: `../../README.md`
- Review generation script comments: `generate_course_data.py`
