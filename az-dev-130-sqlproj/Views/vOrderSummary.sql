CREATE VIEW [dbo].[vOrderSummary]
AS
SELECT
    o.[OrderId],
    o.[PlacedUtc],
    o.[Status],
    c.[Name]  AS CustomerName,
    c.[Email] AS CustomerEmail
FROM [dbo].[Orders]  o
JOIN [dbo].[Customer] c ON c.[CustomerId] = o.[CustomerId];
