using LumenLogistics.Api.Data;
using LumenLogistics.Api.Models;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddSingleton<PackageStore>();

var app = builder.Build();

app.MapGet("/", () => Results.Ok(new
{
    service = "LumenLogistics.Api",
    version = "0.1.0",
    docs = "/packages"
}));

app.MapGet("/packages", (PackageStore store) => Results.Ok(store.All()));

app.MapGet("/packages/{id}", (string id, PackageStore store) =>
    store.Get(id) is { } p ? Results.Ok(p) : Results.NotFound());

app.MapPost("/packages", (Package pkg, PackageStore store) =>
{
    var created = store.Add(pkg);
    return Results.Created($"/packages/{created.Id}", created);
});

app.Run();
