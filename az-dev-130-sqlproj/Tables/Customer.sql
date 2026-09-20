CREATE TABLE [dbo].[Customer]
(
    [CustomerId] INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    [Name]       NVARCHAR(80) NOT NULL,
    [Email]      NVARCHAR(200) NOT NULL
);
GO

CREATE UNIQUE INDEX [IX_Customer_Email] ON [dbo].[Customer]([Email]);
