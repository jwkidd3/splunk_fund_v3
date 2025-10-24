# Lab 9: Creating Alerts in Splunk

⚠️ **WARNING**: This lab requires a Splunk Enterprise trial or paid license. It will not work with the free license version.

## Lab Overview

In this lab, you will learn to create intelligent alerts in Splunk that monitor your data in real-time and notify you when specific conditions occur. You'll build security alerts for failed login attempts, configure alert conditions and actions, and test the alerting system to ensure proper functionality.

## Learning Objectives

By the end of this lab, you will be able to:

- Create real-time alerts based on search criteria
- Configure alert triggers and conditions
- Set up alert throttling to prevent alert storms
- Use the _audit index to monitor Splunk internal events
- Configure alert actions and severity levels
- Test alerts by triggering conditions
- View and manage triggered alerts
- Understand alert types (real-time vs scheduled)

## Prerequisites

- Completed Labs 1-8
- Splunk Enterprise trial or paid license (NOT free license)
- Admin access to Splunk instance
- Understanding of Splunk search commands
- Familiarity with authentication concepts

## Lab Environment Setup

### Step 1: Verify License Type

Check your license type:
1. Navigate to **Settings** → **Licensing**
2. Ensure you have an **Enterprise** or **Trial** license
3. If you see **Free**, this lab cannot be completed

### Step 2: Verify Admin Access

Ensure you have administrative privileges:
1. Check that you can access **Settings** menu
2. Verify you can see the **_audit** index
3. Confirm you can create alerts

### Step 3: Enable Audit Logging

Ensure audit logging is enabled:
1. Navigate to **Settings** → **Server Settings** → **General Settings**
2. Verify **Enable Splunk Web SSL** is configured
3. Restart Splunk if needed

## Key Concepts

### What are Alerts?

**Alerts** are automated notifications triggered when specific conditions are met:
- Monitor data in real-time or on schedule
- Send notifications via email, webhook, or custom scripts
- Take automated actions like running scripts
- Integrate with incident management systems

### Alert Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Real-time** | Continuous monitoring | Security incidents, system failures |
| **Scheduled** | Run at specific intervals | Daily reports, batch processing |

### Alert Conditions

| Condition | Description | Example |
|-----------|-------------|---------|
| **Number of Results** | Count of matching events | Alert if > 5 failed logins |
| **Custom** | Complex logic with eval | Alert if error rate > 10% |
| **Rolling Window** | Time-based aggregation | Alert if 10 errors in 5 minutes |

### The _audit Index

Splunk's **_audit** index contains:
- User login/logout events
- Search activity
- Configuration changes
- System events

---

## Exercise 1: Security Alert for Failed Logins

**Scenario**: Monitor failed login attempts on the Splunk search head. Alert when there's more than one failed admin login within one minute.

### Task 1.1: Understand Audit Data

Search for recent login events:

```spl
index=_audit action="login attempt" 
| head 10 
| table _time, user, action, info, src_ip
```

**Expected Fields**:
- **action**: Type of activity (login attempt, logout, etc.)
- **info**: Result (failed, succeeded)
- **user**: Username attempting login
- **src_ip**: Source IP address

### Task 1.2: Create Failed Login Search

Search for failed admin login attempts:

```spl
index=_audit action="login attempt" info=failed user=admin
```

**Time Range**: Set to **Last 15 minutes**

**Expected Results**: Events showing failed login attempts for admin user

### Task 1.3: Generate Test Data

To test the alert, we need to generate failed login attempts:

1. **Log out** of Splunk using **username** → **Logout**
2. Try to log in with:
   - **Username**: admin
   - **Password**: WrongPassword
3. Repeat this process 2-3 times to generate test data
4. Finally, log in with correct credentials

**✓ Checkpoint**: Failed login events appear in the _audit index

---

## Exercise 2: Create Real-Time Alert

### Task 2.1: Save Search as Alert

Using your failed login search:

```spl
index=_audit action="login attempt" info=failed user=admin
```

1. Click **Save As** → **Alert**
2. Configure basic settings:
   - **Title**: `Splunk Web Login Attempts`
   - **Description**: `Monitor failed admin login attempts`
   - **Permissions**: `Shared in App`

### Task 2.2: Configure Alert Type

Set alert type and timing:
- **Alert type**: Real-time
- **Time Range**: Last 15 minutes (for testing)

### Task 2.3: Configure Trigger Conditions

Set when the alert should fire:
- **Trigger alert when**: Number of Results
- **is greater than**: 0
- **in**: 1 minute

