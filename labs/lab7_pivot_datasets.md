# Lab 7: Using Pivot and Datasets in Splunk
*Day 2 - Lab 3 of 5*

## Duration: 90 minutes

## Lab Overview

In this lab, you will learn to use Splunk's Pivot interface to create visualizations without writing complex searches. You'll build reports for business users using the drag-and-drop Pivot interface, create datasets for reusable analysis, and understand how Pivot transforms raw data into meaningful insights.

## Learning Objectives

By the end of this lab, you will be able to:

- Access and use the Instant Pivot feature from search results
- Build reports using the Pivot interface with filters and splits
- Create visualizations using Split Rows and Split Columns
- Apply multiple filters to refine data analysis
- Save Pivot reports as dashboard panels
- Create and manage datasets from search results
- Navigate between Datasets, Pivot, and Search interfaces
- Understand the relationship between Pivot and data models

## Prerequisites

- Completed Labs 1-6
- Understanding of basic Splunk search commands
- Familiarity with creating dashboards
- Basic knowledge of data visualization concepts

## Lab Environment Setup

### Step 1: Verify Sample Data

Ensure required sample data is loaded:

```spl
index=main earliest=-30d latest=now
| stats count by sourcetype
```

Required sourcetypes:
- `access_combined_wcookie` - Web application logs with referrer data
- `db_audit` - Database audit logs
- `linux_secure` - Linux security logs

### Step 2: Verify Dashboard

Ensure the Sales Dashboard from Lab 6 exists:
1. Navigate to **Dashboards**
2. Look for "Sales Dashboard"
3. If missing, create a new dashboard with this name

## Key Concepts

### Pivot Interface

**What is Pivot?**
- Visual interface for creating reports without SPL knowledge
- Drag-and-drop functionality for non-technical users
- Automatically generates underlying searches
- Built on top of data models for performance

### Pivot Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **Filters** | Limit data to specific criteria | file=cart.do |
| **Split Rows** | Group data by field values (Y-axis) | productId |
| **Split Columns** | Create data series (X-axis) | referrer_domain |
| **Values** | Metrics to calculate | Count, Sum, Average |

### Datasets vs Data Models

**Datasets**
- Simplified data models for specific use cases
- Created from search results
- Easier to manage than full data models
- Good for departmental reporting

**Data Models**
- Enterprise-wide data structures
- Support complex relationships
- Better performance for large-scale reporting
- Require more planning and maintenance

---

## Exercise 1: Customer Referral Analysis

**Scenario**: The CFO wants to know where customers are coming from when they add items to their shopping cart.

### Task 1.1: Access Instant Pivot

Start with a basic search:

```spl
index=main sourcetype=access_combined_wcookie
```

1. Run the search for **All time**
2. Click the **Visualization** tab
3. Observe three icons:
   - **Pivot** - Build tables and visualizations
   - **Quick Reports** - Pre-built report templates
   - **Search Command** - Return to search

### Task 1.2: Launch Pivot Interface

1. Click the **Pivot** icon
2. In the modal window:
   - Select **All Fields**
   - Click **OK**

**✓ Checkpoint**: Pivot interface opens with field list on left

### Task 1.3: Filter for Cart Activity

Under **Filters**:
1. Click **+** to add a filter
2. Select **file** from the Fields list
3. Configure filter:
   - **Filter Type**: Match
   - **Match**: is → `cart.do`
4. Click **Add To Table**

**Expected Result**: Table shows only cart.do events

### Task 1.4: Add Product Breakdown

Under **Split Rows**:
1. Click **+** to add split rows
2. Select **productId** field
3. Configure:
   - **Label**: `Product Added To Cart`
   - Keep other defaults
4. Click **Add To Table**

**✓ Checkpoint**: Products appear as rows with counts

### Task 1.5: Add Referrer Analysis

Under **Split Columns**:
1. Click **+** to add split columns
2. Select **referrer_domain** field
3. Keep default settings
4. Click **Add To Table**

**Observation**: Notice buttercupgames.com dominates the traffic

### Task 1.6: Filter Out Internal Traffic

