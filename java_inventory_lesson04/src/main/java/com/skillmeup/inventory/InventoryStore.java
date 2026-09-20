package com.skillmeup.inventory;

import java.util.ArrayList;
import java.util.List;

public class InventoryStore {

    // TODO Exercise 1: Declare private ArrayList<Product> products = new ArrayList<>();

    // TODO Exercise 2: Implement addProduct(Product p) — add to the list.
    // Also implement getByIndex(int index) returning products.get(index)
    // and size() returning products.size().

    // TODO Exercise 3: Implement removeProduct(String id) — remove the product whose getId() matches.
    // Use an iterator or removeIf(). Return true if removed, false if not found.
    // Also implement listAll() returning List.copyOf(products).

    // Stubs so project compiles:
    public void        addProduct(Product p)     { }
    public Product     getByIndex(int index)     { return null; }
    public int         size()                    { return 0; }
    public boolean     removeProduct(String id)  { return false; }
    public List<Product> listAll()               { return new ArrayList<>(); }
}
