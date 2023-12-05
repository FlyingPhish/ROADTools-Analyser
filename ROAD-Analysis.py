import os
import sqlite3
import pandas as pd
import argparse

def print_banner():
    ascii_art = """
██▀███  ▒█████  ▄▄▄     ▓█████▄▄▄▄█████▓▒█████  ▒█████  ██▓     ██████     ▄▄▄      ███▄    █ ▄▄▄      ██▓  ▓██   ██▓ ██████ ██▓ ██████ 
▓██ ▒ ██▒██▒  ██▒████▄   ▒██▀ ██▓  ██▒ ▓▒██▒  ██▒██▒  ██▓██▒   ▒██    ▒    ▒████▄    ██ ▀█   █▒████▄   ▓██▒   ▒██  ██▒██    ▒▓██▒██    ▒ 
▓██ ░▄█ ▒██░  ██▒██  ▀█▄ ░██   █▒ ▓██░ ▒▒██░  ██▒██░  ██▒██░   ░ ▓██▄      ▒██  ▀█▄ ▓██  ▀█ ██▒██  ▀█▄ ▒██░    ▒██ ██░ ▓██▄  ▒██░ ▓██▄   
▒██▀▀█▄ ▒██   ██░██▄▄▄▄██░▓█▄   ░ ▓██▓ ░▒██   ██▒██   ██▒██░     ▒   ██▒   ░██▄▄▄▄██▓██▒  ▐▌██░██▄▄▄▄██▒██░    ░ ▐██▓░ ▒   ██░██░ ▒   ██▒
░██▓ ▒██░ ████▓▒░▓█   ▓██░▒████▓  ▒██▒ ░░ ████▓▒░ ████▓▒░██████▒██████▒▒    ▓█   ▓██▒██░   ▓██░▓█   ▓██░██████▒░ ██▒▓▒██████▒░██▒██████▒▒
░ ▒▓ ░▒▓░ ▒░▒░▒░ ▒▒   ▓▒█░▒▒▓  ▒  ▒ ░░  ░ ▒░▒░▒░░ ▒░▒░▒░░ ▒░▓  ▒ ▒▓▒ ▒ ░    ▒▒   ▓▒█░ ▒░   ▒ ▒ ▒▒   ▓▒█░ ▒░▓  ░ ██▒▒▒▒ ▒▓▒ ▒ ░▓ ▒ ▒▓▒ ▒ ░
░▒ ░ ▒░ ░ ▒ ▒░  ▒   ▒▒ ░░ ▒  ▒    ░     ░ ▒ ▒░  ░ ▒ ▒░░ ░ ▒  ░ ░▒  ░ ░     ▒   ▒▒ ░ ░░   ░ ▒░ ▒   ▒▒ ░ ░ ▒  ▓██ ░▒░░ ░▒  ░ ░▒ ░ ░▒  ░ ░
░░   ░░ ░ ░ ▒   ░   ▒   ░ ░  ░  ░     ░ ░ ░ ▒ ░ ░ ░ ▒   ░ ░  ░  ░  ░       ░   ▒     ░   ░ ░  ░   ▒    ░ ░  ▒ ▒ ░░ ░  ░  ░  ▒ ░  ░  ░  
░        ░ ░       ░  ░  ░               ░ ░     ░ ░     ░  ░     ░           ░  ░        ░      ░  ░   ░  ░ ░          ░  ░       ░  
By @FlyingPhishy
"""

    print(ascii_art)

def connect_to_db(db_file):
    try:
        return sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def run_query(conn, query):
    try:
        return pd.read_sql_query(query, conn)
    except sqlite3.Error as e:
        print(f"Error running query: {e}")
        return pd.DataFrame()

