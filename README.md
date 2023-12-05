# ROADTools SQLITE Analyser
A smol Python script that takes two user arguments -db (file path of ROADtools db) and -o (file path and name for outputted spreadsheet) that runs a set number of queries aimed at analysing Azure AD user password metadata to identify the following cases:

- Accounts w/ passwords > 90 days
- Accounts w/ Disable Password Expirary
- Accounts and guests w/ unchanged passwords (from creation)
- Onprem sync'd guest accounts
- Overall stats for previous bullet points (including numbers and percentages)
- Table of password ages (in years) and number of accounts per age.

Once completed, the script will output an XLSX spreadsheet with named tabs per query.

## Usage
python .\ROAD-Analysis.py -db "filepath\to\db" -o "filepath\for\outputed\spreadsheet.xlsx"

Can be used for security reviews or for target picking.