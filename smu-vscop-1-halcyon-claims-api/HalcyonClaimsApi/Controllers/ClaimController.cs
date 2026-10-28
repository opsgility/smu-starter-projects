using HalcyonClaimsApi.Models;
using HalcyonClaimsApi.Services;
using Microsoft.AspNetCore.Mvc;

namespace HalcyonClaimsApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ClaimController : ControllerBase
{
    private static readonly List<Claim> _claims = new()
    {
        new Claim { Id = 1, PolicyNumber = "POL-0000001", ClaimAmount = 850m,  IncidentDate = DateTime.UtcNow.AddDays(-14), Description = "Water damage to kitchen flooring.", Status = "Approved" },
        new Claim { Id = 2, PolicyNumber = "POL-0000002", ClaimAmount = 4200m, IncidentDate = DateTime.UtcNow.AddDays(-7),  Description = "Front bumper collision, parking lot.",  Status = "Review"   }
    };

    private readonly IClaimValidationService _validation;

    public ClaimController(IClaimValidationService validation)
    {
        _validation = validation;
    }

    [HttpGet]
    public IActionResult GetAll() => Ok(_claims);

    [HttpGet("{id:int}")]
    public IActionResult GetById(int id)
    {
        var claim = _claims.FirstOrDefault(c => c.Id == id);
        return claim is null ? NotFound() : Ok(claim);
    }

    [HttpPost]
    public async Task<IActionResult> Create([FromBody] Claim claim)
    {
        if (!IsValidPolicyNumber(claim.PolicyNumber))
        {
            return BadRequest("Invalid policy number format. Expected POL- followed by 7 digits.");
        }

        var policy = PolicyController.FindPolicy(claim.PolicyNumber);
        var (isValid, reason) = await _validation.ValidateClaimAsync(claim, policy);
        if (!isValid)
        {
            return BadRequest(reason);
        }

        claim.Id = _claims.Count == 0 ? 1 : _claims.Max(c => c.Id) + 1;
        _claims.Add(claim);
        return CreatedAtAction(nameof(GetById), new { id = claim.Id }, claim);
    }

    private static bool IsValidPolicyNumber(string policyNumber)
    {
        if (string.IsNullOrWhiteSpace(policyNumber))
        {
            return false;
        }

        if (policyNumber.Length != 11)
        {
            return false;
        }

        if (!policyNumber.StartsWith("POL-"))
        {
            return false;
        }

        for (int i = 4; i < policyNumber.Length; i++)
        {
            if (!char.IsDigit(policyNumber[i]))
            {
                return false;
            }
        }

        return true;
    }

    internal static IReadOnlyList<Claim> GetClaimsForPolicy(string policyNumber) =>
        _claims.Where(c => c.PolicyNumber == policyNumber).ToList();
}
