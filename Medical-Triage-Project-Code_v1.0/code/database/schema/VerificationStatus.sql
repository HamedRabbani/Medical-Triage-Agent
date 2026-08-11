CREATE TABLE dbo.VerificationStatus
(
    StatusId INT IDENTITY(1,1) NOT NULL,
    StatusName NVARCHAR(50) NOT NULL,

    CONSTRAINT PK_VerificationStatus
        PRIMARY KEY (StatusId),

    CONSTRAINT UQ_VerificationStatus_StatusName
        UNIQUE (StatusName)
);