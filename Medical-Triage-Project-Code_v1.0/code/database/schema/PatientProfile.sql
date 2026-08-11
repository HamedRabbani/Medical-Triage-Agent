CREATE TABLE dbo.PatientProfile
(
    PatientId INT IDENTITY(1,1) NOT NULL,
    UserId INT NOT NULL,
    FirstName NVARCHAR(100) NOT NULL,
    LastName NVARCHAR(100) NOT NULL,
    DateOfBirth DATE NOT NULL,
    Gender VARCHAR(20) NOT NULL,
    NationalId NVARCHAR(20) NOT NULL,
    CreatedAt DATETIME2(0) NOT NULL
        CONSTRAINT DF_PatientProfile_CreatedAt
        DEFAULT SYSUTCDATETIME(),

    CONSTRAINT PK_PatientProfile
        PRIMARY KEY (PatientId),

    CONSTRAINT FK_PatientProfile_UserAccount
        FOREIGN KEY (UserId)
        REFERENCES dbo.UserAccount(UserId),

    CONSTRAINT UQ_PatientProfile_UserId
        UNIQUE (UserId),

    CONSTRAINT UQ_PatientProfile_NationalId
        UNIQUE (NationalId),

    CONSTRAINT CK_PatientProfile_Gender
        CHECK (Gender IN ('Male', 'Female', 'Other', 'Unknown'))
);