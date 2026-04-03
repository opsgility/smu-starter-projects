using System.Net;
using System.Net.Http.Json;
using TeamTrackr.DTOs;
using Xunit;

namespace TeamTrackr.Tests;

public class AuthTests : IClassFixture<TeamTrackrWebApplicationFactory>
{
    private readonly TeamTrackrWebApplicationFactory _factory;
    private readonly HttpClient _client;

    public AuthTests(TeamTrackrWebApplicationFactory factory)
    {
        _factory = factory;
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task Register_NewUser_ReturnsSuccess()
    {
        var request = new RegisterRequest
        {
            Email = $"newuser_{Guid.NewGuid():N}@test.com",
            Password = "TestPass1234",
            DisplayName = "New User",
            TenantName = "New Org",
            TenantSlug = $"neworg-{Guid.NewGuid():N}"
        };

        var response = await _client.PostAsJsonAsync("/api/auth/register", request);

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var auth = await response.Content.ReadFromJsonAsync<AuthResponse>();
        Assert.NotNull(auth);
        Assert.False(string.IsNullOrEmpty(auth!.Token));
        Assert.False(string.IsNullOrEmpty(auth.RefreshToken));
        Assert.Equal(request.Email, auth.Email);
    }

    [Fact]
    public async Task Register_DuplicateEmail_ReturnsBadRequest()
    {
        var email = $"dup_{Guid.NewGuid():N}@test.com";
        var slug1 = $"org1-{Guid.NewGuid():N}";
        var slug2 = $"org2-{Guid.NewGuid():N}";

        var request1 = new RegisterRequest
        {
            Email = email,
            Password = "TestPass1234",
            DisplayName = "User One",
            TenantName = "Org One",
            TenantSlug = slug1
        };

        var response1 = await _client.PostAsJsonAsync("/api/auth/register", request1);
        Assert.Equal(HttpStatusCode.OK, response1.StatusCode);

        var request2 = new RegisterRequest
        {
            Email = email,
            Password = "TestPass1234",
            DisplayName = "User Two",
            TenantName = "Org Two",
            TenantSlug = slug2
        };

        var response2 = await _client.PostAsJsonAsync("/api/auth/register", request2);
        Assert.Equal(HttpStatusCode.BadRequest, response2.StatusCode);
    }

    [Fact]
    public async Task Login_ValidCredentials_ReturnsJwt()
    {
        // Register a user first
        var email = $"login_{Guid.NewGuid():N}@test.com";
        var password = "TestPass1234";
        var registerRequest = new RegisterRequest
        {
            Email = email,
            Password = password,
            DisplayName = "Login User",
            TenantName = "Login Org",
            TenantSlug = $"loginorg-{Guid.NewGuid():N}"
        };
        var regResponse = await _client.PostAsJsonAsync("/api/auth/register", registerRequest);
        Assert.Equal(HttpStatusCode.OK, regResponse.StatusCode);

        // Now login
        var loginRequest = new LoginRequest { Email = email, Password = password };
        var response = await _client.PostAsJsonAsync("/api/auth/login", loginRequest);

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var auth = await response.Content.ReadFromJsonAsync<AuthResponse>();
        Assert.NotNull(auth);
        Assert.False(string.IsNullOrEmpty(auth!.Token));
        Assert.Equal(email, auth.Email);
    }

    [Fact]
    public async Task Login_InvalidPassword_ReturnsUnauthorized()
    {
        // Register a user first
        var email = $"badpw_{Guid.NewGuid():N}@test.com";
        var registerRequest = new RegisterRequest
        {
            Email = email,
            Password = "TestPass1234",
            DisplayName = "Bad PW User",
            TenantName = "Bad PW Org",
            TenantSlug = $"badpworg-{Guid.NewGuid():N}"
        };
        await _client.PostAsJsonAsync("/api/auth/register", registerRequest);

        var loginRequest = new LoginRequest { Email = email, Password = "WrongPassword1" };
        var response = await _client.PostAsJsonAsync("/api/auth/login", loginRequest);

        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }

    [Fact]
    public async Task Refresh_ValidToken_ReturnsNewJwt()
    {
        // Register to get initial tokens
        var email = $"refresh_{Guid.NewGuid():N}@test.com";
        var registerRequest = new RegisterRequest
        {
            Email = email,
            Password = "TestPass1234",
            DisplayName = "Refresh User",
            TenantName = "Refresh Org",
            TenantSlug = $"refreshorg-{Guid.NewGuid():N}"
        };
        var regResponse = await _client.PostAsJsonAsync("/api/auth/register", registerRequest);
        var auth = await regResponse.Content.ReadFromJsonAsync<AuthResponse>();
        Assert.NotNull(auth);

        // Refresh
        var refreshRequest = new RefreshRequest
        {
            Token = auth!.Token,
            RefreshToken = auth.RefreshToken
        };
        var response = await _client.PostAsJsonAsync("/api/auth/refresh", refreshRequest);

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var newAuth = await response.Content.ReadFromJsonAsync<AuthResponse>();
        Assert.NotNull(newAuth);
        Assert.False(string.IsNullOrEmpty(newAuth!.Token));
        Assert.NotEqual(auth.Token, newAuth.Token);
    }
}
