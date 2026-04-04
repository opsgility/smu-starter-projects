package com.skillmeup.library;

import java.util.Scanner;

public class Main {
    static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.println("=== Library Management System ===");
        boolean running = true;
        while (running) {
            System.out.println("\n1) View sample book  2) Create book  3) Exit");
            System.out.print("Choice: ");
            int choice = scanner.nextInt(); scanner.nextLine();

            switch (choice) {
                case 1 -> {
                    Book b = new Book("Clean Code", "Robert Martin", "9780132350884", 2008, true);
                    System.out.println(formatBook(b));
                }
                case 2 -> {
                    String isbn = promptForIsbn();
                    int    year = parseYear();
                    System.out.print("Enter title: ");  String title  = scanner.nextLine();
                    System.out.print("Enter author: "); String author = scanner.nextLine();
                    Book b = new Book(title, author, isbn, year, true);
                    System.out.println("Created: " + formatBook(b));
                }
                case 3 -> { running = false; System.out.println("Goodbye!"); }
                default -> System.out.println("Invalid choice.");
            }
        }
        scanner.close();
    }

    // TODO Exercise 1: Implement formatBook(Book b)
    // Return: "\"title\" by Author (year) [ISBN] - AVAILABLE" or "- CHECKED OUT"
    public static String formatBook(Book b) {
        return b.toString(); // replace with your implementation
    }

    // TODO Exercise 2: Implement parseYear()
    // Prompt "Enter publication year: ", read nextInt(), consume newline.
    // If year < 1450 or year > 2025, print "Invalid year. Using 2000." and return 2000.
    public static int parseYear() {
        return 2000; // replace with your implementation
    }

    // TODO Exercise 3: Implement promptForIsbn()
    // Prompt "Enter ISBN (13 digits): ", read nextLine().
    // If length != 13 or not all digits, print "Invalid ISBN. Using 0000000000000." and return that.
    public static String promptForIsbn() {
        return "0000000000000"; // replace with your implementation
    }
}
