using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using TeamTrackr.Auth;
using TeamTrackr.Data;
using TeamTrackr.DTOs;
using TeamTrackr.Models;

namespace TeamTrackr.Services;

public class AuthService : IAuthService
{
    private readonly UserManager<AppUser> _userManager;
    private readonly AppDbContext _db;
    private readonly IJwtTokenService _jwtTokenService;

    // In-memory refresh token store (production would use DB or Redis)
    private static readonly Dictionary<string, (string UserId, string RefreshToken)> _refreshTokens = new();

    public AuthService(
        UserManager<AppUser> userManager,
        AppDbContext db,
        IJwtTokenService jwtTokenService)
    {
        _userManager = userManager;
        _db = db;
        _jwtTokenService = jwtTokenService;
    }

    public async Task<AuthResponse> RegisterAsync(RegisterRequest request)
    {
        // Check if tenant slug already exists
        var existingTenant = await _db.Tenants
            .IgnoreQueryFilters()
            .FirstOrDefaultAsync(t => t.Slug == request.TenantSlug);

        Tenant tenant;
        if (existingTenant != null)
        {
            tenant = existingTenant;
        }
        else
        {
            tenant = new Tenant
            {
                Name = request.TenantName,
                Slug = request.TenantSlug,
                Plan = "free"
            };
            _db.Tenants.Add(tenant);
            await _db.SaveChangesAsync();
        }

        var user = new AppUser
        {
            UserName = request.Email,
            Email = request.Email,
            DisplayName = request.DisplayName,
            TenantId = tenant.Id,
            Role = existingTenant == null ? UserRole.Owner : UserRole.Member
        };

        var result = await _userManager.CreateAsync(user, request.Password);
        if (!result.Succeeded)
        {
            var errors = string.Join(", ", result.Errors.Select(e => e.Description));
            throw new InvalidOperationException($"Registration failed: {errors}");
        }

        await _userManager.AddToRoleAsync(user, user.Role.ToString());

        var token = _jwtTokenService.GenerateAccessToken(user);
        var refreshToken = _jwtTokenService.GenerateRefreshToken();
        _refreshTokens[user.Id] = (user.Id, refreshToken);

        return new AuthResponse
        {
            Token = token,
            RefreshToken = refreshToken,
            UserId = user.Id,
            Email = user.Email!,
            DisplayName = user.DisplayName,
            Role = user.Role.ToString(),
            TenantId = tenant.Id,
            TenantName = tenant.Name
        };
    }

    public async Task<AuthResponse> LoginAsync(LoginRequest request)
    {
        var user = await _userManager.FindByEmailAsync(request.Email);
        if (user == null)
            throw new UnauthorizedAccessException("Invalid credentials.");

        var validPassword = await _userManager.CheckPasswordAsync(user, request.Password);
        if (!validPassword)
            throw new UnauthorizedAccessException("Invalid credentials.");

        var tenant = await _db.Tenants
            .IgnoreQueryFilters()
            .FirstAsync(t => t.Id == user.TenantId);

        var token = _jwtTokenService.GenerateAccessToken(user);
        var refreshToken = _jwtTokenService.GenerateRefreshToken();
        _refreshTokens[user.Id] = (user.Id, refreshToken);

        return new AuthResponse
        {
            Token = token,
            RefreshToken = refreshToken,
            UserId = user.Id,
            Email = user.Email!,
            DisplayName = user.DisplayName,
            Role = user.Role.ToString(),
            TenantId = tenant.Id,
            TenantName = tenant.Name
        };
    }

    public async Task<AuthResponse> RefreshTokenAsync(RefreshRequest request)
    {
        var principal = _jwtTokenService.ValidateExpiredToken(request.Token);
        if (principal == null)
            throw new UnauthorizedAccessException("Invalid token.");

        var userId = principal.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value
            ?? principal.FindFirst("sub")?.Value;

        if (userId == null)
            throw new UnauthorizedAccessException("Invalid token claims.");

        if (!_refreshTokens.TryGetValue(userId, out var stored) ||
            stored.RefreshToken != request.RefreshToken)
        {
            throw new UnauthorizedAccessException("Invalid refresh token.");
        }

        var user = await _userManager.FindByIdAsync(userId);
        if (user == null)
            throw new UnauthorizedAccessException("User not found.");

        var tenant = await _db.Tenants
            .IgnoreQueryFilters()
            .FirstAsync(t => t.Id == user.TenantId);

        var newToken = _jwtTokenService.GenerateAccessToken(user);
        var newRefreshToken = _jwtTokenService.GenerateRefreshToken();
        _refreshTokens[user.Id] = (user.Id, newRefreshToken);

        return new AuthResponse
        {
            Token = newToken,
            RefreshToken = newRefreshToken,
            UserId = user.Id,
            Email = user.Email!,
            DisplayName = user.DisplayName,
            Role = user.Role.ToString(),
            TenantId = tenant.Id,
            TenantName = tenant.Name
        };
    }
}