Add another filter to exclude internal traffic:

Under **Filters**:
1. Click **+** to add another filter
2. Select **referrer_domain** from Fields list
3. Configure:
   - **Filter Type**: Match
   - **Match**: is not → `http://www.buttercupgames.com`
4. Click **Add To Table**

**Expected Results**: External referrer domains now visible

### Task 1.7: Change Visualization

1. Use the black sidebar on the left
2. Select **Line Chart** visualization
3. Observe the trend visualization

**✓ Checkpoint**: Line chart shows product additions by external referrer over time

---

## Exercise 2: Save to Dashboard and Create Dataset

### Task 2.1: Save as Dashboard Panel

1. Click **Save As** → **Dashboard Panel**
2. Notice the data model fields:
   - **Model Title**: (Currently empty - will create new)
   - **Model ID**: (Will be auto-generated)
3. Configure:
   - **Dashboard**: Existing
   - **Dashboard Title**: Sales Dashboard
   - **Panel Title**: `Sales By Referral Domain`
   - **Model Title**: `Web Application Dataset`
   - **Model ID**: `web_app_ds`
4. Click **Save**
5. Click **View Dashboard**

**✓ Checkpoint**: New panel added to Sales Dashboard

### Task 2.2: Access Your Dataset

1. Click **Datasets** menu on the top bar
2. Click **Yours** filter to show only your datasets
3. Find "Web Application Dataset" in the list
4. From the **Actions** menu, select **Explore** → **Visualize with Pivot**

**✓ Checkpoint**: Dataset opens in Pivot interface

### Task 2.3: Explore Dataset Capabilities

Using your dataset, create a new analysis:

1. **Clear** any existing configuration
2. Add Filter:
   - Field: **status**
   - Match: is → `200`
3. Split Rows:
   - Field: **file**
   - Label: `Page Type`
4. Split Columns:
   - Field: **_time**
   - Period: Auto
5. Select **Column Chart** visualization

---

## Exercise 3: Advanced Pivot Analysis

**Scenario**: Create a comprehensive traffic analysis showing user behavior patterns.

### Task 3.1: Browser Usage Analysis

Starting from Pivot with your dataset:

1. **Filters**:
   - file → is → `success.do`
2. **Split Rows**:
   - useragent → Label: `Browser`
3. **Split Columns**:
   - productId → Limit: 5
4. Select **Pie Chart** visualization

### Task 3.2: Geographic Analysis

Create location-based insights:

1. **Filters**:
   - status → is → `200`
2. **Split Rows**:
   - clientip → Label: `Client Location`
3. **Values**:
   - Count (default)
   - Add: Sum of bytes → Label: `Bandwidth`
4. Select **Statistics Table**

### Task 3.3: Time-Based Patterns

Analyze traffic patterns over time:

1. **Split Columns**:
   - _time → Period: 1 day
2. **Split Rows**:
   - action → Label: `User Action`
3. Select **Area Chart** visualization

---

## Challenge Exercises

### Challenge 1: Multi-Dimensional Analysis

Create a pivot report showing:
- Products purchased (rows)
- By referrer domain (columns)
- Filtered for successful transactions only
- Excluding internal traffic
- As a heat map visualization

### Challenge 2: Performance Dashboard

Build a complete dashboard using only Pivot:

1. **Panel 1**: Top browsers by traffic volume
2. **Panel 2**: Failed transactions by error code
3. **Panel 3**: Bandwidth consumption by file type
4. **Panel 4**: User sessions by hour of day

### Challenge 3: Dataset Optimization

Create an optimized dataset:
1. Start with a filtered search (status=200)
2. Include only necessary fields
3. Add calculated fields for session duration
4. Save as a new dataset for team use

---

## Working with Datasets

### Dataset Management

| Action | Purpose | Access Point |
|--------|---------|--------------|
| **Create** | Build from search results | Save As → Dataset |
| **Edit** | Modify fields and filters | Datasets → Manage |
| **Share** | Set permissions | Datasets → Permissions |
| **Delete** | Remove unused datasets | Datasets → Actions → Delete |

### Best Practices

