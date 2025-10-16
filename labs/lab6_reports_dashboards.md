# Lab 6: Creating Reports and Dashboards in Splunk
*Day 2 - Lab 2 of 5*

## Lab Overview

In this lab, you will build reports and dashboards for various stakeholders at Buttercup Games. You'll learn how to save searches as reports, create visualizations, build interactive dashboards, and manage permissions to share your work with others.

## Learning Objectives

By the end of this lab, you will be able to:

- Create and save reports from search results
- Configure report permissions and sharing settings
- Build interactive dashboards with multiple panels
- Create different visualization types (charts, single values, tables)
- Arrange and customize dashboard layouts
- Use the visualization editor to select appropriate chart types
- Add panels to existing dashboards
- Navigate between search, visualization, and dashboard views

## Prerequisites

- Completed Labs 1-5
- Understanding of Splunk search syntax and transforming commands
- Familiarity with stats functions (count, sum, avg, etc.)
- Basic knowledge of field extraction

## Lab Environment Setup

### Step 1: Verify Sample Data

Ensure you have the required sample data loaded:

```spl
index=main earliest=-30d latest=now
| stats count by sourcetype
```

Required sourcetypes:
- `access_combined_wcookie` - Web application logs
- `db_audit` - Database audit logs
- `linux_secure` - Linux security logs

### Step 2: Search Settings

For all exercises:
1. Navigate to **Search & Reporting** app
2. Set time range to **All time**
3. Use the `main` index

> **Note**: Searching "All time" is not a production best practice but necessary for our limited dataset.

## Key Concepts

### Reports vs Dashboards

**Reports**
- Saved searches that can be run on demand
- Can include visualizations
- Shareable with specific permissions
- Can be scheduled for regular execution

**Dashboards**
- Collections of visualizations and reports
- Interactive panels with drill-down capabilities
- Real-time or scheduled data updates
- Customizable layouts and styling

### Visualization Types

| Type | Best For | Example Use Case |
|------|----------|------------------|
| Column Chart | Comparing categories | Product sales by ID |
| Single Value | KPIs and metrics | Total sales count |
| Line Chart | Trends over time | Daily transaction volume |
| Pie Chart | Part-to-whole relationships | Traffic by browser type |
| Table | Detailed data display | IP addresses with attempt counts |

---

## Exercise 1: Security Report - Forbidden Access Attempts

**Scenario**: The security team needs a report of IP addresses attempting to access forbidden pages.

### Task 1.1: Search for Forbidden Access

Find all web application events with forbidden status (403):

```spl
index=main sourcetype=access_combined_wcookie status=403
```

**Expected Results**: Events showing forbidden access attempts

### Task 1.2: Count Attempts by IP

Add statistics to count attempts by client IP:

```spl
index=main sourcetype=access_combined_wcookie status=403 
| stats count as attempts by clientip
```

### Task 1.3: Sort Results

Display IPs with highest attempts first:

```spl
index=main sourcetype=access_combined_wcookie status=403 
| stats count as attempts by clientip 
| sort -attempts
```

**✓ Checkpoint**: Record the IP with most attempts: ___________ (Total attempts: ___________)

### Task 1.4: Save as Report

1. Click **Save As** → **Report**
2. Enter report details:
   - **Title**: `403_by_clientip`
   - **Description**: `Security report showing IPs with forbidden access attempts`
   - **Content**: Statistics Table
   - **Time Range Picker**: Yes

3. Click **Save**

### Task 1.5: Set Permissions

1. Click **Permissions** link
2. Configure settings:
   - **Display For**: App
   - **Run As**: Owner
   - **Read**: Everyone
   - **Write**: Power, Admin

3. Click **Save**

### Task 1.6: Verify Report

1. Navigate to **Reports** menu
2. Find `403_by_clientip` in the list
3. Click to run the report

**✓ Checkpoint**: Report successfully created and accessible

---

## Exercise 2: Sales Dashboard - Product Performance

