# Lab 4: Basic Splunk Commands

## Learning Objectives
After completing this lab, you will be able to:
- Use the `fields` command to optimize search performance and focus on relevant data
- Create organized tabular reports using the `table` command
- Rename fields for better readability and alignment with business terminology
- Remove duplicate records using the `dedup` command for accurate analysis
- Build complete search pipelines combining multiple commands
- Apply performance optimization best practices
- Create actionable reports for marketing campaign analysis

## Prerequisites
- Splunk environment running and accessible
- Sample data loaded (completed Lab 1)
- Field usage skills (completed Lab 3)
- Understanding of search pipelines and command chaining

## Lab Scenario
The Marketing team tracks all user sessions related to marketing campaigns. They need a report of all unique user sessions that include purchase actions so they can measure the effectiveness of different campaigns and assign proper value to their marketing investments.

## Data Sources
This lab focuses on web application data:
- **Web Application** (sourcetype: `access_combined_wcookie`)
  - Key fields: action, bytes, categoryId, clientip, itemId, JSESSIONID, productId, referer, referer_domain, status, useragent, file

---

## Task 1: Search for Campaign Purchase Data

### Challenge Level
This lab uses a problem-solving approach. Try to complete each step independently before checking the solutions at the end.

### Steps:

1. **Navigate to Search Interface**
   - Access Search & Reporting app
   - Set time range to **All time** (required for lab dataset)

2. **Create Base Search**
   - Search for all web application events with purchase actions and successful status (200)
   - Use: `index=main sourcetype=access_combined_wcookie action=purchase status=200`

3. **Analyze File Field**
   - In the **Interesting Fields**, click on **file**
   - Notice two different files returned: `error.do` and `success.do`
   - Web development team explains:
     - `success.do`: Served when order processed successfully
     - `error.do`: Served when processing error occurs

4. **Filter for Successful Purchases Only**
   - Modify search to include only successful file processing
   - Add: `file=success.do`

5. **Optimize with Fields Command**
   - Use `fields` command to return only: action, JSESSIONID, status
   - Observe if search performance improves
   - Note how field list becomes cleaner

### Validation:
- [ ] Base search returns purchase transactions with status 200
- [ ] Identified difference between success.do and error.do files
- [ ] Filtered results to show only successful purchases
- [ ] Applied fields command to focus on relevant data
- [ ] Observed performance improvement

**Expected Search Pattern:**
```
index=main sourcetype=access_combined_wcookie action=purchase status=200 file=success.do | fields action, JSESSIONID, status
```

---

## Task 2: Create Marketing-Friendly Reports

### Steps:

1. **Convert to Table Format**
   - Replace `fields` command with `table` command
   - Display data in organized tabular format
   - Order: action, JSESSIONID, status

2. **Reorder Columns**
   - Change column order so JSESSIONID appears first
   - New order: JSESSIONID, action, status

3. **Rename for Business Alignment**
   - Marketing team uses "UserSessions" instead of "JSESSIONID"
   - Use `rename` command: `JSESSIONID as UserSessions`

4. **Sort User Sessions**
   - Add `sort UserSessions` command
   - Observe alphabetical ordering
   - Notice duplicate UserSession values
   - Check event count on Statistics tab

5. **Remove Duplicates**
   - Remove `sort` command
   - Add `dedup JSESSIONID` to eliminate duplicate sessions
   - Compare event count before and after deduplication
   - Note: Place dedup early in pipeline for best performance

6. **Final Report Optimization**
   - Remove action and status fields from table display
   - Marketing team only needs unique UserSessions list
   - Final table should show only UserSessions column

### Validation:
- [ ] Successfully created table format display
- [ ] Reordered columns with JSESSIONID first
- [ ] Renamed JSESSIONID to UserSessions
- [ ] Applied sorting and observed duplicate sessions
- [ ] Used dedup to remove duplicates
- [ ] Created clean final report with only UserSessions

**Expected Final Search Pattern:**
```
index=main sourcetype=access_combined_wcookie action=purchase status=200 file=success.do | dedup JSESSIONID | table JSESSIONID | rename JSESSIONID as UserSessions
```

---

## Progress Tracking Checklist

### Command Mastery
- [ ] Used `fields` command for performance optimization
- [ ] Applied `table` command for report formatting
- [ ] Implemented `rename` command for business alignment
- [ ] Utilized `dedup` command for data accuracy
- [ ] Combined multiple commands in search pipeline

### Search Pipeline Construction
- [ ] Built progressive search refinements
- [ ] Optimized command order for performance
- [ ] Created business-ready report format
- [ ] Verified data accuracy at each step

