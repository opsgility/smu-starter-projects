package com.skillmeup.library;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Book book = new Book("Clean Code", "Robert Martin", "9780132350884", 2008, true);
        System.out.println(book);

        Scanner scanner = new Scanner(System.in);

        // TODO Exercise 1: Declare boolean running = true; then wrap the menu in:
        //   while (running) { ... }
        // Inside the loop print:
        //   "1) View book  2) Toggle availability  3) Exit"
        // and read the user choice with scanner.nextInt()

        // TODO Exercise 2: Add a switch statement on the choice:
        //   case 1 -> print the book
        //   case 2 -> toggle book.setAvailable(!book.isAvailable()), print "Status changed."
        //   case 3 -> set running = false; print "Goodbye!"
        //   default -> print "Invalid choice."

        // TODO Exercise 3: After the switch, use an if statement:
        //   if (!book.isAvailable()) System.out.println("Note: book is currently checked out.");

        scanner.close();
    }
}
