INSERT INTO dbo.UserAccount
    (Email, PasswordHash, Phone, Status)
VALUES
    ('test@example.com', 'TEST_HASH', '09120000000', 'Active');
SELECT * FROM dbo.UserAccount;

INSERT INTO dbo.Role (RoleName)
VALUES ('Patient');
SELECT * FROM dbo.Role;

INSERT INTO dbo.UserRole (UserId, RoleId)
VALUES (1, 1);
SELECT * FROM dbo.UserRole;