### Marketing Analytics
- [ ] Identified successful purchase transactions
- [ ] Filtered out error conditions
- [ ] Created unique user session list
- [ ] Prepared data for campaign value analysis

### Performance Optimization
- [ ] Applied fields command early in pipeline
- [ ] Positioned dedup command optimally
- [ ] Minimized unnecessary field processing
- [ ] Created efficient search patterns

## Key Concepts Summary

### Essential Splunk Commands

#### `fields` Command
- **Purpose**: Specify which fields to include/exclude from results
- **Performance**: Reduces data processing and improves speed
- **Syntax**: `| fields field1, field2, field3`
- **Best Practice**: Use early in search pipeline

#### `table` Command
- **Purpose**: Display results in tabular format
- **Formatting**: Creates organized, readable reports
- **Syntax**: `| table field1, field2, field3`
- **Column Order**: Fields appear in order specified

#### `rename` Command
- **Purpose**: Change field names for clarity or business alignment
- **Syntax**: `| rename old_field as new_field`
- **Multiple Renames**: `| rename field1 as newname1, field2 as newname2`
- **Business Value**: Aligns technical fields with business terminology

#### `dedup` Command
- **Purpose**: Remove duplicate records based on specified fields
- **Syntax**: `| dedup field1, field2`
- **Performance**: Place early in pipeline when possible
- **Use Cases**: Unique counts, eliminating redundant data

### Search Pipeline Best Practices

#### Command Ordering
1. **Filter Early**: Use search terms and WHERE clauses first
2. **Dedup Early**: Remove duplicates before expensive operations
3. **Fields Selection**: Limit fields early to improve performance
4. **Transform Last**: Apply formatting commands at the end

#### Performance Optimization
- Minimize data early in pipeline
- Use specific field filters
- Avoid unnecessary sorting operations
- Position dedup strategically

### Marketing Analytics Applications

#### Campaign Measurement
- Track unique user engagement
- Measure conversion rates
- Analyze customer journey stages
- Calculate return on marketing investment

#### Session Analysis
- Identify unique user sessions
- Track purchase completion rates
- Analyze user behavior patterns
- Measure campaign effectiveness

## Real-World Applications

### E-commerce Analytics
```splunk
# Track unique customers making purchases by product category
index=main sourcetype=access_combined_wcookie action=purchase status=200 
| dedup JSESSIONID, productId 
| table JSESSIONID, productId, categoryId 
| rename JSESSIONID as CustomerSession
```

### Marketing Campaign Performance
```splunk
# Analyze unique sessions per marketing campaign
index=main sourcetype=access_combined_wcookie action=purchase
| dedup JSESSIONID
| stats count by referer
| rename referer as "Campaign Source", count as "Unique Sessions"
```

### Customer Journey Analysis
```splunk
# Track customer actions throughout session
index=main sourcetype=access_combined_wcookie JSESSIONID=specific_session
| table _time, action, productId, status
| sort _time
```

## Troubleshooting

### Common Issues

**Fields command not improving performance:**
- Verify fields are actually being excluded
- Check if downstream commands require excluded fields
- Consider field extraction overhead vs. benefit
- Monitor search inspector for performance metrics

**Table formatting issues:**
- Verify field names exist in data
- Check for typos in field references
- Ensure fields have values in result set
- Use `fieldformat` for display formatting if needed

**Dedup not removing expected duplicates:**
- Verify field names are correct
- Check if fields contain slight variations
- Consider case sensitivity issues
- Use `stats` with `values()` for complex deduplication

**Rename command not working:**
- Confirm original field name exists
- Check for case sensitivity
- Verify field has values in results
- Use `eval` for complex field transformations

### Performance Issues

**Slow search execution:**
- Move filters earlier in search
- Use more specific search terms
- Limit time ranges appropriately
- Consider summary indexes for repeated searches

**Memory or resource errors:**
- Reduce field count with `fields` command
- Implement earlier deduplication
- Use more restrictive base search
- Consider search job parallelization

### Windows/Mac Compatibility Notes

**Windows Users:**
- Copy/paste search commands using Ctrl+C/Ctrl+V
- Use Windows-style line breaks if creating saved searches
- PowerShell available for any scripting needs
- Check browser performance with large result sets

**Mac Users:**
- Copy/paste search commands using Cmd+C/Cmd+V
- Use Unix-style line breaks in search macros
- Terminal available for command line operations
- Monitor browser memory usage with large datasets

**Both Platforms:**
- Enable browser JavaScript for full functionality
- Clear cache if command completion issues occur
- Use modern browsers for best performance
- Consider browser zoom for table readability