This means the alert triggers immediately when any failed admin login occurs.

### Task 2.4: Configure Alert Behavior

Set how the alert should behave:
- **Trigger**: For each result
- **Throttle**: ✓ Enable throttling
- **Suppress results containing field value**: host
- **Suppress triggering for**: 60 seconds

**Why Throttling?** Prevents alert storms by suppressing duplicate alerts for 60 seconds.

### Task 2.5: Configure Alert Actions

Add actions when alert triggers:

1. Click **Add Actions**
2. Select **Add to Triggered Alerts**
3. Configure:
   - **Severity**: High
   - **Add to**: Triggered Alerts (enabled by default)

### Task 2.6: Save Alert

1. Click **Save**
2. Click **View Alert** to see the alert configuration

**✓ Checkpoint**: Alert created and ready for testing

---

## Exercise 3: Test and Validate Alert

### Task 3.1: Trigger Alert Conditions

Generate events that should trigger the alert:

1. **Log out** of Splunk
2. Attempt to log in with wrong password **3 times**:
   - Username: admin
   - Password: WrongPassword
3. Log in with correct credentials

### Task 3.2: View Triggered Alerts

Check if alerts were triggered:

1. From the Splunk bar, click **Activity** → **Triggered Alerts**
2. Ensure **Search & Reporting** is selected for App
3. Look for "Splunk Web Login Attempts" alerts

**Expected Results**: One or more triggered alerts with High severity

### Task 3.3: Examine Alert Details

Click **View results** on a triggered alert to see:
- Events that caused the alert
- Timestamp when alert fired
- Search results that matched conditions

**✓ Checkpoint**: Alert successfully triggered and visible in Activity menu

---

## Exercise 4: Advanced Alert Configuration

### Task 4.1: Create Scheduled Alert

Create a summary alert that runs every 5 minutes:

```spl
index=_audit action="login attempt" info=failed 
| stats count by user, src_ip 
| where count > 2
```

Configure as:
- **Alert type**: Scheduled
- **Schedule**: Every 5 minutes
- **Trigger condition**: Number of Results > 0

### Task 4.2: Email Alert Action

Add email notification:
1. Edit your original alert
2. Add Actions → **Send email**
3. Configure:
   - **To**: your-email@domain.com
   - **Subject**: Failed Login Alert - $name$
   - **Message**: Include search results

### Task 4.3: Webhook Alert Action

For integration with external systems:
1. Add Actions → **Webhook**
2. Configure:
   - **URL**: http://your-webhook-url.com/alert
   - **HTTP Method**: POST
   - **Format**: JSON

---

## Challenge Exercises

### Challenge 1: Multi-Condition Alert

Create an alert for suspicious user activity:

```spl
index=_audit 
| bucket _time span=5m 
| stats dc(user) as unique_users, count by _time 
| where unique_users > 10 OR count > 100
```

Alert when:
- More than 10 different users active in 5 minutes, OR
- More than 100 total activities in 5 minutes

### Challenge 2: Correlation Alert

Monitor for brute force attacks:

```spl
index=_audit action="login attempt" info=failed 
| bucket _time span=1m 
| stats count by _time, src_ip 
| where count >= 5
```

Alert for 5+ failed logins from same IP within 1 minute.

### Challenge 3: Application Security Alert

Using your web application data:

```spl
index=main sourcetype=access_combined_wcookie status>=400 
| bucket _time span=5m 
| stats count by _time, clientip, status 
| where count > 10
```

Alert for high error rates from specific IPs.

---

## Alert Management

### Alert States

| State | Description | Action |
|-------|-------------|--------|
| **Enabled** | Alert is active and monitoring | Normal operation |
| **Disabled** | Alert exists but not running | Edit to re-enable |
| **Skipped** | Missed scheduled run | Check system resources |

### Alert History

View alert history:
1. Navigate to **Settings** → **Searches, reports, and alerts**
2. Find your alert and click **Edit**
3. Click **View triggered alert history**

### Alert Performance

Monitor alert performance:
- **Search execution time**: Should complete quickly
- **Alert frequency**: Avoid too frequent alerts
- **Resource usage**: Monitor system impact

---

## Best Practices

### Alert Design Principles

1. **Specific Conditions**: Make alerts actionable, not noisy
2. **Appropriate Timing**: Balance between quick detection and false positives
3. **Clear Documentation**: Include context in alert descriptions
4. **Test Thoroughly**: Validate alerts work before deploying

### Alert Naming Conventions

