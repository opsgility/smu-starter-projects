package com.skillmeup.inventory;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class CategoryMap {
    private HashMap<String, Category> categories = new HashMap<>();
    private HashSet<String> tags = new HashSet<>();

    public void        addCategory(Category c)     { categories.put(c.getId(), c); }
    public Category    getCategory(String id)      { return categories.get(id); }
    public void        addTag(String tag)           { tags.add(tag); }
    public Set<String> getTags()                   { return Set.copyOf(tags); }
    public boolean     containsCategory(String id) { return categories.containsKey(id); }
    public List<Category> listCategories()         { return new ArrayList<>(categories.values()); }
}
