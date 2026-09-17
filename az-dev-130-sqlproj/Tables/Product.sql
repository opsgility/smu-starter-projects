CREATE TABLE [dbo].[Product]
(
    [ProductId] INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    [Name]      NVARCHAR(120) NOT NULL,
    [Sku]       NVARCHAR(40) NOT NULL,
    [Price]     DECIMAL(10,2) NOT NULL
);
GO

CREATE UNIQUE INDEX [IX_Product_Sku] ON [dbo].[Product]([Sku]);
