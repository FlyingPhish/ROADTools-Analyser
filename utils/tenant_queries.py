# utils/tenant_queries.py

TENANT_QUERIES = {
    "AuthorizationPolicyQuery": """
    SELECT 
        id,
        allowInvitesFrom,
        allowedToSignUpEmailBasedSubscriptions,
        allowedToUseSSPR,
        allowEmailVerifiedUsersToJoinOrganization,
        blockMsolPowerShell,
        defaultUserRolePermissions,
        displayName,
        description,
        enabledPreviewFeatures
    FROM AuthorizationPolicys;
    """,

    "TenantDetailsQuery": """
    SELECT 
        objectId as Tenant_ID,
        dirSyncEnabled,
        selfServePasswordResetPolicy,
        companyLastDirSyncTime,
        companyTags,
        createdDateTime,
        displayName,
        city,
        street,
        state,
        postalCode,
        country,
        countryLetterCode,
        assignedPlans,
        authorizedServiceInstance
    FROM TenantDetails;
    """,

    "DirectorySettingsQuery": """
    SELECT 
        displayName,
        [values]
    FROM DirectorySettings;
    """
}