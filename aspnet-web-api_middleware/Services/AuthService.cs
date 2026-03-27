using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.IdentityModel.Tokens;
using TaskFlow.Api.DTOs;

namespace TaskFlow.Api.Services;

public interface IAuthService
{
    AuthResponseDto? Login(LoginDto dto);
    AuthResponseDto Register(RegisterDto dto);
}

public class AuthService : IAuthService
{
    private readonly IConfiguration _configuration;

    // In-memory user store for demo purposes
    private static readonly List<UserRecord> _users = new()
    {
        new UserRecord("admin", "admin123", "Admin"),
        new UserRecord("user1", "user123", "User"),
        new UserRecord("user2", "user123", "User")
    };

    public AuthService(IConfiguration configuration)
    {
        _configuration = configuration;
    }

    public AuthResponseDto? Login(LoginDto dto)
    {
        var user = _users.FirstOrDefault(u =>
            u.Username == dto.Username && u.Password == dto.Password);

        if (user == null)
            return null;

        var token = GenerateToken(user);
        return new AuthResponseDto
        {
            Token = token,
            Username = user.Username,
            Role = user.Role
        };
    }

    public AuthResponseDto Register(RegisterDto dto)
    {
        if (_users.Any(u => u.Username == dto.Username))
            throw new InvalidOperationException("Username already exists");

        var validRoles = new[] { "User", "Admin" };
        var role = validRoles.Contains(dto.Role) ? dto.Role : "User";

        var user = new UserRecord(dto.Username, dto.Password, role);
        _users.Add(user);

        var token = GenerateToken(user);
        return new AuthResponseDto
        {
            Token = token,
            Username = user.Username,
            Role = user.Role
        };
    }

    private string GenerateToken(UserRecord user)
    {
        var key = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(_configuration["Jwt:Key"]!));
        var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var claims = new[]
        {
            new Claim(ClaimTypes.Name, user.Username),
            new Claim(ClaimTypes.NameIdentifier, user.Username),
            new Claim(ClaimTypes.Role, user.Role)
        };

        var token = new JwtSecurityToken(
            issuer: _configuration["Jwt:Issuer"],
            audience: _configuration["Jwt:Audience"],
            claims: claims,
            expires: DateTime.UtcNow.AddHours(2),
            signingCredentials: credentials);

        return new JwtSecurityTokenHandler().WriteToken(token);
    }

    private record UserRecord(string Username, string Password, string Role);
}