## Validation Exercises

### Exercise 1: Independent Search Creation
Create a search to find unique user sessions that viewed product category "sports":

**Requirements:**
- Use web application data
- Filter for "view" actions in "sports" category
- Show unique sessions only
- Display as clean table with renamed fields

### Exercise 2: Performance Comparison
Compare performance of two approaches:
1. Dedup early: `base_search | dedup JSESSIONID | other_commands`
2. Dedup late: `base_search | other_commands | dedup JSESSIONID`

Measure and explain the difference.

### Exercise 3: Business Report Creation
Create a marketing report showing:
- Unique user sessions per hour
- Only successful purchases
- Formatted for executive presentation

## Extension Activities

### Advanced Command Combinations
- Use `stats` with `dedup` for complex aggregations
- Combine `eval` with `rename` for calculated fields
- Apply `where` filters after table creation
- Use `sort` with multiple fields and directions

### Marketing Intelligence Enhancements
- Add time-based analysis with `timechart`
- Include geographical data with location fields
- Calculate conversion rates using `eventstats`
- Create executive dashboards with formatted tables

### Data Quality Improvements
- Implement field validation with `where` commands
- Add data completeness checks
- Create data profiling searches
- Build automated quality monitoring

## Cleanup Instructions

1. **Clear Search Interface**
   - Remove search criteria from search bar
   - Reset time range to default (Last 24 hours)
   - Clear any selected fields or filters

2. **Verify Search History**
   - Review Activity > Jobs for completed searches
   - Keep successful searches for reference
   - Clean up any failed or unnecessary searches

3. **Document Key Searches**
   - Save effective search patterns as references
   - Note performance improvements observed
   - Record business insights discovered

## Next Steps

This lab covered fundamental Splunk commands for data manipulation and reporting. 

---

## 🎯 End of Day 1

**Congratulations!** You have completed Day 1 of the Splunk Fundamentals course.

### Day 1 Summary
✅ **Lab 1**: Data Loading and Environment Setup  
✅ **Lab 2**: Basic Searching with Splunk Search Language  
✅ **Lab 3**: Using Fields in Searches  
✅ **Lab 4**: Basic Splunk Commands  

### Tomorrow (Day 2)
Day 2 will focus on advanced analysis and reporting:
- **Lab 5**: Transforming Commands (statistical analysis)
- **Lab 6**: Reports and Dashboards (visualization)
- **Lab 7**: Pivot and Datasets (business user tools)
- **Lab 8**: Lookups (data enrichment)
- **Lab 9**: Alerts (proactive monitoring)

## Solutions Section

### Task 1 Solutions

**Step 2 - Base Search:**
```splunk
index=main sourcetype=access_combined_wcookie action=purchase status=200
```

**Step 4 - Filter for Success:**
```splunk
index=main sourcetype=access_combined_wcookie action=purchase status=200 file=success.do
```

**Step 5 - Add Fields Command:**
```splunk
index=main sourcetype=access_combined_wcookie action=purchase status=200 file=success.do | fields action, JSESSIONID, status
```

### Task 2 Solutions

**Step 1 - Table Format:**
```splunk
index=main sourcetype=access_combined_wcookie action=purchase status=200 file=success.do | table action, JSESSIONID, status
```

**Step 2 - Reorder Columns:**
```splunk
index=main sourcetype=access_combined_wcookie action=purchase status=200 file=success.do | table JSESSIONID, action, status
```

**Step 3 - Rename Field:**
```splunk
index=main sourcetype=access_combined_wcookie action=purchase status=200 file=success.do | table JSESSIONID, action, status | rename JSESSIONID as UserSessions
```

**Step 4 - Sort Sessions:**
```splunk
index=main sourcetype=access_combined_wcookie action=purchase status=200 file=success.do | table JSESSIONID, action, status | rename JSESSIONID as UserSessions | sort UserSessions
```

**Step 5 - Remove Duplicates:**
```splunk
index=main sourcetype=access_combined_wcookie action=purchase status=200 file=success.do | dedup JSESSIONID | table JSESSIONID, action, status | rename JSESSIONID as UserSessions
```

**Step 6 - Final Report:**
```splunk
index=main sourcetype=access_combined_wcookie action=purchase status=200 file=success.do | dedup JSESSIONID | table JSESSIONID | rename JSESSIONID as UserSessions
```

## Additional Resources

- Splunk Search Command Reference
- Search Performance Optimization Guide
- Marketing Analytics Best Practices
- Data Deduplication Strategies
- Business Intelligence Reporting Techniques