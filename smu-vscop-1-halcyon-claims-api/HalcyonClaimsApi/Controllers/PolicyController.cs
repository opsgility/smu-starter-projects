using HalcyonClaimsApi.Models;
using Microsoft.AspNetCore.Mvc;

namespace HalcyonClaimsApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class PolicyController : ControllerBase
{
    private static readonly List<Policy> _policies = new()
    {
        new Policy { Id = 1, PolicyNumber = "POL-0000001", Holder = "Jordan Avery",   CoverageAmount = 150000m, EffectiveDate = DateTime.UtcNow.AddMonths(-10), ExpirationDate = DateTime.UtcNow.AddMonths(2),  IsActive = true  },
        new Policy { Id = 2, PolicyNumber = "POL-0000002", Holder = "Avery Blake",    CoverageAmount =  50000m, EffectiveDate = DateTime.UtcNow.AddMonths(-6),  ExpirationDate = DateTime.UtcNow.AddMonths(6),  IsActive = true  },
        new Policy { Id = 3, PolicyNumber = "POL-0000003", Holder = "Riley Chen",     CoverageAmount = 250000m, EffectiveDate = DateTime.UtcNow.AddMonths(-24), ExpirationDate = DateTime.UtcNow.AddMonths(-1), IsActive = false }
    };

    [HttpGet]
    public IActionResult GetAll() => Ok(_policies);

    [HttpGet("{id:int}")]
    public IActionResult GetById(int id)
    {
        var policy = _policies.FirstOrDefault(p => p.Id == id);
        return policy is null ? NotFound() : Ok(policy);
    }

    [HttpPost]
    public IActionResult Create([FromBody] Policy policy)
    {
        if (!IsValidPolicyNumber(policy.PolicyNumber))
        {
            return BadRequest("Invalid policy number format. Expected POL- followed by 7 digits.");
        }

        policy.Id = _policies.Count == 0 ? 1 : _policies.Max(p => p.Id) + 1;
        _policies.Add(policy);
        return CreatedAtAction(nameof(GetById), new { id = policy.Id }, policy);
    }

    internal static Policy? FindPolicy(string policyNumber) =>
        _policies.FirstOrDefault(p => p.PolicyNumber == policyNumber);

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
}
