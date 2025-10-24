# Lab 3: Using Fields in Searches

## Learning Objectives
After completing this lab, you will be able to:
- Use the Fields sidebar to examine and analyze search results
- Identify and work with interesting fields extracted by Splunk
- Select and deselect fields to customize result displays
- Filter searches using field values and comparison operators
- Navigate and utilize Search History effectively
- Manage search jobs and identify keystroke errors
- Analyze web server performance using field-based searches

## Prerequisites
- Splunk environment running and accessible
- Sample data loaded (completed Lab 1)
- Basic search skills (completed Lab 2)
- Understanding of Splunk Search Language basics

## Lab Scenario
Your web server has been experiencing downtime issues. The Director of Sales has asked your team to examine how this has affected sales on the website. You need to analyze purchase transactions and identify failed requests that prevented customers from completing their purchases.

## Data Sources
This lab focuses on web application data:
- **Web Application** (sourcetype: `access_combined_wcookie`)
  - Key fields: action, bytes, categoryId, clientip, itemId, JSESSIONID, productId, referer, referer_domain, status, useragent, file

---

## Task 1: Use the Fields Sidebar to Examine Search Results

### Steps:

1. **Navigate to Search Interface**
   - Click **Search** in the app navigation bar
   - If needed, click **App: Search & Reporting** in the Splunk bar to clear previous search

2. **Execute Purchase Transaction Search**
   - Enter search: `index=main sourcetype=access_combined_wcookie action=purchase`
   - Set time range to **All time**
   - Execute the search

3. **Verify Smart Mode**
   - After search finalizes, verify "Smart Mode" displays under time range picker
   - If not in Smart Mode, change it to Smart Mode and re-execute

4. **Explore Interesting Fields**
   - Examine the **Interesting Fields** list in the Fields sidebar
   - Locate **productId** in the interesting fields
   - Click **productId** to open the field window
   - Review the top ten purchased products by productId
   - Close the window using the **x** in upper right corner

5. **Analyze Status Field**
   - In Fields sidebar, under **Interesting Fields**, click **status**
   - Note that status codes > 200 indicate customer interaction errors
   - Review the status code distribution

6. **Select Fields for Display**
   - From the status field window, click **Yes** next to "Selected"
   - Close the window using the **x**
   - Notice **status** now appears in **Selected Fields**
   - Observe **status=value** displayed below each event

### Validation:
- [ ] Search executed successfully in Smart Mode
- [ ] Found productId in interesting fields
- [ ] Viewed top ten purchased products
- [ ] Status field selected and visible in results
- [ ] Status values displayed below each event

---

## Task 2: Filter Results Using Field Values

### Steps:

1. **Filter by Most Common Status**
   - In Fields sidebar, under **Selected Fields**, click **status**
   - Click the value with highest count (at top of list)
   - Notice field and value added to search criteria
   - Observe new search executed automatically

2. **Identify Server Errors**
   - Note most common value is likely 200 (success)
   - Since we want to see errors, modify the search
   - Change status search to: `status!=200`
   - Execute the search

3. **Analyze Error Results**
   - Review search results showing only failed purchases
   - Note the event count under the search bar
   - Record this number for reference: _______ events

4. **Remove Status from Selected Fields**
   - Click **status** in Fields sidebar
   - Select **No** next to "Selected"
   - Close field window using **x**
   - Click **search** link in Splunk Bar to clear results

### Validation:
- [ ] Successfully filtered by most common status value
- [ ] Modified search to show only error statuses (!=200)
- [ ] Identified count of purchase errors
- [ ] Removed status from selected fields
- [ ] Cleared search results

---

## Task 3: Use Search History to Browse Previous Searches

### Steps:

1. **Access Search History**
   - Click **Search History** to view past searches
   - Note difference from Jobs: History shows search criteria (saved long-term)
   - Jobs show search results (saved short-term)

2. **Filter Search History**
   - Click inside **Search History filter box**
   - Type: `purchase`
   - Notice search list shortened to only searches containing "purchase"

3. **Reuse Previous Search**
   - For one of the filtered searches, click **Add to Search**
   - Notice search criteria appears in search bar
   - Note time range still shows default setting
   - Change time range as needed
   - Optionally modify search criteria
   - Execute the search

### Validation:
- [ ] Successfully accessed Search History
- [ ] Filtered history by "purchase" keyword
- [ ] Added previous search to current search bar
- [ ] Modified time range and executed search

---

## Task 4: Manage Search Jobs and Identify Errors

### Steps:

1. **Access Jobs Page**
   - In Splunk bar (black bar at top), click **Activity > Jobs**
   - Review search strings for any keystroke mistakes
   - Look for system searches like "| metadata ..." or "| history ..."

2. **Analyze Job Information**
   - Review columns: Owner, Events, Expires, Status, Actions
   - Identify any running jobs that could be finalized
   - Note any failed or error status jobs

3. **Clean Up Jobs (Optional)**
   - For any unnecessary running jobs, click stop button under Actions
   - This sets job status to "Finalized" and saves system resources

### Validation:
- [ ] Successfully accessed Jobs page
- [ ] Reviewed search strings for errors
- [ ] Identified job status and information
- [ ] Optionally cleaned up unnecessary jobs

---

## Progress Tracking Checklist

### Field Analysis Skills
- [ ] Identified interesting fields in search results
- [ ] Used Fields sidebar to explore field values
- [ ] Selected and deselected fields for display
- [ ] Analyzed field distributions and patterns

