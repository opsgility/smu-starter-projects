using System.Security.Claims;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.Identity.Web;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApi(builder.Configuration.GetSection("AzureAdB2C"));

var app = builder.Build();
app.UseSwagger();
app.UseAuthentication();
app.UseAuthorization();

var v1 = app.MapGroup("/v1").RequireAuthorization();

v1.MapGet("/tasks", (ClaimsPrincipal user) =>
{
    var tid = user.FindFirst("tid")?.Value ?? "unknown";
    return new[] { new { id = "tsk-1", tenantId = tid, title = "Sample" } };
});

v1.MapGet("/projects/{projectId}/tasks", (string projectId, ClaimsPrincipal user) =>
{
    var tid = user.FindFirst("tid")?.Value ?? "unknown";
    return new[] { new { id = "tsk-2", tenantId = tid, projectId, title = "In project" } };
});

app.Run();
