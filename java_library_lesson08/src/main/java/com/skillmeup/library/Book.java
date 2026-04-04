package com.skillmeup.library;

public class Book {
    private String title;
    private String author;
    private String isbn;
    private int year;
    private boolean available;

    public Book(String title, String author, String isbn, int year, boolean available) {
        if (title == null || title.isBlank()) throw new IllegalArgumentException("Title cannot be blank");
        if (year < 1450 || year > 2025)       throw new IllegalArgumentException("Year out of range: " + year);
        this.title = title; this.author = author; this.isbn = isbn;
        this.year = year;   this.available = available;
    }

    public String  getTitle()    { return title; }
    public String  getAuthor()   { return author; }
    public String  getIsbn()     { return isbn; }
    public int     getYear()     { return year; }
    public boolean isAvailable() { return available; }
    public void    setAvailable(boolean available) { this.available = available; }

    @Override
    public String toString() {
        return title + " by " + author + " (" + year + ") [ISBN: " + isbn + "] - Available: " + available;
    }
}