### Search Refinement
- [ ] Filtered searches using field values
- [ ] Used comparison operators (!=, =)
- [ ] Modified searches based on field analysis
- [ ] Interpreted error vs. success status codes

### Search Management
- [ ] Accessed and filtered Search History
- [ ] Reused previous search criteria
- [ ] Managed search jobs effectively
- [ ] Identified and cleaned up system searches

### Data Analysis
- [ ] Analyzed purchase transaction success rates
- [ ] Identified server errors affecting sales
- [ ] Quantified impact of downtime on transactions
- [ ] Provided actionable insights for business stakeholders

## Key Concepts Summary

### Field Types in Splunk
- **Interesting Fields**: Automatically identified fields with valuable data
- **Selected Fields**: Fields chosen for prominent display in results
- **Default Fields**: Always present (host, source, sourcetype, _time)

### Field-Based Filtering
- **Equality**: `field=value` (exact match)
- **Inequality**: `field!=value` (exclude specific values)
- **Interactive Selection**: Click field values to add to search
- **Multiple Values**: Combine with Boolean operators

### Search History vs. Jobs
- **Search History**: Long-term storage of search criteria
- **Jobs**: Short-term storage of search results and metadata
- **Filtering**: Both support filtering by keywords and time
- **Reuse**: History for criteria, Jobs for complete results

### HTTP Status Codes
- **200**: Success - transaction completed
- **4xx**: Client errors (400, 404, etc.)
- **5xx**: Server errors (500, 503, etc.)
- **Business Impact**: Status codes > 200 indicate lost sales

## Real-World Applications

### E-commerce Analysis
- Monitor purchase success rates
- Identify products with high error rates
- Track customer experience issues
- Measure downtime impact on revenue

### Performance Monitoring
- Analyze server response patterns
- Identify peak error periods
- Monitor application health
- Track user behavior trends

### Troubleshooting Workflows
- Use fields to narrow problem scope
- Filter by error types and codes
- Correlate issues across time periods
- Build targeted investigations

## Troubleshooting

### Common Issues

**Fields not appearing in sidebar:**
- Verify search contains relevant data
- Check if search is in Smart Mode
- Ensure field extraction is working properly
- Try refreshing the search

**Selected fields not displaying:**
- Confirm field was properly selected
- Check if field has values in current results
- Verify field selection wasn't accidentally removed
- Re-select field if necessary

**Search History empty or incomplete:**
- Verify you're logged in to correct account
- Check time range filter in history
- Clear any content filters
- History may be limited by retention settings

**Job management issues:**
- Check user permissions for job management
- Verify jobs aren't system-protected
- Some jobs may auto-expire
- Contact admin if persistent issues

### Windows/Mac Compatibility Notes

**Windows Users:**
- Use Ctrl+F to search within pages
- Browser zoom: Ctrl + (+/-) for better field visibility
- Right-click context menus work in field windows
- PowerShell available for any command line needs

**Mac Users:**
- Use Cmd+F to search within pages  
- Browser zoom: Cmd + (+/-) for better field visibility
- Right-click/Control-click for context menus
- Terminal available for command line operations

**Both Platforms:**
- Ensure JavaScript enabled for interactive fields
- Clear browser cache if field interactions fail
- Check popup blockers don't interfere with field windows
- Use modern browsers (Chrome, Firefox, Safari, Edge)

## Cleanup Instructions

1. **Clear Active Searches**
   - Return to Search interface
   - Clear search bar contents
   - Reset time range to default (Last 24 hours)

2. **Deselect All Fields**
   - Remove any fields from Selected Fields list
   - This improves performance for future searches
   - Return Fields sidebar to default state

3. **Optional: Clean Search History**
   - Remove test searches from history if desired
   - Keep useful searches for future reference
   - Consider saving important searches as reports

4. **Close Unnecessary Tabs**
   - Close extra Splunk browser tabs
   - Keep main Search & Reporting tab if continuing
   - Free up browser memory for better performance

## Validation Steps

After completing this lab, demonstrate your skills by:

1. **Independent Field Analysis**
   - Create a search and identify 3 interesting fields
   - Select 2 fields for display and explain their business value
   - Use field filtering to narrow results by 50%

2. **Error Analysis**
   - Find a search with both success and error results
   - Calculate error percentage: (errors / total) × 100
   - Explain business impact of identified errors

3. **Search Management**
   - Show 3 different ways to reuse previous searches
   - Demonstrate job cleanup process
   - Explain difference between History and Jobs

## Extension Activities

### Advanced Field Operations
- Explore field extraction for custom fields
- Use field aliases and calculated fields
- Create field-based data models
- Build field-centric dashboards

### Business Intelligence Applications
- Calculate conversion rates by product
- Analyze customer behavior patterns
- Monitor service level agreements
- Create executive summary reports

### Performance Optimization
- Optimize searches using field-based filtering
- Use field summary for data quality checks
- Implement field-based alerting
- Design efficient field extraction rules

## Next Steps

This lab covered field-based search techniques. The next lab will focus on:
- Advanced search commands and transformations
- Statistical analysis and aggregations
- Time-based analysis and trending
- Creating visualizations and reports

## Additional Resources

- Splunk Fields Reference Guide
- HTTP Status Code Reference
- Search Performance Best Practices  
- Field Extraction Documentation
- E-commerce Analytics Use Cases