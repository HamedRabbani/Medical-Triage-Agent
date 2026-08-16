USE MedicalTriageDB;
GO


-- =====================================================
-- Create Roles
-- =====================================================

IF NOT EXISTS (
    SELECT 1
    FROM dbo.Role
    WHERE RoleName = 'Admin'
)
BEGIN
    INSERT INTO dbo.Role(RoleName)
    VALUES ('Admin');
END


IF NOT EXISTS (
    SELECT 1
    FROM dbo.Role
    WHERE RoleName = 'Doctor'
)
BEGIN
    INSERT INTO dbo.Role(RoleName)
    VALUES ('Doctor');
END


IF NOT EXISTS (
    SELECT 1
    FROM dbo.Role
    WHERE RoleName = 'Patient'
)
BEGIN
    INSERT INTO dbo.Role(RoleName)
    VALUES ('Patient');
END

GO



-- =====================================================
-- Create Admin User
-- Email: a.nejatian87@gmail.com
-- =====================================================

DECLARE @AdminUserId INT;
DECLARE @AdminRoleId INT;


IF NOT EXISTS (
    SELECT 1
    FROM dbo.UserAccount
    WHERE Email = 'a.nejatian87@gmail.com'
)
BEGIN

    INSERT INTO dbo.UserAccount
    (
        Email,
        PasswordHash,
        Phone,
        Status
    )
    VALUES
    (
        'a.nejatian87@gmail.com',

        'sha256$310000$bea680ad6b576e10b8ded9a299395987264cd5f1b777d6206898f692f16ad5b1$5940f2551689bec07b857b1d7c4e43ce08f29a454bfd5c6b38214ed17944f5cf',

        NULL,
        'Active'
    );


    SET @AdminUserId = SCOPE_IDENTITY();


    SELECT @AdminRoleId = RoleId
    FROM dbo.Role
    WHERE RoleName = 'Admin';


    INSERT INTO dbo.UserRole
    (
        UserId,
        RoleId
    )
    VALUES
    (
        @AdminUserId,
        @AdminRoleId
    );

END

GO



-- =====================================================
-- Create Patient User
-- Email: hamedrabbani304@gmail.com
-- =====================================================


DECLARE @PatientUserId INT;
DECLARE @PatientRoleId INT;


IF NOT EXISTS (
    SELECT 1
    FROM dbo.UserAccount
    WHERE Email = 'hamedrabbani304@gmail.com'
)
BEGIN


    INSERT INTO dbo.UserAccount
    (
        Email,
        PasswordHash,
        Phone,
        Status
    )
    VALUES
    (
        'hamedrabbani304@gmail.com',

        'sha256$310000$c796e9f2771a4d880f3483dff63796901628c7203b62674563af37ffca6c4f6f$ebefafc6ce24f3b28ce30a29e0a0c732ae0c6e140e083290ec0a88d4eb9adb03',

        NULL,
        'Active'
    );


    SET @PatientUserId = SCOPE_IDENTITY();



    SELECT @PatientRoleId = RoleId
    FROM dbo.Role
    WHERE RoleName = 'Patient';



    INSERT INTO dbo.UserRole
    (
        UserId,
        RoleId
    )
    VALUES
    (
        @PatientUserId,
        @PatientRoleId
    );



    INSERT INTO dbo.PatientProfile
    (
        UserId,
        FirstName,
        LastName,
        DateOfBirth,
        Gender,
        NationalId,
        CreatedAt
    )
    VALUES
    (
        @PatientUserId,
        'Hamed',
        'Rabbani',
        '1997-01-01',
        'Male',
        'DEMO-HAMED-001',
        GETDATE()
    );


END

GO