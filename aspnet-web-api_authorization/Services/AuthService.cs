using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.IdentityModel.Tokens;
using TaskFlow.Api.DTOs;
using TaskFlow.Api.Models;

namespace TaskFlow.Api.Services;

public class AuthService : IAuthService
{
    private readonly IConfiguration _configuration;

    private static readonly List<User> _users = new()
    {
        new User
        {
            Id = 1,
            Username = "admin",
            Email = "admin@taskflow.com",
            PasswordHash = BCryptHash("admin123"),
            Role = "Admin"
        },
        new User
        {
            Id = 2,
            Username = "user",
            Email = "user@taskflow.com",
            PasswordHash = BCryptHash("user123"),
            Role = "User"
        }
    };

    public AuthService(IConfiguration configuration)
    {
        _configuration = configuration;
    }

    public Task<LoginResponseDto?> AuthenticateAsync(LoginDto dto)
    {
        var user = _users.FirstOrDefault(u =>
            u.Username.Equals(dto.Username, StringComparison.OrdinalIgnoreCase));

        if (user == null || !VerifyPassword(dto.Password, user.PasswordHash))
            return Task.FromResult<LoginResponseDto?>(null);

        var token = GenerateJwtToken(user);

        var response = new LoginResponseDto
        {
            Token = token.Token,
            ExpiresAt = token.ExpiresAt,
            Username = user.Username,
            Role = user.Role
        };

        return Task.FromResult<LoginResponseDto?>(response);
    }

    private (string Token, DateTime ExpiresAt) GenerateJwtToken(User user)
    {
        var secret = _configuration["Jwt:Secret"]!;
        var issuer = _configuration["Jwt:Issuer"]!;
        var audience = _configuration["Jwt:Audience"]!;
        var expirationMinutes = int.Parse(_configuration["Jwt:ExpirationMinutes"] ?? "60");

        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secret));
        var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var claims = new[]
        {
            new Claim(JwtRegisteredClaimNames.Sub, user.Id.ToString()),
            new Claim(JwtRegisteredClaimNames.Email, user.Email),
            new Claim(ClaimTypes.Role, user.Role),
            new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString())
        };

        var expiresAt = DateTime.UtcNow.AddMinutes(expirationMinutes);

        var token = new JwtSecurityToken(
            issuer: issuer,
            audience: audience,
            claims: claims,
            expires: expiresAt,
            signingCredentials: credentials);

        return (new JwtSecurityTokenHandler().WriteToken(token), expiresAt);
    }

    private static string BCryptHash(string password)
    {
        // Simple hash for demo purposes — in production use BCrypt or Argon2
        using var sha = System.Security.Cryptography.SHA256.Create();
        var bytes = sha.ComputeHash(Encoding.UTF8.GetBytes(password));
        return Convert.ToBase64String(bytes);
    }

    private static bool VerifyPassword(string password, string hash)
    {
        return BCryptHash(password) == hash;
    }
}
