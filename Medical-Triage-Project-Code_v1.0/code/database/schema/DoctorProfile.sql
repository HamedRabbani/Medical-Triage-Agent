CREATE TABLE dbo.DoctorProfile
(
    DoctorId INT IDENTITY(1,1) NOT NULL,
    UserId INT NOT NULL,
    OrganizationId INT NOT NULL,
    LicenseNumber NVARCHAR(100) NOT NULL,
    Specialty NVARCHAR(100) NOT NULL,

    CONSTRAINT PK_DoctorProfile
        PRIMARY KEY (DoctorId),

    CONSTRAINT FK_DoctorProfile_UserAccount
        FOREIGN KEY (UserId)
        REFERENCES dbo.UserAccount(UserId),

    CONSTRAINT FK_DoctorProfile_HealthcareOrg
        FOREIGN KEY (OrganizationId)
        REFERENCES dbo.HealthcareOrg(OrganizationId),

    CONSTRAINT UQ_DoctorProfile_UserId
        UNIQUE (UserId),

    CONSTRAINT UQ_DoctorProfile_LicenseNumber
        UNIQUE (LicenseNumber)
);