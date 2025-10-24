# Lab 1: Data Loading and Environment Setup

## Learning Objectives
By completing this lab, you will:
- Upload data files to Splunk Enterprise
- Configure source types for different data formats
- Set host field values for data identification
- Understand the data ingestion workflow
- Verify successful data ingestion

## Prerequisites
- Access to Splunk Enterprise instance (provided)
- Administrative access to Splunk Web interface
- Lab data files (already provided in data folder)

## Lab Environment
- **Splunk Version:** Enterprise (latest stable)
- **User Account:** admin
- **Password:** password
- **Default Index:** main

---

## Scenario
You have recently joined the team at Buttercup Games as a Splunk Administrator. Your first assignment is to ingest three critical data sources into your Splunk Enterprise instance for security monitoring and analysis:
1. Web application access logs
2. Linux secure logs from web servers
3. Database audit logs

These datasets cover 30 days of historical data that will be used for training and analysis purposes.

---

## Task 1: Verify Lab Data Files

### Overview
The lab data files are already provided in your course materials folder for this exercise.

### Steps:

1. **Locate the lab data directory:**
   Navigate to the `data` folder in your course materials directory

2. **Verify the following files are present:**
   - `access_30DAY.log` (Web application logs)
   - `linux_s_30DAY.log` (Linux secure logs)
   - `db_audit_30DAY.csv` (Database audit logs)
   - `products.csv` (Product lookup data for later labs)

3. **Note about the data:**
   - These files contain 30 days of historical data
   - The data is static (not real-time) for training purposes
   - You will use these same files throughout the course

### Checkpoint ✓
- [ ] Located the course data directory
- [ ] Verified access_30DAY.log is present
- [ ] Verified linux_s_30DAY.log is present
- [ ] Verified db_audit_30DAY.csv is present
- [ ] Verified products.csv is present

---

## Task 2: Ingest Web Application Data

### Overview
You will upload web application access logs that contain HTTP requests, response codes, and user session information.

### Steps:

1. **Access Splunk Web Interface:**
   - Open your browser
   - Navigate to your Splunk instance: `http://localhost:8000`
   - Log in with username: `admin` and password: `password`

2. **Navigate to Add Data:**
   - Click **Settings** in the top menu
   - Select **Add Data**
   
   > **Note:** If you don't see the Add Data option, ensure you're logged in as admin

3. **Begin Upload Process:**
   - On the Add Data page, click **Upload**
   - Click **Select File**
   - Browse to your course materials `data` folder
   - Select `access_30DAY.log`
   - Click **Open**

4. **Review Source Type Detection:**
   - Splunk will analyze the file
   - Verify it automatically detected source type as `access_combined_wcookie`
   - Review the preview pane showing parsed events
   - Click **Next**

5. **Configure Input Settings:**
   - **Host field value:** Enter `web_application`
   - Leave Index as `Default`
   - Click **Review**

6. **Review and Submit:**
   - Verify the following settings:
     - Input Type: Uploaded File
     - File Name: access_30DAY.log
     - Source Type: access_combined_wcookie
     - Host: web_application
     - Index: Default
   - Click **Submit**

7. **Verify Upload:**
   - Wait for the progress bar to complete
   - You should see "File has been uploaded successfully"
   - Click **Start Searching** to verify data

8. **Quick Validation Search:**
   ```spl
   index=main host=web_application earliest=-30d
   | stats count
   ```
   - Verify you see events from the uploaded file

### Checkpoint ✓
- [ ] Successfully logged into Splunk
- [ ] File uploaded without errors
- [ ] Source type correctly identified
- [ ] Host field set to web_application
- [ ] Events visible in search

---

## Task 3: Ingest Linux Secure Logs

### Overview
Upload Linux secure logs containing authentication and security events from web servers.

### Steps:

1. **Return to Add Data:**
   - Click **Add More Data** from the success screen
   - Or navigate: **Settings** → **Add Data** → **Upload**

2. **Select Linux Log File:**
   - Click **Select File**
   - Choose `linux_s_30DAY.log`
   - Click **Open**

3. **Configure Source Type:**
   - Notice Splunk shows source type as `default`
   - Click the **Source type** dropdown button
   - In the search box, type "linux_secure" or navigate to:
     - Expand **Operating System** category
     - Select **linux_secure**
   - Verify the preview updates with proper field extraction
   - Click **Next**

4. **Set Input Configuration:**
   - **Host field value:** Enter `web_server`
   - Keep Index as `Default`
   - Click **Review**

5. **Submit Configuration:**
   - Verify settings:
     - File Name: linux_s_30DAY.log
     - Source Type: linux_secure
     - Host: web_server
     - Index: Default
   - Click **Submit**

6. **Validation Search:**
   ```spl
   index=main host=web_server sourcetype=linux_secure earliest=-30d
   | head 10
   ```

### Checkpoint ✓
- [ ] Source type manually configured
- [ ] Host field set to web_server
- [ ] Events properly parsed
- [ ] Authentication events visible

