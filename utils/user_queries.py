USER_QUERIES = {
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

    "GroupedByPassAge": """
        SELECT 
            CAST((julianday(date('now')) - julianday(date(lastPasswordChangeDateTime))) / 365 AS INTEGER) AS 'YearsSincePasswordChange',
            COUNT(*) AS 'NumberOfUsers'
        FROM Users
        WHERE accountEnabled = '1'
        GROUP BY YearsSincePasswordChange
        ORDER BY YearsSincePasswordChange DESC;
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