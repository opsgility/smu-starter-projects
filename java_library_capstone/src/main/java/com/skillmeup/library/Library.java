package com.skillmeup.library;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.stream.Collectors;

public class Library implements Loanable {
    private HashMap<String, Book>  books           = new HashMap<>();
    private HashSet<String>        checkedOutIsbns = new HashSet<>();
    private ArrayList<Loan>        loans           = new ArrayList<>();
    private ArrayList<Patron>      patrons         = new ArrayList<>();
    private Book    pendingBook    = null;
    private Patron  pendingPatron  = null;

    public void addBook(Book book)       { books.put(book.getIsbn(), book); }
    public Book findBook(String isbn)    { return books.get(isbn); }
    public void registerPatron(Patron p) { patrons.add(p); }
    public List<Book>   getAllBooks()    { return new ArrayList<>(books.values()); }
    public List<Patron> getAllPatrons()  { return List.copyOf(patrons); }
    public List<Loan>   getActiveLoans(){ return List.copyOf(loans); }

    // TODO Capstone Exercise 1: Implement checkOut(String isbn, Patron patron)
    // Steps:
    //   1. Look up book by isbn; if null, print "Book not found." and return false.
    //   2. If checkedOutIsbns contains isbn, print "Already checked out." and return false.
    //   3. Call book.setAvailable(false), add isbn to checkedOutIsbns.
    //   4. Create new Loan(book, patron, LocalDate.now()) and add to loans list.
    //   5. Return true.
    public boolean checkOut(String isbn, Patron patron) {
        return false; // TODO: implement this
    }

    // TODO Capstone Exercise 2: Implement returnBook(String isbn)
    // Steps:
    //   1. If isbn not in checkedOutIsbns, print "Not checked out." and return false.
    //   2. Call findBook(isbn).setAvailable(true), remove isbn from checkedOutIsbns.
    //   3. Return true.
    public boolean returnBook(String isbn) {
        return false; // TODO: implement this
    }

    // TODO Capstone Exercise 3: Implement getOverdueLoans()
    // Return loans filtered to where isOverdue() == true.
    // Hint: loans.stream().filter(Loan::isOverdue).collect(Collectors.toList())
    public List<Loan> getOverdueLoans() {
        return new ArrayList<>(); // TODO: implement this
    }

    // Loanable interface — delegates to the checkOut/returnBook methods above
    @Override public void checkOut(Patron patron) { }
    @Override public void returnItem() { }
}
