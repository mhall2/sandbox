Select COUNT(*) 'Number of Database Objects' , RoleName, permission_name  From
(
SELECT
    OBJECT_NAME(major_id) 'ObjName', USER_NAME(grantee_principal_id) 'RoleName', permission_name
FROM
    sys.database_permissions p
WHERE
    p.class = 1 AND
    OBJECTPROPERTY(major_id, 'IsMSSHipped') = 0
    ) as T where T.RoleName in ('Editor', 'Viewer')
    Group by RoleName , permission_name 