def save_to_excel(dataframes, file_name):
    with pd.ExcelWriter(file_name) as writer:
        for sheet_name, df in dataframes.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SQLite queries and export results to Excel.")
    parser.add_argument("-db", "--database", required=True, help="Path to the SQLite database file.")
    parser.add_argument("-o", "--output", required=True, help="Path and name of the output Excel file.")
    args = parser.parse_args()

    print_banner()

    if not os.path.exists(args.database):
        print(f"The specified database file does not exist: {args.db_file}")
        exit()

    database_file = args.database
    output_file = args.output

    queries = {
        "GroupedByPassAge": """
            SELECT 
                CAST((julianday(date('now')) - julianday(date(lastPasswordChangeDateTime))) / 365 AS INTEGER) AS 'YearsSincePasswordChange',
                COUNT(*) AS 'NumberOfUsers'
            FROM Users
            WHERE accountEnabled = '1'
            GROUP BY YearsSincePasswordChange
            ORDER BY YearsSincePasswordChange DESC;
        """,

        "OverallStats": """
            SELECT 
                (SELECT COUNT(*) FROM Users) AS 'Total Users',
                (SELECT COUNT(*) FROM Users WHERE userType = 'Member') AS 'Total Member Users',
                (SELECT COUNT(*) FROM Users WHERE userType = 'Guest') AS 'Total Guest Users',
                (SELECT COUNT(*) FROM Users WHERE accountEnabled = '1' AND userType = "Member") AS 'Total Active Users',
                (SELECT COUNT(*) FROM Users WHERE userType = 'Guest') AS 'Total Guests',
                (SELECT COUNT(*) FROM Users WHERE accountEnabled = '1' AND userType = 'Guest') AS 'Total Active Guests',
                (SELECT COUNT(*) FROM Users WHERE accountEnabled = '1' AND userType = 'Member' AND julianday(date('now')) - julianday(date(lastPasswordChangeDateTime)) > 90) AS 'Member Users Password > 90 Days',
                (SELECT COUNT(*) FROM Users WHERE accountEnabled = '1' AND userType = 'Guest' AND julianday(date('now')) - julianday(date(lastPasswordChangeDateTime)) > 90) AS 'Guest Users Password > 90 Days',
                (SELECT COUNT(*) FROM Users WHERE accountEnabled = '1' AND userType = 'Member' AND date(createdDateTime) = date(lastPasswordChangeDateTime)) AS 'Unchanged Member Passwords From Creation',
                (SELECT COUNT(*) FROM Users WHERE accountEnabled = '1' AND userType = 'Guest' AND date(createdDateTime) = date(lastPasswordChangeDateTime)) AS 'Unchanged Guest Passwords From Creation',
                (SELECT COUNT(*) FROM Users WHERE accountEnabled = '1' AND passwordPolicies = 'DisablePasswordExpiration') AS 'Users w/ Disable Password Expiry',
                -- Stats
                100.0 * (SELECT COUNT(*) FROM Users WHERE accountEnabled = '1' AND passwordPolicies = 'DisablePasswordExpiration') / (SELECT COUNT(*) FROM Users WHERE accountEnabled = '1') AS 'Percentage Users w/ Disable Password Expiry',
                100.0 * (SELECT COUNT(*) FROM Users WHERE accountEnabled = '1' AND userType = 'Member' AND julianday(date('now')) - julianday(date(lastPasswordChangeDateTime)) > 90) / (SELECT COUNT(*) FROM Users WHERE accountEnabled = '1' AND userType = 'Member') AS 'Percentage of Members Password > 90 Days',
                100.0 * (SELECT COUNT(*) FROM Users WHERE accountEnabled = '1' AND userType = 'Guest' AND julianday(date('now')) - julianday(date(lastPasswordChangeDateTime)) > 90) / (SELECT COUNT(*) FROM Users WHERE accountEnabled = '1' AND userType = 'Guest') AS 'Percentage of Guests Password > 90 Days',
                100.0 * (SELECT COUNT(*) FROM Users WHERE accountEnabled = '1' AND userType = 'Member' AND date(createdDateTime) = date(lastPasswordChangeDateTime)) / (SELECT COUNT(*) FROM Users WHERE accountEnabled = '1' AND userType = 'Member') AS 'Percentage of Members w/ Unchanged Passwords From Creation',
                100.0 * (SELECT COUNT(*) FROM Users WHERE accountEnabled = '1' AND userType = 'Guest' AND date(createdDateTime) = date(lastPasswordChangeDateTime)) / (SELECT COUNT(*) FROM Users WHERE accountEnabled = '1' AND userType = 'Guest') AS 'Percentage of Guests w/ Unchanged Passwords From Creation'
                ;
        """,

        "OnPremGuests": """
            SELECT 
                userPrincipalName as UPN, 
                displayName as Name, 
                userType as UserType, 
                dirSyncEnabled as SyncronisedToOnprem, 
                strftime('%d/%m/%Y', lastDirSyncTime) as LastDirSync, 
                strftime('%d/%m/%Y', lastPasswordChangeDateTime) as LastPassChange, 
                strftime('%d/%m/%Y', onPremisesPasswordChangeTimestamp) as LastOnPremPassChange
            FROM Users
            WHERE userType = 'Guest' AND dirSyncEnabled = '1';
        """,

        "UnchangedPassGuests": """
            SELECT 
                userPrincipalName as UPN, 
                displayName as Name, 
                userType as UserType, 
                strftime('%d/%m/%Y', createdDateTime) as CreatedDate, 
                strftime('%d/%m/%Y', lastPasswordChangeDateTime) as LastPassChange,
                CASE
                        WHEN (julianday(date('now')) - julianday(date(createdDateTime))) < 30 THEN
                            ROUND(julianday(date('now')) - julianday(date(createdDateTime))) || ' day(s)'
                        WHEN (julianday(date('now')) - julianday(date(createdDateTime))) < 365 THEN
                            ROUND((julianday(date('now')) - julianday(date(createdDateTime)))/30) || ' month(s)'
                        ELSE
                            ROUND((julianday(date('now')) - julianday(date(createdDateTime)))/365) || ' year(s)'
                END AS accountAge,
                ROUND(julianday(date('now')) - julianday(date(createdDateTime))) AS accountAgeInDays
            FROM Users
            WHERE userType = 'Guest' AND date(createdDateTime) = date(lastPasswordChangeDateTime) AND accountEnabled = '1'
            ORDER BY accountAgeInDays DESC;
        """,

        "UnchangedPassUsers": """
            SELECT 
                userPrincipalName as UPN, 
                displayName as Name, 
                userType as UserType, 
                strftime('%d/%m/%Y', createdDateTime) as CreatedDate, 
                strftime('%d/%m/%Y', lastPasswordChangeDateTime) as LastPassChange,
                strftime('%d/%m/%Y', onPremisesPasswordChangeTimestamp) as LastOnPremPassChange, 
                CASE
                        WHEN (julianday(date('now')) - julianday(date(createdDateTime))) < 30 THEN
                            ROUND(julianday(date('now')) - julianday(date(createdDateTime))) || ' day(s)'
                        WHEN (julianday(date('now')) - julianday(date(createdDateTime))) < 365 THEN
                            ROUND((julianday(date('now')) - julianday(date(createdDateTime)))/30) || ' month(s)'
                        ELSE
                            ROUND((julianday(date('now')) - julianday(date(createdDateTime)))/365) || ' year(s)'
                END AS accountAge,
                ROUND(julianday(date('now')) - julianday(date(createdDateTime))) AS accountAgeInDays
            FROM Users
            WHERE date(createdDateTime) = date(lastPasswordChangeDateTime) AND accountEnabled = '1'
            ORDER BY accountAgeInDays DESC;
        """,

        "UsersWPasswordExpiration": """
            SELECT userPrincipalName as UPN, displayName as Name, userType as UserType, passwordPolicies, 
                (SELECT COUNT(*) FROM Users WHERE passwordPolicies = 'DisablePasswordExpiration') AS countUsersWithPolicy
            FROM Users
            WHERE passwordPolicies = 'DisablePasswordExpiration' AND accountEnabled = '1';
        """,

        "AllDetails": """
            SELECT 
                userPrincipalName as UPN, 
                displayName as Name, 
                userType as UserType,
                strftime('%d/%m/%Y', lastPasswordChangeDateTime) as LastPassChange,
                strftime('%d/%m/%Y', onPremisesPasswordChangeTimestamp) as LastOnPremPassChange, 
                CASE
                        WHEN (julianday(date('now')) - julianday(date(lastPasswordChangeDateTime))) < 30 THEN
                            CAST((julianday(date('now')) - julianday(date(lastPasswordChangeDateTime))) AS INTEGER) || ' day(s)'
                        WHEN (julianday(date('now')) - julianday(date(lastPasswordChangeDateTime))) < 365 THEN
                            CAST(((julianday(date('now')) - julianday(date(lastPasswordChangeDateTime)))/30) AS INTEGER) || ' month(s)'
                        ELSE
                            CAST(((julianday(date('now')) - julianday(date(lastPasswordChangeDateTime)))/365) AS INTEGER) || ' year(s)'
                END AS PasswordAge,
                CASE WHEN date(lastPasswordChangeDateTime) = date(createdDateTime) THEN 'True' ELSE 'False' END AS PasswordAgeEqualsCreationDate,
                CAST((julianday(date('now')) - julianday(date(lastPasswordChangeDateTime))) AS INTEGER) AS PasswordAgeInDays
            FROM Users
            WHERE julianday(date('now')) - julianday(date(lastPasswordChangeDateTime)) > 90 AND accountEnabled = '1'
            ORDER BY PasswordAgeInDays DESC;
        """
    }

    conn = connect_to_db(database_file)
    if conn:
        results = {name: run_query(conn, query) for name, query in queries.items()}
        save_to_excel(results, output_file)
        conn.close()