package com.skillmeup.inventory;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public class InventoryStore {
    private ProductRepository repo = new ProductRepository();

    public void    addProduct(Product p)    { repo.save(p); }
    public Product findById(String id)      { return repo.findById(id); }
    public boolean removeProduct(String id) { return repo.delete(id); }
    public List<Product> listAll()          { return repo.findAll(); }

    // TODO Exercise 2: Implement sortByName()
    // Get a mutable copy of repo.findAll(), call Collections.sort(list) (uses Comparable),
    // and return the sorted list.
    public List<Product> sortByName() {
        return new ArrayList<>(repo.findAll()); // TODO: sort this before returning
    }

    // TODO Exercise 3: Implement sortByPrice() using a Comparator lambda:
    // Comparator.comparingDouble(Product::getUnitPrice)
    // and sortByQuantity() using Comparator.comparingInt(Product::getQuantity)
    public List<Product> sortByPrice()    { return new ArrayList<>(repo.findAll()); }
    public List<Product> sortByQuantity() { return new ArrayList<>(repo.findAll()); }
}
