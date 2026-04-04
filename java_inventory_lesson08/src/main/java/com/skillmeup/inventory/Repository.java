package com.skillmeup.inventory;

import java.util.List;

/**
 * TODO Exercise 1: Define a generic interface Repository<T> with these method signatures:
 *   void   save(T item);
 *   T      findById(String id);
 *   List<T> findAll();
 *   boolean delete(String id);
 *
 * Use generic type parameter <T extends Identifiable> once you define Identifiable below.
 * For now, use plain <T>.
 */
public interface Repository<T> {
    // TODO: add method signatures here
}
