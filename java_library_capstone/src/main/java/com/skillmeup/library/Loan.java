package com.skillmeup.library;

import java.time.LocalDate;

public class Loan {
    private Book book;
    private Patron patron;
    private LocalDate checkoutDate;
    private LocalDate dueDate;

    public Loan(Book book, Patron patron, LocalDate checkoutDate) {
        this.book = book; this.patron = patron;
        this.checkoutDate = checkoutDate;
        this.dueDate = checkoutDate.plusDays(14);
    }
    public Book      getBook()        { return book; }
    public Patron    getPatron()      { return patron; }
    public LocalDate getCheckoutDate(){ return checkoutDate; }
    public LocalDate getDueDate()     { return dueDate; }
    public boolean   isOverdue()      { return LocalDate.now().isAfter(dueDate); }
}
