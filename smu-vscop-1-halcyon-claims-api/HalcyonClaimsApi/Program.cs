using HalcyonClaimsApi.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();

builder.Services.AddSingleton<IClaimValidationService, ClaimValidationService>();
builder.Services.AddSingleton<IClaimTriageService, ClaimTriageService>();

var app = builder.Build();

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();
