# Lab 2: Basic Searching with Splunk Search Language
*Day 1 - Lab 2 of 4*

## Learning Objectives
After completing this lab, you will be able to:
- Perform basic searches using Splunk Search Language
- Use Boolean operators (AND, OR) and wildcards in searches
- Navigate and analyze search results effectively
- Use the timeline to identify patterns and trends
- Refine searches using field values
- Save and share search results with proper permissions
- Manage search jobs and histories

## Prerequisites
- Splunk environment running and accessible
- Sample data loaded (completed Lab 1)
- Basic understanding of Splunk interface

## Lab Scenario
There is reason to believe there might be a security issue with your web server. Your manager has asked you to explore failed SSH login attempts and identify potential security threats.

## Data Sources
This lab uses the following data types:
- **Web Application** (sourcetype: `access_combined_wcookie`)
- **Database** (sourcetype: `db_audit`)
- **Web Server** (sourcetype: `linux_secure`)

---

## Task 1: Perform a Basic Search

### Steps:

1. **Navigate to Search Interface**
   - If in Home app, click **Search & Reporting** from the left sidebar
   - Alternatively, click **Search** from the top navigation bar

2. **Execute Your First Search**
   - In the search bar, type: `error OR fail*`
   - Set time range to **All time** using the time picker
   - Click the **Search** button

3. **Analyze Results**
   - Review search results and observe highlighted search terms
   - Use pagination to browse through results
   - Note the host, source, and sourcetype values at the bottom of each event
   - Observe events from both `web_application` and `web_server` hosts

### Validation:
- [ ] Search executed successfully
- [ ] Results show highlighted search terms
- [ ] Multiple hosts visible in results
- [ ] Can navigate through paginated results

---

## Task 2: Narrow Your Search Results

### Steps:

1. **Start New Search**
   - Click **Search** to start fresh
   - Enter search: `fail* AND password`
   - Set time range to **All time**
   - Execute search

2. **Add Port Filter**
   - Note port values in several events
   - At end of search string, add: `22`
   - Execute search
   - Observe that events with any occurrence of "22" are returned

3. **Refine with Exact Phrase**
   - Replace `22` with `"port 22"` (include quotes)
   - Execute search
   - Verify only events with exact phrase "port 22" appear
   - Page through results to see login failures

### Validation:
- [ ] Initial search returns password-related failures
- [ ] Adding "22" returns too many results
- [ ] Using "port 22" in quotes returns specific SSH login attempts
- [ ] Multiple login failures visible

---

## Task 3: Analyze Trends Using Timeline

### Steps:

1. **Examine Timeline**
   - Look for patterns and spikes in the timeline above results
   - Single-click on different columns to view events for specific time periods

2. **Identify Attack Patterns**
   - Look for spikes that might indicate coordinated attacks
   - Single-click another column and compare event patterns
   - Note any similarities in IP addresses or user accounts

3. **Time Range Drilling**
   - If you see a spike, double-click that column to zoom into that time range
   - Analyze the concentrated activity during that period

### Validation:
- [ ] Can interact with timeline columns
- [ ] Identified time periods with unusual activity
- [ ] Recognized potential attack patterns
- [ ] Successfully drilled down into specific time ranges

---

## Task 4: Refine Results Using Field Values

### Steps:

1. **Use Interactive Fields**
   - Click on a username in the search results
   - Select **Add to search** from the popup menu
   - Observe updated search string and results

2. **Analyze User-Specific Activity**
   - Review timeline for spikes in this user's failed attempts
   - If spike exists, double-click timeline column to zoom in

3. **Remove Field Filter**
   - Click the same username again
   - Select **Remove from search**
   - Verify search returns to broader results

### Validation:
- [ ] Successfully added user to search filter
- [ ] Search results narrowed to specific user
- [ ] Timeline shows user-specific activity patterns
- [ ] Successfully removed filter to return to broader results

---

## Task 5: Save and Share Search Results

### Steps:

1. **Access Job Settings**
   - From **Job** menu (below search bar), select **Edit Job Settings**

2. **Modify Permissions**
   - Change **Read Permissions** from Private to **Everyone**
   - This allows others to leverage your search work

