CREATE TABLE dbo.PatientDoctor
(
    RelationId BIGINT IDENTITY(1,1) NOT NULL,
    PatientId INT NOT NULL,
    DoctorId INT NOT NULL,
    RelationshipType VARCHAR(50) NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NULL,

    CONSTRAINT PK_PatientDoctor
        PRIMARY KEY (RelationId),

    CONSTRAINT FK_PatientDoctor_Patient
        FOREIGN KEY (PatientId)
        REFERENCES dbo.PatientProfile(PatientId),

    CONSTRAINT FK_PatientDoctor_Doctor
        FOREIGN KEY (DoctorId)
        REFERENCES dbo.DoctorProfile(DoctorId),

    CONSTRAINT UQ_PatientDoctor_Patient_Doctor
        UNIQUE (PatientId, DoctorId),

    CONSTRAINT CK_PatientDoctor_Dates
        CHECK (EndDate IS NULL OR EndDate >= StartDate)
);