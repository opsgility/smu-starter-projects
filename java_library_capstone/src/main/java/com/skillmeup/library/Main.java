package com.skillmeup.library;

import java.util.Scanner;

public class Main {
    static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        Library library = new Library();
        // Pre-loaded data
        library.addBook(new Book("Clean Code",               "Robert Martin",  "9780132350884", 2008, true));
        library.addBook(new Book("The Pragmatic Programmer", "Hunt & Thomas",  "9780201616224", 1999, true));
        library.addBook(new Book("Design Patterns",          "Gang of Four",   "9780201633610", 1994, true));
        library.registerPatron(new Patron("Alice Smith",  "P001", "alice@example.com"));
        library.registerPatron(new Patron("Bob Johnson",  "P002", "bob@example.com"));

        boolean running = true;
        while (running) {
            System.out.println("\n=== Library Management System ===");
            System.out.println("1) List books  2) List patrons  3) Check out  4) Return");
            System.out.println("5) Active loans  6) Overdue loans  7) Exit");
            System.out.print("Choice: ");
            int choice = scanner.nextInt(); scanner.nextLine();

            switch (choice) {
                case 1 -> library.getAllBooks().forEach(b -> System.out.println("  " + b));
                case 2 -> library.getAllPatrons().forEach(p -> System.out.println("  " + p));
                case 3 -> {
                    System.out.print("ISBN: "); String isbn = scanner.nextLine();
                    System.out.print("Patron ID: "); String pid = scanner.nextLine();
                    Patron p = library.getAllPatrons().stream()
                            .filter(x -> x.getPatronId().equals(pid)).findFirst().orElse(null);
                    if (p == null) { System.out.println("Patron not found."); break; }
                    System.out.println(library.checkOut(isbn, p) ? "Checked out!" : "Failed.");
                }
                case 4 -> {
                    System.out.print("ISBN: "); String isbn = scanner.nextLine();
                    System.out.println(library.returnBook(isbn) ? "Returned." : "Failed.");
                }
                case 5 -> {
                    var active = library.getActiveLoans();
                    if (active.isEmpty()) System.out.println("No active loans.");
                    else active.forEach(l -> System.out.printf("  %s -> %s (due %s)%n",
                            l.getBook().getTitle(), l.getPatron().getName(), l.getDueDate()));
                }
                case 6 -> {
                    var overdue = library.getOverdueLoans();
                    if (overdue.isEmpty()) System.out.println("No overdue loans.");
                    else overdue.forEach(l -> System.out.println("  OVERDUE: " + l.getBook().getTitle()));
                }
                case 7 -> { running = false; System.out.println("Goodbye!"); }
                default -> System.out.println("Invalid choice.");
            }
        }
        scanner.close();
    }
}
