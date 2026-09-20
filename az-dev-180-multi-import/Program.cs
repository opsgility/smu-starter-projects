using Microsoft.OpenApi.Models;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(o => o.SwaggerDoc("v1", new OpenApiInfo { Title = "Anchorline Customers", Version = "v1" }));
var app = builder.Build();
app.UseSwagger();
app.UseSwaggerUI();

app.MapGet("/customers", () => new[] {
    new { id = "cust-42", name = "Ada",   tier = "Standard" },
    new { id = "cust-88", name = "Grace", tier = "Premium"  },
});
app.MapGet("/customers/{id}", (string id) => Results.Ok(new { id, name = "Ada", tier = "Standard" }));

app.Run();
