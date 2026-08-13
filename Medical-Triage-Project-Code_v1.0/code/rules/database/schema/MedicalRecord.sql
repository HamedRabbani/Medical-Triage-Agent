CREATE TABLE dbo.MedicalRecord
(
    RecordId BIGINT IDENTITY(1,1) NOT NULL,
    PatientId INT NOT NULL,
    CreatedByUserId INT NOT NULL,
    Condition NVARCHAR(200) NOT NULL,
    Description NVARCHAR(MAX) NULL,
    RecordType VARCHAR(50) NOT NULL,
    CreatedAt DATETIME2(0) NOT NULL
        CONSTRAINT DF_MedicalRecord_CreatedAt
        DEFAULT SYSUTCDATETIME(),
    VerificationStatusId INT NOT NULL,

    CONSTRAINT PK_MedicalRecord
        PRIMARY KEY (RecordId),

    CONSTRAINT FK_MedicalRecord_PatientProfile
        FOREIGN KEY (PatientId)
        REFERENCES dbo.PatientProfile(PatientId),

    CONSTRAINT FK_MedicalRecord_CreatedByUser
        FOREIGN KEY (CreatedByUserId)
        REFERENCES dbo.UserAccount(UserId),

    CONSTRAINT FK_MedicalRecord_VerificationStatus
        FOREIGN KEY (VerificationStatusId)
        REFERENCES dbo.VerificationStatus(StatusId)
);