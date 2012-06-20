select  p.name 'roleName' , pm.name 'userName' from sys.database_role_members rm 
	inner join sys.database_principals p on rm.role_principal_id = p.principal_id
	inner join sys.database_principals pm on rm.member_principal_id = pm.principal_id
order by roleName 