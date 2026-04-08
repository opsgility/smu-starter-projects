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

    // Sorts by natural order (Product.compareTo() — alphabetical by name)
    // NOTE: Product.compareTo() currently returns 0 (stub) — complete Exercise 1 first!
    public List<Product> sortByName() {
        List<Product> list = new ArrayList<>(repo.findAll());
        Collections.sort(list); // uses Comparable (Product.compareTo())
        return list;
    }

    // TODO Exercise 2: Implement sortByPrice() using Comparator.comparingDouble(Product::getUnitPrice)
    public List<Product> sortByPrice() {
        return new ArrayList<>(repo.findAll()); // TODO: sort before returning
    }

    // TODO Exercise 2: Implement sortByQuantity() using Comparator.comparingInt(Product::getQuantity)
    public List<Product> sortByQuantity() {
        return new ArrayList<>(repo.findAll()); // TODO: sort before returning
    }

    // TODO Exercise 3: Implement sortByCategoryThenPrice() using
    // Comparator.comparing(Product::getCategory).thenComparingDouble(Product::getUnitPrice)
    public List<Product> sortByCategoryThenPrice() {
        return new ArrayList<>(repo.findAll()); // TODO: sort before returning
    }
}