**Scenario**: The CFO needs a dashboard showing product sales performance in one centralized location.

### Task 2.1: Create Product Sales Visualization

Search for successful purchases:

```spl
index=main sourcetype=access_combined_wcookie 
  file=success.do 
  status=200
```

### Task 2.2: Add Statistics

Count sales by product:

```spl
index=main sourcetype=access_combined_wcookie 
  file=success.do 
  status=200 
| stats count by productId
```

### Task 2.3: Create Column Chart

1. Click **Visualization** tab
2. Select **Column Chart** from Splunk Visualizations
3. Review the chart display

### Task 2.4: Save to New Dashboard

1. Click **Save As** → **Dashboard Panel**
2. Configure settings:
   - **Dashboard**: New
   - **Dashboard Title**: `Sales Dashboard`
   - **Panel Title**: `Product Sales`
   - **Panel Description**: `Sales count by product ID`

3. Click **Save**
4. Click **View Dashboard**

**✓ Checkpoint**: Dashboard created with Product Sales panel

### Task 2.5: Add Total Sales Panel

1. Click **Open in Search** icon at bottom of Product Sales panel
2. Modify search to remove the `by` clause:

```spl
index=main sourcetype=access_combined_wcookie 
  file=success.do 
  status=200 
| stats count
```

3. Click **Visualization** tab
4. Select **Single Value** visualization
5. Click **Save As** → **Dashboard Panel**
6. Configure:
   - **Dashboard**: Existing
   - **Dashboard Title**: Sales Dashboard
   - **Panel Title**: `Total Units Sold`

7. Click **Save** → **View Dashboard**

### Task 2.6: Arrange Dashboard Layout

1. Click **Edit** button on dashboard
2. Click and hold the bar at top of **Total Units Sold** panel
3. Drag panel to top position
4. Click **Save**

**✓ Checkpoint**: Dashboard displays Total Units Sold prominently at top

---

## Exercise 3: Enhanced Dashboard Panels

**Scenario**: Add more analytical panels to provide comprehensive sales insights.

### Task 3.1: Top 5 Products Panel

Create a focused view of best sellers:

```spl
index=main sourcetype=access_combined_wcookie 
  file=success.do 
  status=200 
| top limit=5 productId showperc=false
```

1. Select **Pie Chart** visualization
2. Save to existing Sales Dashboard
3. Panel Title: `Top 5 Products`

### Task 3.2: Daily Sales Trend

Show sales over time:

```spl
index=main sourcetype=access_combined_wcookie 
  file=success.do 
  status=200 
| timechart span=1d count as Sales
```

1. Select **Line Chart** visualization
2. Save to existing Sales Dashboard
3. Panel Title: `Daily Sales Trend`

### Task 3.3: Customer Activity

Track unique customers:

```spl
index=main sourcetype=access_combined_wcookie 
  file=success.do 
  status=200 
| stats dc(clientip) as "Unique Customers", 
        count as "Total Purchases" 
| eval "Avg Purchases per Customer"=round('Total Purchases'/'Unique Customers',2)
```

1. Select **Single Value** visualization with Trellis
2. Save to existing Sales Dashboard
3. Panel Title: `Customer Metrics`

---

## Challenge Exercises

### Challenge 1: Security Dashboard

Create a comprehensive security dashboard with:

1. **Failed Login Attempts Panel**:
```spl
index=main sourcetype=linux_secure "Failed password"
| stats count by process
| sort -count
```

2. **404 Error Tracking**:
```spl
index=main sourcetype=access_combined_wcookie status=404
| timechart span=1h count
```

3. **Suspicious Activity Score**:
```spl
index=main sourcetype=access_combined_wcookie 
| eval suspicious=case(
    status=403, 3,
    status=404, 1,
    file="passwords.pdf", 5,
    1=1, 0)
| stats sum(suspicious) as "Risk Score" by clientip
| where 'Risk Score' > 10
```

