-- RLS predicate function + policy for TaskForge Tasks table
CREATE OR ALTER FUNCTION dbo.fn_TenantAccessPredicate(@TenantId uniqueidentifier)
    RETURNS TABLE
    WITH SCHEMABINDING
AS
    RETURN SELECT 1 AS access_granted
    WHERE @TenantId = CAST(SESSION_CONTEXT(N'tenantId') AS uniqueidentifier)
       OR IS_MEMBER('db_owner') = 1;
GO

DROP SECURITY POLICY IF EXISTS dbo.TenantIsolationPolicy;
GO

CREATE SECURITY POLICY dbo.TenantIsolationPolicy
    ADD FILTER PREDICATE dbo.fn_TenantAccessPredicate(TenantId) ON dbo.Tasks,
    ADD BLOCK PREDICATE  dbo.fn_TenantAccessPredicate(TenantId) ON dbo.Tasks AFTER INSERT,
    ADD BLOCK PREDICATE  dbo.fn_TenantAccessPredicate(TenantId) ON dbo.Tasks AFTER UPDATE,
    ADD BLOCK PREDICATE  dbo.fn_TenantAccessPredicate(TenantId) ON dbo.Tasks BEFORE UPDATE,
    ADD BLOCK PREDICATE  dbo.fn_TenantAccessPredicate(TenantId) ON dbo.Tasks BEFORE DELETE
    WITH (STATE = ON);
GO
