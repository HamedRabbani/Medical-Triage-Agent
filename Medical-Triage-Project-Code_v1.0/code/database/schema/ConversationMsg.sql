CREATE TABLE dbo.ConversationMsg
(
    MessageId BIGINT IDENTITY(1,1) NOT NULL,
    SessionId BIGINT NOT NULL,
    SenderType VARCHAR(20) NOT NULL,
    Content NVARCHAR(MAX) NOT NULL,
    Timestamp DATETIME2(0) NOT NULL
        CONSTRAINT DF_ConversationMsg_Timestamp
        DEFAULT SYSUTCDATETIME(),

    CONSTRAINT PK_ConversationMsg
        PRIMARY KEY (MessageId),

    CONSTRAINT FK_ConversationMsg_TriageSession
        FOREIGN KEY (SessionId)
        REFERENCES dbo.TriageSession(SessionId),

    CONSTRAINT CK_ConversationMsg_SenderType
        CHECK (SenderType IN ('Patient', 'Agent', 'Doctor', 'System'))
);