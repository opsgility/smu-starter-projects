package com.skillmeup.shopnest.product;
import jakarta.persistence.*;
@Entity @Table(name="products")
public class Product {
    @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id;
    @Column(nullable=false) private String name;
    private String description;
    private double price;
    private int stockQuantity;
    public Product() {}
    public Product(String name, String description, double price, int stockQuantity) {
        this.name=name; this.description=description; this.price=price; this.stockQuantity=stockQuantity;
    }
    public Long getId() { return id; }
    public String getName() { return name; }
    public String getDescription() { return description; }
    public double getPrice() { return price; }
    public int getStockQuantity() { return stockQuantity; }
    public void setName(String n) { this.name=n; }
    public void setDescription(String d) { this.description=d; }
    public void setPrice(double p) { this.price=p; }
    public void setStockQuantity(int q) { this.stockQuantity=q; }
}