Use descriptive, consistent names:
- Environment: `PROD_Failed_Login_Alert`
- Severity: `CRITICAL_Database_Down`
- Category: `SECURITY_Suspicious_Activity`

### Throttling Strategy

| Alert Type | Throttling Period | Reason |
|------------|------------------|---------|
| Critical Security | 5-15 minutes | Immediate but not overwhelming |
| Performance Issues | 30-60 minutes | Avoid alert fatigue |
| Informational | 1-24 hours | Summary notifications |

### Alert Actions

| Action Type | Use Case | Configuration Tips |
|-------------|----------|-------------------|
| **Email** | Human notifications | Use clear subject lines |
| **Webhook** | System integration | Include context in payload |
| **Script** | Automated remediation | Test scripts thoroughly |
| **Triggered Alerts** | Splunk dashboard | Always include for tracking |

---

## Troubleshooting Guide

### Common Issues and Solutions

| Issue | Symptom | Solution |
|-------|---------|----------|
| Alert not triggering | No triggered alerts shown | Check search syntax and time range |
| Too many alerts | Alert storm/fatigue | Increase throttling period |
| Alert delays | Late notifications | Check system resources, simplify search |
| Missing audit data | Empty _audit index | Verify audit logging is enabled |
| Permission errors | Cannot create alerts | Check admin privileges |

### Debug Alert Searches

Test alert search manually:
```spl
| rest /services/saved/searches 
| search title="Splunk Web Login Attempts" 
| table title, search, cron_schedule, is_scheduled
```

Check alert status:
```spl
| rest /services/alerts/fired_alerts 
| table title, trigger_time, severity
```

### Performance Optimization

1. **Limit Time Range**: Use specific time windows
2. **Efficient Searches**: Avoid wildcards and regex when possible
3. **Index Selection**: Target specific indexes
4. **Field Optimization**: Extract only needed fields

---

## Cleanup

### Remove Test Alerts

After completing the lab:

1. **Delete Alerts**:
   - Navigate to Settings → Searches, reports, and alerts
   - Find "Splunk Web Login Attempts"
   - Click Delete

2. **Clear Triggered Alerts**:
   - Go to Activity → Triggered Alerts
   - Clear old test alerts

---

## Key Takeaways

✅ **You've learned to:**
- Create real-time alerts for security monitoring
- Configure alert triggers and conditions
- Implement throttling to prevent alert storms
- Use the _audit index for system monitoring
- Test alerts by generating trigger conditions
- Manage triggered alerts through the Activity menu
- Understand different alert types and their use cases

## Next Steps

- Explore advanced alert actions (scripts, webhooks)
- Learn about alert clustering and correlation
- Study integration with SOAR platforms
- Practice with custom alert conditions using eval

---

## Quick Reference

### Essential Alert SPL

```spl
# Basic failed login monitoring
index=_audit action="login attempt" info=failed user=admin

# Brute force detection
index=_audit action="login attempt" info=failed 
| bucket _time span=1m 
| stats count by _time, user, src_ip 
| where count >= 5

# System error monitoring
index=_internal log_level=ERROR 
| stats count by component 
| where count > 10
```

### Alert Configuration Template

```
Title: [SEVERITY]_[CATEGORY]_[DESCRIPTION]
Description: Clear explanation of what triggers alert
Search: Specific, efficient SPL query
Time Range: Appropriate for detection speed
Trigger: Based on business requirements
Throttling: Prevent alert fatigue
Actions: Appropriate notification methods
```

### REST API Commands

```spl
# List all alerts
| rest /services/saved/searches 
| search is_scheduled=1 
| table title, search, cron_schedule

# View triggered alerts
| rest /services/alerts/fired_alerts 
| table title, trigger_time, severity, sid

# Check alert status
| rest /services/saved/searches/[alert_name] 
| table title, disabled, next_scheduled_time
```

---

## Answer Key

<details>
<summary>Click to reveal answers</summary>

### Exercise 1
- Search: `index=_audit action="login attempt" info=failed user=admin`
- Expected events: Failed login attempts for admin user

### Exercise 2
- Alert name: Splunk Web Login Attempts
- Alert type: Real-time
- Trigger condition: Number of Results > 0
- Throttling: 60 seconds on host field

### Exercise 3
- Trigger method: 3 failed logins with wrong password
- Result: Alerts appear in Activity → Triggered Alerts
- Severity: High

### Key Fields in _audit
- action: login attempt, logout, search, etc.
- info: failed, succeeded
- user: Username
- src_ip: Source IP address

</details>