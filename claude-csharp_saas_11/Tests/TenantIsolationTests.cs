using System.Net;
using System.Net.Http.Json;
using Microsoft.Extensions.DependencyInjection;
using TeamTrackr.Data;
using TeamTrackr.DTOs;
using TeamTrackr.Models;
using Xunit;

namespace TeamTrackr.Tests;

public class TenantIsolationTests : IClassFixture<TeamTrackrWebApplicationFactory>
{
    private readonly TeamTrackrWebApplicationFactory _factory;

    public TenantIsolationTests(TeamTrackrWebApplicationFactory factory)
    {
        _factory = factory;
    }

    private async Task<ProjectResponse> CreateProject(HttpClient client, string suffix)
    {
        var key = suffix.ToUpper()[..Math.Min(6, suffix.Length)];
        var req = new CreateProjectRequest
        {
            Name = $"Iso Project {suffix}",
            Description = "Isolation test project",
            Key = key
        };
        var resp = await client.PostAsJsonAsync("/api/projects", req);
        resp.EnsureSuccessStatusCode();
        return (await resp.Content.ReadFromJsonAsync<ProjectResponse>())!;
    }

    private async Task<TaskResponse> CreateTask(HttpClient client, int projectId, string title)
    {
        var req = new CreateTaskRequest
        {
            ProjectId = projectId,
            Title = title,
            Status = TaskItemStatus.Todo
        };
        var resp = await client.PostAsJsonAsync("/api/tasks", req);
        resp.EnsureSuccessStatusCode();
        return (await resp.Content.ReadFromJsonAsync<TaskResponse>())!;
    }

    [Fact]
    public async Task TenantA_CannotSee_TenantB_Projects()
    {
        var clientA = _factory.CreateAuthenticatedClient();
        var clientB = _factory.CreateTenantBClient();

        var suffix = Guid.NewGuid().ToString("N")[..6];
        var projectB = await CreateProject(clientB, $"isB{suffix}");

        // Tenant A tries to list projects - should not see Tenant B's project
        var response = await clientA.GetAsync("/api/projects");
        var projects = await response.Content.ReadFromJsonAsync<List<ProjectResponse>>();
        Assert.DoesNotContain(projects!, p => p.Id == projectB.Id);
    }

    [Fact]
    public async Task TenantA_CannotSee_TenantB_Tasks()
    {
        var clientA = _factory.CreateAuthenticatedClient();
        var clientB = _factory.CreateTenantBClient();

        var suffix = Guid.NewGuid().ToString("N")[..6];
        var projectB = await CreateProject(clientB, $"tB{suffix}");
        var taskB = await CreateTask(clientB, projectB.Id, "Secret Task B");

        // Tenant A tries to get the task directly
        var response = await clientA.GetAsync($"/api/tasks/{taskB.Id}");
        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
    }

    [Fact]
    public async Task TenantA_CannotModify_TenantB_Projects()
    {
        var clientA = _factory.CreateAuthenticatedClient();
        var clientB = _factory.CreateTenantBClient();

        var suffix = Guid.NewGuid().ToString("N")[..6];
        var projectB = await CreateProject(clientB, $"mB{suffix}");

        // Tenant A tries to update Tenant B's project
        var updateReq = new UpdateProjectRequest { Name = "Hacked Name" };
        var response = await clientA.PutAsJsonAsync($"/api/projects/{projectB.Id}", updateReq);
        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
    }

    [Fact]
    public async Task CreatingResources_AutoAssigns_CorrectTenantId()
    {
        var clientA = _factory.CreateAuthenticatedClient();

        var suffix = Guid.NewGuid().ToString("N")[..6];
        var project = await CreateProject(clientA, $"au{suffix}");
        var task = await CreateTask(clientA, project.Id, "Auto-tenant Task");

        // Verify through the API that the task belongs to the right project
        // and is visible to Tenant A (which means it has the right TenantId)
        var response = await clientA.GetAsync($"/api/tasks/{task.Id}");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var fetched = await response.Content.ReadFromJsonAsync<TaskResponse>();
        Assert.Equal(project.Id, fetched!.ProjectId);

        // Verify Tenant B cannot see it
        var clientB = _factory.CreateTenantBClient();
        var responseB = await clientB.GetAsync($"/api/tasks/{task.Id}");
        Assert.Equal(HttpStatusCode.NotFound, responseB.StatusCode);
    }

    [Fact]
    public async Task ApiKey_FromTenantA_CannotAccess_TenantB_Data()
    {
        var clientA = _factory.CreateAuthenticatedClient();
        var clientB = _factory.CreateTenantBClient();

        var suffix = Guid.NewGuid().ToString("N")[..6];

        // Create a project in Tenant B
        var projectB = await CreateProject(clientB, $"aB{suffix}");

        // Create an API key for Tenant A
        var apiKeyResp = await clientA.PostAsJsonAsync("/api/apikeys", new { Name = "TestKey" });
        apiKeyResp.EnsureSuccessStatusCode();
        var apiKeyJson = await apiKeyResp.Content.ReadFromJsonAsync<ApiKeyCreatedDto>();

        // Use the API key to try to access Tenant B's project
        var apiClient = _factory.CreateClient();
        apiClient.DefaultRequestHeaders.Add("X-API-Key", apiKeyJson!.Key);

        var response = await apiClient.GetAsync($"/api/projects/{projectB.Id}");
        // Should be NotFound because API key resolves to Tenant A, and query filter hides Tenant B data
        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
    }
}

// DTO for deserializing the API key creation response
internal class ApiKeyCreatedDto
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Key { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; }
}
