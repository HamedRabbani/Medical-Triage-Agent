CREATE TABLE dbo.UserAccount
(
    UserId INT IDENTITY(1,1) NOT NULL,
    Email NVARCHAR(254) NOT NULL,
    PasswordHash NVARCHAR(255) NOT NULL,
    Phone NVARCHAR(20) NULL,
    Status VARCHAR(20) NOT NULL
        CONSTRAINT DF_UserAccount_Status DEFAULT 'Active',
    CreatedAt DATETIME2(0) NOT NULL
        CONSTRAINT DF_UserAccount_CreatedAt DEFAULT SYSUTCDATETIME(),

    CONSTRAINT PK_UserAccount
        PRIMARY KEY (UserId),

    CONSTRAINT UQ_UserAccount_Email
        UNIQUE (Email),

    CONSTRAINT CK_UserAccount_Status
        CHECK (Status IN ('Active', 'Disabled', 'Locked'))
);
