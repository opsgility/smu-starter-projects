package com.skillmeup.inventory;

import java.util.ArrayList;
import java.util.List;

public interface Repository<T> {
    void    save(T item);
    T       findById(String id);
    List<T> findAll();
    boolean delete(String id);
}
