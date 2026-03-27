using TaskFlow.Api.DTOs;

namespace TaskFlow.Api.Services;

public interface IAuthService
{
    Task<LoginResponseDto?> AuthenticateAsync(LoginDto dto);
}
