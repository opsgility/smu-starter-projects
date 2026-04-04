package com.skillmeup.inventory;

import java.util.ArrayList;
import java.util.List;

public class InventoryStore {
    private ArrayList<Product> products = new ArrayList<>();

    public void addProduct(Product p) { products.add(p); }
    public Product getByIndex(int index) { return products.get(index); }
    public int size() { return products.size(); }

    public boolean removeProduct(String id) {
        return products.removeIf(p -> p.getId().equalsIgnoreCase(id));
    }

    public List<Product> listAll() { return List.copyOf(products); }
}
