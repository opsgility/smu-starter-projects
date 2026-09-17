-- Anchorline Multi-Tenant SaaS data layer, RLS-enforced.
-- Run once as the Entra admin against the DB.

IF OBJECT_ID('dbo.Orders','U') IS NOT NULL DROP TABLE dbo.Orders;
IF OBJECT_ID('dbo.Customer','U') IS NOT NULL DROP TABLE dbo.Customer;
IF EXISTS(SELECT 1 FROM sys.security_policies WHERE name = 'TenantIsolationPolicy') DROP SECURITY POLICY dbo.TenantIsolationPolicy;
IF OBJECT_ID('dbo.fn_TenantAccess','IF') IS NOT NULL DROP FUNCTION dbo.fn_TenantAccess;
GO

CREATE TABLE dbo.Customer(
    CustomerId INT IDENTITY PRIMARY KEY,
    TenantId   INT NOT NULL,
    Name       NVARCHAR(80) NOT NULL,
    Email      NVARCHAR(200) NOT NULL,
    INDEX IX_Customer_TenantId (TenantId)
);
GO

CREATE TABLE dbo.Orders(
    OrderId    INT IDENTITY PRIMARY KEY,
    TenantId   INT NOT NULL,
    CustomerId INT NOT NULL,
    PlacedUtc  DATETIME2 NOT NULL,
    Status     NVARCHAR(30) NOT NULL,
    Amount     DECIMAL(10,2) NOT NULL,
    INDEX IX_Orders_TenantId_PlacedUtc (TenantId, PlacedUtc)
);
GO

-- Row-Level Security predicate function.
-- Reads the current SESSION_CONTEXT('TenantId') and returns 1 for matching rows.
CREATE FUNCTION dbo.fn_TenantAccess(@TenantId INT)
RETURNS TABLE WITH SCHEMABINDING AS
RETURN SELECT 1 AS Allowed
WHERE @TenantId = CONVERT(INT, SESSION_CONTEXT(N'TenantId'));
GO

CREATE SECURITY POLICY dbo.TenantIsolationPolicy
    ADD FILTER PREDICATE dbo.fn_TenantAccess(TenantId) ON dbo.Customer,
    ADD FILTER PREDICATE dbo.fn_TenantAccess(TenantId) ON dbo.Orders,
    ADD BLOCK  PREDICATE dbo.fn_TenantAccess(TenantId) ON dbo.Customer AFTER INSERT,
    ADD BLOCK  PREDICATE dbo.fn_TenantAccess(TenantId) ON dbo.Customer AFTER UPDATE,
    ADD BLOCK  PREDICATE dbo.fn_TenantAccess(TenantId) ON dbo.Orders   AFTER INSERT,
    ADD BLOCK  PREDICATE dbo.fn_TenantAccess(TenantId) ON dbo.Orders   AFTER UPDATE
WITH (STATE = ON, SCHEMABINDING = ON);
GO
