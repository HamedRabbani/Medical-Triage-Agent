CREATE TABLE dbo.TriageResult
(
    ResultId BIGINT IDENTITY(1,1) NOT NULL,
    SessionId BIGINT NOT NULL,
    RiskLevel VARCHAR(20) NOT NULL,
    ConfidenceScore DECIMAL(5,2) NOT NULL,
    Recommendation NVARCHAR(MAX) NOT NULL,
    CreatedAt DATETIME2(0) NOT NULL
        CONSTRAINT DF_TriageResult_CreatedAt
        DEFAULT SYSUTCDATETIME(),

    CONSTRAINT PK_TriageResult
        PRIMARY KEY (ResultId),

    CONSTRAINT FK_TriageResult_TriageSession
        FOREIGN KEY (SessionId)
        REFERENCES dbo.TriageSession(SessionId),

    CONSTRAINT CK_TriageResult_RiskLevel
        CHECK (RiskLevel IN ('Low', 'Medium', 'High', 'Emergency')),

    CONSTRAINT CK_TriageResult_ConfidenceScore
        CHECK (ConfidenceScore >= 0 AND ConfidenceScore <= 100)
);