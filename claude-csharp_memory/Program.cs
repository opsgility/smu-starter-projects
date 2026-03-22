using MemoryApp;

var userService = new UserService();
var orderService = new OrderService();

var user = userService.Create("Alice", "alice@example.com");
var order = orderService.Create(user.id, 99.99m);

Console.WriteLine($"User: {user.name} ({user.email})");
Console.WriteLine($"Order: #{order.Id} - {order.Total:C}");
