package com.skillmeup.library;

import java.util.ArrayList;
import java.util.List;

public class BookCatalog {
    private ArrayList<Book> books = new ArrayList<>();

    public void addBook(Book book) {
        for (Book b : books) {
            if (b.getIsbn().equals(book.getIsbn()))
                throw new IllegalArgumentException("Duplicate ISBN: " + book.getIsbn());
        }
        books.add(book);
    }

    public Book findByIsbn(String isbn) {
        for (Book b : books) if (b.getIsbn().equalsIgnoreCase(isbn)) return b;
        return null;
    }

    public boolean removeBook(String isbn) {
        return books.removeIf(b -> b.getIsbn().equalsIgnoreCase(isbn));
    }

    public List<Book> getAllBooks() { return List.copyOf(books); }
}