1. **Naming Conventions**:
   - Use descriptive names
   - Include department/team prefix
   - Version datasets when updating

2. **Field Selection**:
   - Include only necessary fields
   - Add calculated fields in dataset
   - Document field purposes

3. **Performance**:
   - Limit time range where possible
   - Use acceleration for large datasets
   - Regular maintenance and cleanup

---

## Pivot Interface Reference

### Filter Options

| Filter Type | Use Case | Example |
|------------|----------|---------|
| **Match** | Exact value matching | file = cart.do |
| **Does not match** | Exclusion | status != 200 |
| **Contains** | Partial string match | url contains "admin" |
| **Is null** | Missing values | referrer is null |
| **In range** | Numeric ranges | bytes 1000-5000 |

### Split Options

| Split Type | Purpose | Best For |
|-----------|---------|----------|
| **Split Rows** | Y-axis grouping | Categories, products |
| **Split Columns** | X-axis series | Time, locations |
| **Split by** | Color coding | Status, severity |

### Visualization Selection Guide

```
Data Pattern → Recommended Visualization
├── Trends over time → Line/Area Chart
├── Category comparison → Column/Bar Chart
├── Part of whole → Pie/Donut Chart
├── Multi-dimensional → Heat Map
├── Statistical summary → Statistics Table
└── Single metric → Single Value
```

---

## Troubleshooting Guide

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| No data in Pivot | Check time range and filters |
| Fields not appearing | Ensure "All Fields" is selected |
| Visualization not updating | Click "Apply" after changes |
| Cannot save dataset | Check write permissions |
| Pivot running slowly | Consider data model acceleration |

### Performance Tips

1. **Use Filters First**: Apply filters before splits to reduce data
2. **Limit Split Values**: Use "Limit" option for large cardinality fields
3. **Time Range**: Use specific time ranges instead of "All time"
4. **Dataset Acceleration**: Enable for frequently used datasets

---

## Cleanup

To clean up after this lab:

1. **Remove Dataset**:
   - Navigate to Datasets
   - Find "Web Application Dataset"
   - Select Delete from Actions menu

2. **Remove Dashboard Panel** (optional):
   - Open Sales Dashboard
   - Click Edit
   - Remove "Sales By Referral Domain" panel
   - Save dashboard

---

## Key Takeaways

✅ **You've learned to:**
- Use Instant Pivot from search results
- Build complex reports without writing SPL
- Create and manage datasets for reusable analysis
- Apply multiple filters and splits in Pivot
- Choose appropriate visualizations for different data patterns
- Save Pivot reports to dashboards
- Navigate between Datasets and Pivot interfaces

## Next Steps

- Proceed to Lab 8: Scheduling Reports and Alerts
- Explore data model creation and acceleration
- Learn about Pivot table calculations and formatting

---

## Quick Reference

### Pivot Workflow

1. **Access Pivot**:
   - From Search: Visualization tab → Pivot
   - From Dataset: Datasets → Visualize with Pivot
   - From Data Model: Settings → Data models → Pivot

2. **Build Report**:
   - Add Filters → Define criteria
   - Add Splits → Group data
   - Select Values → Choose metrics
   - Pick Visualization → Display results

3. **Save Options**:
   - Save as Report
   - Save as Dashboard Panel
   - Save as Dataset (from search)

### Common Pivot Patterns

| Analysis Type | Filters | Split Rows | Split Columns |
|--------------|---------|------------|---------------|
| Product Sales | file=success.do | productId | _time |
| Traffic Sources | status=200 | referrer_domain | date_hour |
| Error Analysis | status>=400 | status | file |
| User Behavior | - | action | clientip |

---

## Answer Key

<details>
<summary>Click to reveal answers</summary>

### Exercise 1
- Most cart additions come from: google.com, yahoo.com, bing.com
- Top products added to cart: BS-AG-G09, CU-PG-G06, DB-SG-G01

### Exercise 2
- Dataset created: web_app_ds
- Panel added: Sales By Referral Domain

### Dataset Fields
- Key fields: file, productId, referrer_domain, status, clientip
- Time field: _time

</details>