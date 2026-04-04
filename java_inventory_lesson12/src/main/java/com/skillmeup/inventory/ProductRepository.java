package com.skillmeup.inventory;

import java.util.ArrayList;
import java.util.List;

public class ProductRepository implements Repository<Product> {
    private ArrayList<Product> storage = new ArrayList<>();

    @Override public void    save(Product p)     { storage.add(p); }
    @Override public Product findById(String id) {
        return storage.stream().filter(p -> p.getId().equalsIgnoreCase(id)).findFirst().orElse(null);
    }
    @Override public List<Product> findAll()     { return List.copyOf(storage); }
    @Override public boolean delete(String id)   { return storage.removeIf(p -> p.getId().equalsIgnoreCase(id)); }
}
