CREATE TABLE dbo.AuditLog
(
    AuditId BIGINT IDENTITY(1,1) NOT NULL,
    UserId INT NULL,
    Action VARCHAR(50) NOT NULL,
    EntityName VARCHAR(100) NOT NULL,
    EntityId INT NULL,
    OldValue NVARCHAR(MAX) NULL,
    NewValue NVARCHAR(MAX) NULL,
    CreatedAt DATETIME2(0) NOT NULL
        CONSTRAINT DF_AuditLog_CreatedAt DEFAULT SYSUTCDATETIME(),

    CONSTRAINT PK_AuditLog
        PRIMARY KEY (AuditId),

    CONSTRAINT FK_AuditLog_UserAccount
        FOREIGN KEY (UserId)
        REFERENCES dbo.UserAccount(UserId)
);