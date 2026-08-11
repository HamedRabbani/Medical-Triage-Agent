CREATE TABLE dbo.UserRole
(
    UserRoleId INT IDENTITY(1,1) NOT NULL,
    UserId INT NOT NULL,
    RoleId INT NOT NULL,

    CONSTRAINT PK_UserRole
        PRIMARY KEY (UserRoleId),

    CONSTRAINT FK_UserRole_UserAccount
        FOREIGN KEY (UserId)
        REFERENCES dbo.UserAccount(UserId),

    CONSTRAINT FK_UserRole_Role
        FOREIGN KEY (RoleId)
        REFERENCES dbo.Role(RoleId),

    CONSTRAINT UQ_UserRole_User_Role
        UNIQUE (UserId, RoleId)
);