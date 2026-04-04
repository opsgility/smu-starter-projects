package com.skillmeup.library;

public interface Loanable {
    void checkOut(Patron patron);
    void returnItem();
}
