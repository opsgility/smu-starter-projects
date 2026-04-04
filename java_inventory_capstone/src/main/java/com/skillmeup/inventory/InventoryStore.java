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

    public List<Product> sortByName() {
        List<Product> list = new ArrayList<>(repo.findAll());
        Collections.sort(list);
        return list;
    }
    public List<Product> sortByPrice() {
        List<Product> list = new ArrayList<>(repo.findAll());
        list.sort(Comparator.comparingDouble(Product::getUnitPrice));
        return list;
    }
    public List<Product> sortByQuantity() {
        List<Product> list = new ArrayList<>(repo.findAll());
        list.sort(Comparator.comparingInt(Product::getQuantity));
        return list;
    }
}
