package com.skillmeup.library;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;

public class Library {

    // TODO Exercise 1: Replace this stub with proper fields:
    //   private HashMap<String, Book> books = new HashMap<>();
    //   private HashSet<String> checkedOutIsbns = new HashSet<>();
    //   private ArrayList<Loan> loans = new ArrayList<>();
    //   private ArrayList<Patron> patrons = new ArrayList<>();

    // TODO Exercise 2: Implement addBook(Book book) using books.put(isbn, book)
    //   and findBook(String isbn) using books.get(isbn).

    // TODO Exercise 3: Implement registerPatron(Patron patron),
    //   checkOut(String isbn, Patron patron) that creates a Loan and tracks the ISBN,
    //   and returnBook(String isbn) that clears the checkout.

    // Stubs so project compiles:
    public void        addBook(Book b)               { }
    public Book        findBook(String isbn)          { return null; }
    public void        registerPatron(Patron p)       { }
    public boolean     checkOut(String isbn, Patron p){ return false; }
    public boolean     returnBook(String isbn)        { return false; }
    public List<Loan>  getActiveLoans()               { return new ArrayList<>(); }
    public List<Book>  getAllBooks()                  { return new ArrayList<>(); }
    public List<Patron>getAllPatrons()                { return new ArrayList<>(); }
}