3. **Extend Lifetime**
   - Change search lifetime from default (10 minutes) to **7 days**
   - Note options to copy link or bookmark search

4. **Save Changes**
   - Click **Save** to return to Search view

5. **Review Job History**
   - Navigate to **Activity > Jobs** (right side of Splunk bar)
   - Review Owner, Events, Expires, Status, and Actions columns
   - Click on your search criteria (in blue) to reopen saved search

### Validation:
- [ ] Successfully modified job permissions to Everyone
- [ ] Extended search lifetime to 7 days
- [ ] Can access job history
- [ ] Can reopen saved search from history
- [ ] Search reopens without re-executing

---

## Progress Tracking Checklist

### Basic Search Skills
- [ ] Executed searches with Boolean operators (AND, OR)
- [ ] Used wildcards (*) effectively
- [ ] Applied proper time range selection
- [ ] Navigated paginated results

### Search Refinement
- [ ] Filtered results using exact phrases with quotes
- [ ] Added and removed field-based filters
- [ ] Used interactive field selection menus

### Analysis Techniques
- [ ] Interpreted timeline patterns
- [ ] Identified potential security threats
- [ ] Correlated events across time periods
- [ ] Recognized attack patterns

### Search Management
- [ ] Modified job permissions and lifetime
- [ ] Accessed and managed job history
- [ ] Shared search results appropriately

## Key Concepts Summary

### Search Language Basics
- **Boolean Operators**: Use AND, OR for combining search terms
- **Wildcards**: Use * for pattern matching (fail* matches fail, failed, failure)
- **Exact Phrases**: Use quotes for exact string matching ("port 22")

### Timeline Analysis
- Timeline visualization helps identify patterns and anomalies
- Spikes in activity may indicate security incidents
- Time-based correlation reveals attack sequences

### Interactive Search
- Click field values to dynamically modify searches
- Add/remove filters without retyping search strings
- Interactive approach speeds up investigation workflows

### Search Job Management
- Control search permissions for collaboration
- Extend job lifetime for important searches
- Job history provides audit trail and reusability

## Troubleshooting

### Common Issues

**Search returns no results:**
- Verify time range covers data periods
- Check search syntax for typos
- Ensure data sources are available

**Too many results to analyze:**
- Add more specific filters
- Use exact phrases with quotes
- Narrow time range to focus investigation

**Timeline shows no activity:**
- Expand time range
- Verify search terms match data
- Check if events exist in selected timeframe

**Cannot save or share searches:**
- Verify user permissions
- Check system storage limits
- Confirm job settings access

### Windows/Mac Compatibility Notes

**Windows Users:**
- Use Command Prompt or PowerShell for any command line operations
- Browser compatibility: Chrome, Firefox, Edge supported
- File paths use backslashes (\) in Windows

**Mac Users:**
- Use Terminal for command line operations  
- Browser compatibility: Safari, Chrome, Firefox supported
- File paths use forward slashes (/) in macOS

**Both Platforms:**
- Ensure JavaScript is enabled in browser
- Clear browser cache if interface issues occur
- Check firewall settings allow Splunk web interface access

## Cleanup Instructions

1. **Optional: Clear Search History**
   - Navigate to Activity > Jobs
   - Delete unnecessary search jobs to free storage
   - Keep important searches with extended lifetimes

2. **Reset Time Range**
   - Set time picker back to default range (Last 24 hours)
   - This improves performance for future searches

3. **Close Browser Tabs**
   - Close extra Splunk tabs to free resources
   - Keep main Search & Reporting tab open if continuing

## Validation Steps

After completing this lab, verify your skills by:

1. **Independent Search**: Create a search for successful logins without guidance
2. **Pattern Recognition**: Identify at least one suspicious activity pattern
3. **Search Management**: Save one search with appropriate permissions
4. **Timeline Analysis**: Explain what timeline patterns might indicate security issues

## Next Steps

This lab covered fundamental searching techniques. In the next lab, you will learn about:
- Advanced search commands and functions
- Statistical analysis and reporting
- Data visualization and dashboards
- Automated alerting and monitoring

## Additional Resources

- Splunk Search Language Reference
- Best Practices for Search Performance
- Security Use Cases and Examples
- Advanced Timeline Analysis Techniques