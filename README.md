# ROADTools SQLITE Analyser
A Python script that analyzes Azure AD user and tenant data from a ROADtools database. It takes two user arguments: `-db` (file path of ROADtools db) and `-o` (file path and name for outputted spreadsheet). The script runs a set of predefined queries to extract and analyze various aspects of Azure AD configuration and user data.

## Features

### User Data Analysis
- Identifies accounts with passwords older than 90 days
- Lists accounts with 'Disable Password Expiry' policy
- Shows accounts and guests with unchanged passwords (from creation)
- Identifies on-premises synced guest accounts
- Provides overall statistics including numbers and percentages for the above points
- Generates a table of password ages (in years) and the number of accounts per age

### Tenant Data Analysis
- Extracts and formats Authorization Policy details
- Retrieves comprehensive Tenant Details
- Pulls Directory Settings information

### Output
- Generates an XLSX spreadsheet with named tabs for each query result
- Formats JSON data for improved readability in Excel
- Ensures all query results are included, even if empty (headers are preserved)
- Auto-adjusts column widths for better visibility
- Applies text wrapping and vertical alignment for JSON columns

### Console Output
Displays a summary of key statistics after analysis completion

```text
{Banner Goes Here}
By @FlyingPhishy

Excel file saved: Your_Output_Name.xlsx

General Statistics:
* Total Users: 500
* Total Member Users: 346
* Total Active Users: 335
* Total Guests: 114
* Total Active Guest Users: 114
* Total Users w/ Disable Password Expiry: 100

Password statistics for active users:
* 100% of users have the password policy 'Disable Password Expiration' attached.
* 100% of member users have passwords over 90 days old.
* 100% of guest users have passwords over 90 days old.
* 50.5% of members have not changed their password since creation.
* 100% of guest users have not changed their password since creation.
```

### Users By Password Years (SQL View)
<p align="center">
  <img src="https://github.com/FlyingPhish/ROADTools-Analyser/assets/46652779/8c0e2af8-d252-463a-a97d-603f02fc6fbf" alt="Number of users grouped by password age in years">
</p>

### Toal User Stats (SQL View)
<p align="center">
  <img src="https://github.com/FlyingPhish/ROADTools-Analyser/assets/46652779/ad6a26bd-8a4b-4db8-b803-fe0a99d9088c" alt="total user stats">
</p>

## Usage
```
python3 ROAD-Analysis.py -db "filepath/to/db" -o "filepath/for/output/spreadsheet.xlsx"
```

## Requirements

Ensure you have the required packages installed:

```
python3 -m venv .venv 
source .venv/bin/activate
pip install -r requirements.txt
```

## Applications
This tool can be used for:
- Microsoft Cloud, Azure AD, Intune MDM Security Reviews
- Compliance Audits

PS - I use it on all my cloud-based engagements

## To-Do
- Outdated and unsupported devices (port from my Intune-OS-Build-Checker Script)
- Privileged Users
- Group-based windows of opportunities
- Service Principles