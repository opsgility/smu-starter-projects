package com.skillmeup.inventory;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;

public class CategoryMap {

    // TODO Exercise 1: Declare private HashMap<String, Category> categories = new HashMap<>();
    // Also declare private HashSet<String> tags = new HashSet<>();

    // TODO Exercise 2: Implement addCategory(Category c) using categories.put(c.getId(), c)
    // and getCategory(String id) using categories.get(id).
    // Also implement addTag(String tag) and getTags() returning Set.copyOf(tags).

    // TODO Exercise 3: Implement listCategories() — return a new ArrayList of categories.values()
    // and containsCategory(String id) returning categories.containsKey(id).

    // Stubs so project compiles:
    public void         addCategory(Category c)      { }
    public Category     getCategory(String id)       { return null; }
    public void         addTag(String tag)            { }
    public Set<String>  getTags()                    { return new HashSet<>(); }
    public boolean      containsCategory(String id)  { return false; }
}
