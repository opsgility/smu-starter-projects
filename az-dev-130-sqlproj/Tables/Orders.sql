CREATE TABLE [dbo].[Orders]
(
    [OrderId]    INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    [CustomerId] INT NOT NULL,
    [PlacedUtc]  DATETIME2 NOT NULL,
    [Status]     NVARCHAR(30) NOT NULL,
    CONSTRAINT [FK_Orders_Customer] FOREIGN KEY ([CustomerId]) REFERENCES [dbo].[Customer]([CustomerId])
);
GO

CREATE INDEX [IX_Orders_PlacedUtc] ON [dbo].[Orders]([PlacedUtc]);
