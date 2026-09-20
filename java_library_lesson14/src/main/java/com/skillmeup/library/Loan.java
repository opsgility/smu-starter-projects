package com.skillmeup.library;

import java.time.LocalDate;

public class Loan {
    // TODO Exercise 1: Add private fields: Book book, Patron patron,
    //   LocalDate checkoutDate, LocalDate dueDate.

    // TODO Exercise 2: Add constructor Loan(Book book, Patron patron, LocalDate checkoutDate).
    //   Set dueDate = checkoutDate.plusDays(14).

    // TODO Exercise 3: Add getters getBook(), getPatron(), getCheckoutDate(), getDueDate().
    //   Add isOverdue() that returns true if LocalDate.now().isAfter(dueDate).
}