### Challenge 2: Performance Dashboard

Build a database performance dashboard:

1. **Slow Query Monitor**:
```spl
index=main sourcetype=db_audit Duration>1000
| stats count as "Slow Queries", 
        avg(Duration) as "Avg Duration" by Command
| sort -"Avg Duration"
```

2. **Query Type Distribution**:
```spl
index=main sourcetype=db_audit
| stats count by Type
| eval percent=round(count*100/sum(count),2)
```

### Challenge 3: Executive Dashboard

Create a C-suite dashboard with:
- Revenue metrics (simulated using bytes field)
- Customer engagement scores
- Operational KPIs
- Trend indicators with sparklines

---

## Dashboard Best Practices

### Layout Guidelines

1. **Priority Placement**: Most important metrics at top
2. **Logical Grouping**: Related panels together
3. **Visual Hierarchy**: Single values for KPIs, charts for trends
4. **Consistent Styling**: Uniform colors and formatting

### Performance Optimization

1. **Base Searches**: Use post-process searches for related panels
2. **Time Range**: Set appropriate refresh intervals
3. **Data Models**: Consider using for frequently accessed data
4. **Scheduled Searches**: Pre-compute expensive searches

### Sharing and Permissions

| Permission Level | Access Rights |
|-----------------|---------------|
| Private | Only creator can view |
| App | All app users can view |
| Global | Available across all apps |

---

## Troubleshooting Guide

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Report not appearing in list | Check permissions and app context |
| Visualization not displaying | Verify data format matches chart requirements |
| Dashboard panels not loading | Check search syntax and time range |
| Cannot edit dashboard | Verify write permissions |
| Single value shows N/A | Ensure search returns single numeric value |

### Dashboard Tips

- **Panel Linking**: Use drilldown to connect related dashboards
- **Input Controls**: Add time pickers and dropdowns for interactivity
- **Auto-Refresh**: Set appropriate refresh intervals for real-time data
- **Export Options**: Enable PDF/PNG export for sharing

---

## Cleanup

This lab creates persistent objects. To clean up:

1. **Delete Reports**:
   - Navigate to Settings → Searches, reports, and alerts
   - Find and delete `403_by_clientip`

2. **Delete Dashboard**:
   - Navigate to Dashboards
   - Find and delete `Sales Dashboard`

---

## Key Takeaways

✅ **You've learned to:**
- Create and manage reports with appropriate permissions
- Build multi-panel dashboards
- Select appropriate visualizations for different data types
- Arrange and customize dashboard layouts
- Share reports and dashboards with teams

## Next Steps

- Proceed to Lab 7: Advanced Searching and Field Extraction
- Explore dashboard drilldown and form inputs
- Learn about scheduled reports and alerts

---

## Quick Reference

### Report Creation Workflow

1. Run search → Save As → Report
2. Set title and description
3. Configure permissions
4. Schedule if needed

### Dashboard Panel Types

| Panel Type | SPL Requirement | Best Practice |
|------------|-----------------|---------------|
| Single Value | Returns one numeric result | Use for KPIs |
| Chart | Returns series data | Include time or category field |
| Table | Returns tabular data | Limit rows for readability |
| Map | Returns geographic data | Include lat/lon or location fields |

### Visualization Selection Guide

```
Data Type → Recommended Visualization
├── Single Metric → Single Value
├── Categories → Column/Bar Chart
├── Time Series → Line/Area Chart
├── Part-to-Whole → Pie/Donut Chart
├── Correlation → Scatter Plot
└── Geographic → Cluster Map
```

---

## Answer Key

<details>
<summary>Click to reveal answers</summary>

### Exercise 1
- IP with most attempts: 87.194.216.51
- Total attempts: 11

### Exercise 2
- Total units sold: 16,139
- Top selling product: WC-SH-G04

### Additional Metrics
- Conversion rate: ~55% (16,139 purchases / 29,328 cart additions)
- Unique sessions: 11,455

</details>