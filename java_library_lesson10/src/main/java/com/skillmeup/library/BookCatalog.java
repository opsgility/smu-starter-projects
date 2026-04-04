package com.skillmeup.library;

import java.util.ArrayList;
import java.util.List;

public class BookCatalog {

    // TODO Exercise 1: Declare private ArrayList<Book> books = new ArrayList<>();

    // TODO Exercise 2: Implement addBook(Book book)
    // Before adding, iterate the list: if any book has the same ISBN, throw
    //   new IllegalArgumentException("Duplicate ISBN: " + book.getIsbn())
    // Otherwise add to the list.

    // TODO Exercise 3: Implement findByIsbn(String isbn)
    // Loop through books; return the first where getIsbn().equalsIgnoreCase(isbn).
    // Return null if not found.

    // Bonus: implement removeBook(String isbn) — return true if removed, false if not found.
    // Bonus: implement getAllBooks() — return List.copyOf(books).

    // Stubs so the project compiles:
    public void       addBook(Book book)      { }
    public Book       findByIsbn(String isbn) { return null; }
    public boolean    removeBook(String isbn) { return false; }
    public List<Book> getAllBooks()            { return new ArrayList<>(); }
}
