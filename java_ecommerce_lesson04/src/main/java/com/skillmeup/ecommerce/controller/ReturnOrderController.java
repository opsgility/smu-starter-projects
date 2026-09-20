package com.skillmeup.ecommerce.controller;

import com.skillmeup.ecommerce.model.ReturnOrder;
import com.skillmeup.ecommerce.service.ReturnOrderService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/returns")
public class ReturnOrderController {
    private final ReturnOrderService returnOrderService;

    public ReturnOrderController(ReturnOrderService returnOrderService) {
        this.returnOrderService = returnOrderService;
    }

    @GetMapping("/{id}")
    public ResponseEntity<ReturnOrder> getReturn(@PathVariable Long id) {
        return ResponseEntity.ok(returnOrderService.getReturnById(id));
    }

    @GetMapping("/order/{orderId}")
    public ResponseEntity<List<ReturnOrder>> getReturnsByOrder(@PathVariable Long orderId) {
        return ResponseEntity.ok(returnOrderService.getReturnsByOrder(orderId));
    }

    @PostMapping
    public ResponseEntity<ReturnOrder> requestReturn(@RequestBody ReturnRequest request) {
        ReturnOrder ret = returnOrderService.requestReturn(request.orderId(), request.reason());
        return ResponseEntity.status(201).body(ret);
    }

    @PostMapping("/{id}/approve")
    public ResponseEntity<ReturnOrder> approveReturn(@PathVariable Long id) {
        return ResponseEntity.ok(returnOrderService.approveReturn(id));
    }

    @PostMapping("/{id}/reject")
    public ResponseEntity<ReturnOrder> rejectReturn(@PathVariable Long id,
                                                     @RequestBody RejectRequest request) {
        return ResponseEntity.ok(returnOrderService.rejectReturn(id, request.reason()));
    }

    public record ReturnRequest(Long orderId, String reason) {}
    public record RejectRequest(String reason) {}
}
