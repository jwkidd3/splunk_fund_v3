# Splunk Fundamentals Course Data Files

This directory contains synthetic data files for the Splunk Fundamentals course labs.

## Data Files

| File | Size | Records | Description |
|------|------|---------|-------------|
| **access_30DAY.log** | ~35 MB | ~131K | Web application access logs (30 days) |
| **linux_s_30DAY.log** | ~6.4 MB | ~64K | Linux SSH security logs (30 days) |
| **db_audit_30DAY.csv** | ~3.6 MB | ~44K | Database audit logs (30 days) |
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
91.214.92.22 - - [15/Oct/2025:05:59:36] "POST /success.do?action=purchase&categoryId=SIMULATION&productId=BS-AG-G09&JSESSIONID=SD1SL38FF97ADFF1201 HTTP 1.1" 200 691 "-" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36" 387
```

### Linux Security Logs (linux_s_30DAY.log)
- **Format:** Linux syslog format (SSH daemon logs)
- **Sourcetype:** `linux_secure`
- **Host:** `web_server` (set during upload)
- **Content:**
  - **Failed password attempts** (~45%): Brute force SSH attacks
    - 75% on port 22 (realistic attack pattern)
    - Mix of invalid and valid usernames
    - From suspicious IP addresses
  - **Successful logins** (~25%): Legitimate SSH sessions
    - Always port 22
    - From legitimate IP addresses
  - **Invalid user attempts** (~5%): Explicit invalid user attacks
    - Always port 22
    - Common attack usernames (admin, test, root, etc.)
  - **Session events** (~22%): Session opened/closed
  - **Server events** (~3%): SSH daemon status messages

**Sample Events:**
```
Mon Oct 06 2025 05:41:05 www1 sshd[15456]: Failed password for invalid user root from 202.179.8.245 port 22 ssh2
Mon Oct 20 2025 06:07:12 www1 sshd[45252]: Accepted password for root from 10.0.0.50 port 22 ssh2
Sat Oct 11 2025 04:04:14 www1 sshd[23766]: pam_unix(sshd:session): session closed for user analyst
```

**Key Learning Points:**
- ~42K events contain "port 22" for Task 2 exercises
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
27/Sep/2025 01:32:00,Query,UPDATE products SET stock = stock - 1 WHERE productid = 1304,30
11/Oct/2025 22:53:55,Query,"INSERT INTO users (username, password, fname, lname, email) VALUES (...)",21
24/Oct/2025 00:36:35,Connect,admin on BCG using TCP/IP,
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

3. **Customization options:**
   Edit `generate_course_data.py` to modify:
   - **Days of data:** Change `days=30` in `__init__`
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
# Verify all data loaded
index=main earliest=-30d
| stats count by sourcetype, host

# Expected results:
# - access_combined_wcookie, web_application: ~131K events
# - linux_secure, web_server: ~64K events
# - db_audit, database: ~44K events
```

### Detailed Instructions
See `Lab1_Data_Loading.md` for complete upload instructions.

## Important Notes

- ⚠️ **products.csv is static** - Do not regenerate; used as lookup table
- 📊 **30 days of historical data** - Timestamps span 30 days back from generation time
- 🔄 **Re-upload required** - After regenerating data, must re-upload to Splunk
- 🎯 **Lab alignment** - Data patterns designed specifically for lab exercises
- 🔒 **Synthetic data only** - All IPs, usernames, and data are fake/synthetic

## Troubleshooting

### "No events found" in Splunk
- Check time range is set to "All time" or "Last 30 days"
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
