using System.Net;
using System.Net.Http.Json;
using TeamTrackr.DTOs;
using Xunit;

namespace TeamTrackr.Tests;

public class ProjectTests : IClassFixture<TeamTrackrWebApplicationFactory>
{
    private readonly TeamTrackrWebApplicationFactory _factory;

    public ProjectTests(TeamTrackrWebApplicationFactory factory)
    {
        _factory = factory;
    }

    private CreateProjectRequest MakeProject(string? suffix = null)
    {
        var id = suffix ?? Guid.NewGuid().ToString("N")[..8];
        return new CreateProjectRequest
        {
            Name = $"Project {id}",
            Description = "A test project",
            Key = $"P{id}".ToUpper()[..6]
        };
    }

    [Fact]
    public async Task CreateProject_Succeeds()
    {
        var client = _factory.CreateAuthenticatedClient();
        var request = MakeProject();

        var response = await client.PostAsJsonAsync("/api/projects", request);

        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
        var project = await response.Content.ReadFromJsonAsync<ProjectResponse>();
        Assert.NotNull(project);
        Assert.Equal(request.Name, project!.Name);
        Assert.Equal(request.Key, project.Key);
    }

    [Fact]
    public async Task GetAllProjects_ReturnsOnlyTenantProjects()
    {
        var clientA = _factory.CreateAuthenticatedClient();
        var clientB = _factory.CreateTenantBClient();

        // Create project in Tenant A
        var reqA = MakeProject("tenA1");
        await clientA.PostAsJsonAsync("/api/projects", reqA);

        // Create project in Tenant B
        var reqB = MakeProject("tenB1");
        await clientB.PostAsJsonAsync("/api/projects", reqB);

        // Tenant A should not see Tenant B's project
        var response = await clientA.GetAsync("/api/projects");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var projects = await response.Content.ReadFromJsonAsync<List<ProjectResponse>>();
        Assert.NotNull(projects);
        Assert.DoesNotContain(projects!, p => p.Name == reqB.Name);
    }

    [Fact]
    public async Task UpdateProject_Succeeds()
    {
        var client = _factory.CreateAuthenticatedClient();
        var createReq = MakeProject();
        var createResp = await client.PostAsJsonAsync("/api/projects", createReq);
        var created = await createResp.Content.ReadFromJsonAsync<ProjectResponse>();

        var updateReq = new UpdateProjectRequest { Name = "Updated Name" };
        var response = await client.PutAsJsonAsync($"/api/projects/{created!.Id}", updateReq);

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var updated = await response.Content.ReadFromJsonAsync<ProjectResponse>();
        Assert.Equal("Updated Name", updated!.Name);
    }

    [Fact]
    public async Task DeleteProject_Succeeds()
    {
        var client = _factory.CreateAuthenticatedClient();
        var createReq = MakeProject();
        var createResp = await client.PostAsJsonAsync("/api/projects", createReq);
        var created = await createResp.Content.ReadFromJsonAsync<ProjectResponse>();

        var response = await client.DeleteAsync($"/api/projects/{created!.Id}");
        Assert.Equal(HttpStatusCode.NoContent, response.StatusCode);

        // Verify it's gone
        var getResponse = await client.GetAsync($"/api/projects/{created.Id}");
        Assert.Equal(HttpStatusCode.NotFound, getResponse.StatusCode);
    }

    [Fact]
    public async Task UnauthorizedRequest_Returns401()
    {
        var client = _factory.CreateClient(); // No auth header
        var response = await client.GetAsync("/api/projects");
        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }
}
