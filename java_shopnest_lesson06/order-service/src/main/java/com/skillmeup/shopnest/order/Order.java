package com.skillmeup.shopnest.order;
import jakarta.persistence.*;
import java.time.LocalDateTime;
@Entity @Table(name="orders")
public class Order {
    @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id;
    private Long productId;
    private int quantity;
    private double totalPrice;
    private String status;
    private LocalDateTime createdAt;
    public Order() {}
    public Order(Long productId, int quantity, double totalPrice) {
        this.productId=productId; this.quantity=quantity; this.totalPrice=totalPrice;
        this.status="PENDING"; this.createdAt=LocalDateTime.now();
    }
    public Long getId() { return id; } public Long getProductId() { return productId; }
    public int getQuantity() { return quantity; } public double getTotalPrice() { return totalPrice; }
    public String getStatus() { return status; } public LocalDateTime getCreatedAt() { return createdAt; }
    public void setStatus(String s) { this.status=s; }
}
