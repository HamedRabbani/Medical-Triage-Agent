CREATE TABLE dbo.Role
(
    RoleId INT IDENTITY(1,1) NOT NULL,
    RoleName NVARCHAR(50) NOT NULL,

    CONSTRAINT PK_Role
        PRIMARY KEY (RoleId),

    CONSTRAINT UQ_Role_RoleName
        UNIQUE (RoleName)
);