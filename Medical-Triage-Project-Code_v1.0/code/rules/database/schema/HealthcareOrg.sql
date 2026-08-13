CREATE TABLE dbo.HealthcareOrg
(
    OrganizationId INT IDENTITY(1,1) NOT NULL,
    Name NVARCHAR(200) NOT NULL,
    Type VARCHAR(50) NOT NULL,
    LicenseNumber NVARCHAR(100) NOT NULL,
    Address NVARCHAR(500) NULL,

    CONSTRAINT PK_HealthcareOrg
        PRIMARY KEY (OrganizationId),

    CONSTRAINT UQ_HealthcareOrg_LicenseNumber
        UNIQUE (LicenseNumber)
);