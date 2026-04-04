package com.skillmeup.library;

import java.util.Scanner;

public class Main {
    static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.println("=== Library Management System ===");
        BookCatalog catalog = new BookCatalog();
        boolean running = true;

        while (running) {
            System.out.println("\n1) Add book  2) Find by ISBN  3) List all  4) Remove  5) Exit");
            System.out.print("Choice: ");
            int choice = scanner.nextInt(); scanner.nextLine();

            switch (choice) {
                case 1 -> {
                    String isbn = promptForIsbn();
                    int year = parseYear();
                    System.out.print("Title: ");  String title  = scanner.nextLine();
                    System.out.print("Author: "); String author = scanner.nextLine();
                    catalog.addBook(new Book(title, author, isbn, year, true));
                    System.out.println("Added.");
                }
                case 2 -> {
                    System.out.print("ISBN: "); String isbn = scanner.nextLine();
                    Book b = catalog.findByIsbn(isbn);
                    System.out.println(b != null ? formatBook(b) : "Not found.");
                }
                case 3 -> {
                    if (catalog.getAllBooks().isEmpty()) System.out.println("Empty catalog.");
                    else catalog.getAllBooks().forEach(b -> System.out.println(formatBook(b)));
                }
                case 4 -> {
                    System.out.print("ISBN: "); String isbn = scanner.nextLine();
                    System.out.println(catalog.removeBook(isbn) ? "Removed." : "Not found.");
                }
                case 5 -> { running = false; System.out.println("Goodbye!"); }
                default -> System.out.println("Invalid choice.");
            }
        }
        scanner.close();
    }

    public static String formatBook(Book b) {
        return "\"" + b.getTitle() + "\" by " + b.getAuthor() +
               " (" + b.getYear() + ") [" + b.getIsbn() + "] - " +
               (b.isAvailable() ? "AVAILABLE" : "CHECKED OUT");
    }

    public static int parseYear() {
        System.out.print("Enter publication year: ");
        int y = scanner.nextInt(); scanner.nextLine();
        if (y < 1450 || y > 2025) { System.out.println("Invalid year. Using 2000."); return 2000; }
        return y;
    }

    public static String promptForIsbn() {
        System.out.print("Enter ISBN (13 digits): ");
        String isbn = scanner.nextLine();
        if (isbn.length() != 13 || !isbn.chars().allMatch(Character::isDigit)) {
            System.out.println("Invalid ISBN. Using 0000000000000."); return "0000000000000";
        }
        return isbn;
    }
}
