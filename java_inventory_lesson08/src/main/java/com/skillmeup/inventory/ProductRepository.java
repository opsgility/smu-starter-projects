package com.skillmeup.inventory;

import java.util.ArrayList;
import java.util.List;

/**
 * TODO Exercise 2: Make ProductRepository implement Repository<Product>.
 * Add private ArrayList<Product> storage = new ArrayList<>();
 * Implement all four interface methods:
 *   save(Product p)       — adds to storage
 *   findById(String id)   — searches by product id
 *   findAll()             — returns List.copyOf(storage)
 *   delete(String id)     — removes by id, returns true/false
 */
public class ProductRepository {
    // TODO: add implements Repository<Product>

    // Stub methods so the project compiles:
    public void           save(Product p)      { }
    public Product        findById(String id)  { return null; }
    public List<Product>  findAll()            { return new ArrayList<>(); }
    public boolean        delete(String id)    { return false; }
}
