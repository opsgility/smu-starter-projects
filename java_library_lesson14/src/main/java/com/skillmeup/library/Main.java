package com.skillmeup.library;

import java.util.Scanner;

public class Main {
    static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        Library library = new Library();
        boolean running = true;
        while (running) {
            System.out.println("\n=== Library ===");
            System.out.println("1) Add book  2) Register patron  3) Check out  4) Return  5) Loans  6) Exit");
            System.out.print("Choice: ");
            int choice = scanner.nextInt(); scanner.nextLine();
            switch (choice) {
                case 1 -> {
                    System.out.print("ISBN: "); String isbn = scanner.nextLine();
                    System.out.print("Title: "); String title = scanner.nextLine();
                    System.out.print("Author: "); String author = scanner.nextLine();
                    library.addBook(new Book(title, author, isbn, 2020, true));
                    System.out.println("Added.");
                }
                case 2 -> {
                    System.out.print("Name: "); String name = scanner.nextLine();
                    System.out.print("ID: "); String pid = scanner.nextLine();
                    System.out.print("Email: "); String email = scanner.nextLine();
                    library.registerPatron(new Patron(name, pid, email));
                    System.out.println("Registered.");
                }
                case 3 -> {
                    System.out.print("ISBN: "); String isbn = scanner.nextLine();
                    System.out.print("Patron ID: "); String pid = scanner.nextLine();
                    Patron p = library.getAllPatrons().stream()
                            .filter(x -> x.getPatronId().equals(pid)).findFirst().orElse(null);
                    if (p == null) { System.out.println("Patron not found."); break; }
                    System.out.println(library.checkOut(isbn, p) ? "Checked out." : "Unavailable.");
                }
                case 4 -> {
                    System.out.print("ISBN: "); String isbn = scanner.nextLine();
                    System.out.println(library.returnBook(isbn) ? "Returned." : "Not checked out.");
                }
                case 5 -> library.getActiveLoans().forEach(l ->
                    System.out.println(l.getBook().getTitle() + " -> " + l.getPatron().getName()));
                case 6 -> { running = false; System.out.println("Goodbye!"); }
                default -> System.out.println("Invalid.");
            }
        }
        scanner.close();
    }
}
