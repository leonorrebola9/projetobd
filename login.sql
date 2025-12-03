CREATE LOGIN adriana WITH PASSWORD = '12345', CHECK_POLICY = OFF;
USE projeto;
CREATE USER adriana FOR LOGIN adriana;
EXEC sp_addrolemember 'db_owner', 'adriana';