---

## Task 4: Ingest Database Audit Logs

### Overview
Upload CSV-formatted database audit logs and create a custom source type.

### Steps:

1. **Start Upload Process:**
   - Click **Add More Data** from the success screen
   - Or navigate: **Settings** → **Add Data** → **Upload**
   - Click **Select File**
   - Choose `db_audit_30DAY.csv`
   - Click **Open**

2. **Create Custom Source Type:**
   - Splunk detects source type as `csv`
   - Click **Save As** button (next to source type)
   - In the modal window, enter:
     - **Name:** `db_audit`
     - **Description:** `Postgres Database Audit Logs`
     - **Category:** Select `Database`
     - **App:** Keep as `system`
   - Click **Save**

3. **Review Field Extraction:**
   - Verify the preview shows proper column headers
   - Confirm fields are properly extracted
   - Click **Next**

4. **Configure Input Settings:**
   - **Host field value:** Enter `database`
   - Index: `Default`
   - Click **Review**

5. **Final Submission:**
   - Verify all settings:
     - File Name: db_audit_30DAY.csv
     - Source Type: db_audit
     - Host: database
     - Index: Default
   - Click **Submit**

6. **Verify with Search:**
   ```spl
   index=main sourcetype=db_audit host=database earliest=-30d
   | table _time, Time, Type, Command, Duration
   | head 10
   ```

### Checkpoint ✓
- [ ] Custom source type created
- [ ] CSV fields properly extracted
- [ ] Host field set to database
- [ ] Tabular data displays correctly

---

## Task 5: Verify All Data Sources

### Overview
Confirm all three data sources are properly ingested and searchable.

### Steps:

1. **Run Summary Search:**
   ```spl
   index=main earliest=-30d latest=now
   | stats count by sourcetype, host
   | sort -count
   ```

2. **Expected Results:**
   You should see three rows:
   - sourcetype=access_combined_wcookie, host=web_application
   - sourcetype=linux_secure, host=web_server
   - sourcetype=db_audit, host=database

3. **Check Time Range Coverage:**
   ```spl
   index=main earliest=-30d latest=now
   | stats earliest(_time) as earliest, latest(_time) as latest by sourcetype
   | eval earliest=strftime(earliest, "%Y-%m-%d %H:%M:%S")
   | eval latest=strftime(latest, "%Y-%m-%d %H:%M:%S")
   ```

4. **Field Discovery Check:**
   ```spl
   index=main sourcetype=access_combined_wcookie | head 1
   ```
   - Click on the event
   - Verify you can see extracted fields like status, clientip, method

### Checkpoint ✓
- [ ] All three source types visible
- [ ] Event counts reasonable
- [ ] 30-day time range confirmed
- [ ] Fields properly extracted

---

## Troubleshooting Guide

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| "Add Data" option not visible | Log out and log back in with admin credentials |
| Source type not auto-detected | Manually select from the source type menu |
| No events in search | Check time range picker is set to "Last 30 days" |
| Fields not extracted in CSV | Ensure first row contains headers, re-upload if needed |
| Upload fails with size error | Check available disk space on Splunk server |
| Browser timeout during upload | Use Chrome/Firefox, disable aggressive timeout settings |

### Getting Help
1. Check the Splunk UI for error messages
2. Review `index=_internal` for ingestion errors
3. Verify file permissions and formats
4. Ask instructor for assistance

---

## Lab Summary

### What You Accomplished
✅ Located and verified sample data files  
✅ Successfully uploaded three different data types  
✅ Configured appropriate source types  
✅ Set identifying host values  
✅ Verified data ingestion through searches  
✅ Created a custom source type for database audit logs  

### Key Concepts Covered
- **Data Ingestion Methods:** File upload through Splunk Web
- **Source Types:** Automatic detection and manual configuration
- **Host Field:** Identifying data sources
- **Index Selection:** Using default index for training
- **Data Verification:** Using SPL to confirm ingestion

### Skills Developed
1. Navigating Splunk Web interface
2. Uploading data files
3. Configuring source types
4. Creating custom source types
5. Basic SPL search commands
6. Data validation techniques

---

## Next Steps

In the next lab, you will:
- Learn basic search commands
- Work with time ranges
- Filter and transform the data you just loaded
- Create your first saved searches

---

**End of Lab 1** | **Continue to Lab 2** →

## Clean-up Instructions

**Note:** Do NOT clean up data for this course as it will be used in subsequent labs.

If you need to reset your environment later:
1. Navigate to Settings → Indexes
2. Clean the main index events (instructor will demonstrate if needed)
3. Re-run this lab to reload data

---

## Additional Notes

- The data loaded in this lab represents 30 days of historical data
- These datasets will be used throughout the course
- Real-time data ingestion will be covered in advanced courses
- Keep note of the host values you assigned - you'll need them in future labs

**Congratulations on completing Lab 1!** 🎉