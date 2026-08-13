CREATE TABLE dbo.TriageSession
(
    SessionId BIGINT IDENTITY(1,1) NOT NULL,
    PatientId INT NOT NULL,
    StartTime DATETIME2(0) NOT NULL
        CONSTRAINT DF_TriageSession_StartTime
        DEFAULT SYSUTCDATETIME(),
    EndTime DATETIME2(0) NULL,
    Status VARCHAR(20) NOT NULL
        CONSTRAINT DF_TriageSession_Status
        DEFAULT 'Active',

    CONSTRAINT PK_TriageSession
        PRIMARY KEY (SessionId),

    CONSTRAINT FK_TriageSession_PatientProfile
        FOREIGN KEY (PatientId)
        REFERENCES dbo.PatientProfile(PatientId),

    CONSTRAINT CK_TriageSession_Status
        CHECK (Status IN ('Active', 'Completed', 'Cancelled')),

    CONSTRAINT CK_TriageSession_Time
        CHECK (EndTime IS NULL OR EndTime >= StartTime)
);