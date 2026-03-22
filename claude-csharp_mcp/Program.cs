using Microsoft.Data.Sqlite;

const string dbPath = "library.db";

if (File.Exists(dbPath))
{
    File.Delete(dbPath);
}

using var connection = new SqliteConnection($"Data Source={dbPath}");
connection.Open();

// Create tables
var createTables = connection.CreateCommand();
createTables.CommandText = @"
    CREATE TABLE Authors (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Country TEXT NOT NULL,
        BirthYear INTEGER NOT NULL
    );

    CREATE TABLE Genres (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Description TEXT NOT NULL
    );

    CREATE TABLE Books (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT NOT NULL,
        AuthorId INTEGER NOT NULL,
        GenreId INTEGER NOT NULL,
        PublicationYear INTEGER NOT NULL,
        ISBN TEXT NOT NULL,
        FOREIGN KEY (AuthorId) REFERENCES Authors(Id),
        FOREIGN KEY (GenreId) REFERENCES Genres(Id)
    );
";
createTables.ExecuteNonQuery();

// Seed Authors
var insertAuthors = connection.CreateCommand();
insertAuthors.CommandText = @"
    INSERT INTO Authors (Name, Country, BirthYear) VALUES ('George Orwell', 'United Kingdom', 1903);
    INSERT INTO Authors (Name, Country, BirthYear) VALUES ('Jane Austen', 'United Kingdom', 1775);
    INSERT INTO Authors (Name, Country, BirthYear) VALUES ('Mark Twain', 'United States', 1835);
    INSERT INTO Authors (Name, Country, BirthYear) VALUES ('Gabriel Garcia Marquez', 'Colombia', 1927);
    INSERT INTO Authors (Name, Country, BirthYear) VALUES ('Haruki Murakami', 'Japan', 1949);
";
insertAuthors.ExecuteNonQuery();

// Seed Genres
var insertGenres = connection.CreateCommand();
insertGenres.CommandText = @"
    INSERT INTO Genres (Name, Description) VALUES ('Dystopian', 'Fiction set in a dark, oppressive society');
    INSERT INTO Genres (Name, Description) VALUES ('Satire', 'Literature that uses humor and irony to criticize');
    INSERT INTO Genres (Name, Description) VALUES ('Romance', 'Fiction centered on romantic relationships');
    INSERT INTO Genres (Name, Description) VALUES ('Adventure', 'Fiction involving exciting journeys and experiences');
    INSERT INTO Genres (Name, Description) VALUES ('Magical Realism', 'Fiction blending magical elements with reality');
    INSERT INTO Genres (Name, Description) VALUES ('Literary Fiction', 'Character-driven fiction with artistic merit');
";
insertGenres.ExecuteNonQuery();

// Seed Books
var insertBooks = connection.CreateCommand();
insertBooks.CommandText = @"
    INSERT INTO Books (Title, AuthorId, GenreId, PublicationYear, ISBN) VALUES ('1984', 1, 1, 1949, '978-0451524935');
    INSERT INTO Books (Title, AuthorId, GenreId, PublicationYear, ISBN) VALUES ('Animal Farm', 1, 2, 1945, '978-0451526342');
    INSERT INTO Books (Title, AuthorId, GenreId, PublicationYear, ISBN) VALUES ('Pride and Prejudice', 2, 3, 1813, '978-0141439518');
    INSERT INTO Books (Title, AuthorId, GenreId, PublicationYear, ISBN) VALUES ('Sense and Sensibility', 2, 3, 1811, '978-0141439662');
    INSERT INTO Books (Title, AuthorId, GenreId, PublicationYear, ISBN) VALUES ('The Adventures of Tom Sawyer', 3, 4, 1876, '978-0143039563');
    INSERT INTO Books (Title, AuthorId, GenreId, PublicationYear, ISBN) VALUES ('Adventures of Huckleberry Finn', 3, 4, 1884, '978-0142437179');
    INSERT INTO Books (Title, AuthorId, GenreId, PublicationYear, ISBN) VALUES ('One Hundred Years of Solitude', 4, 5, 1967, '978-0060883287');
    INSERT INTO Books (Title, AuthorId, GenreId, PublicationYear, ISBN) VALUES ('Love in the Time of Cholera', 4, 5, 1985, '978-0307389732');
    INSERT INTO Books (Title, AuthorId, GenreId, PublicationYear, ISBN) VALUES ('Norwegian Wood', 5, 6, 1987, '978-0375704024');
    INSERT INTO Books (Title, AuthorId, GenreId, PublicationYear, ISBN) VALUES ('Kafka on the Shore', 5, 6, 2002, '978-1400079278');
";
insertBooks.ExecuteNonQuery();

// Verify seed data
var count = connection.CreateCommand();
count.CommandText = "SELECT COUNT(*) FROM Authors";
Console.WriteLine($"Authors: {count.ExecuteScalar()}");

count.CommandText = "SELECT COUNT(*) FROM Books";
Console.WriteLine($"Books: {count.ExecuteScalar()}");

count.CommandText = "SELECT COUNT(*) FROM Genres";
Console.WriteLine($"Genres: {count.ExecuteScalar()}");

Console.WriteLine($"Database created at: {Path.GetFullPath(dbPath)}");
