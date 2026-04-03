using System.Net;
using System.Net.Http.Json;
using TeamTrackr.DTOs;
using TeamTrackr.Models;
using Xunit;

namespace TeamTrackr.Tests;

public class TaskTests : IClassFixture<TeamTrackrWebApplicationFactory>
{
    private readonly TeamTrackrWebApplicationFactory _factory;

    public TaskTests(TeamTrackrWebApplicationFactory factory)
    {
        _factory = factory;
    }

    private async Task<ProjectResponse> CreateTestProject(HttpClient client)
    {
        var key = Guid.NewGuid().ToString("N")[..6].ToUpper();
        var req = new CreateProjectRequest
        {
            Name = $"TaskTestProject {key}",
            Description = "For task tests",
            Key = key
        };
        var resp = await client.PostAsJsonAsync("/api/projects", req);
        resp.EnsureSuccessStatusCode();
        return (await resp.Content.ReadFromJsonAsync<ProjectResponse>())!;
    }

    [Fact]
    public async Task CreateTask_InProject_Succeeds()
    {
        var client = _factory.CreateAuthenticatedClient();
        var project = await CreateTestProject(client);

        var request = new CreateTaskRequest
        {
            ProjectId = project.Id,
            Title = "Test Task",
            Description = "A test task",
            Status = TaskItemStatus.Todo,
            Priority = TaskPriority.Medium
        };

        var response = await client.PostAsJsonAsync("/api/tasks", request);

        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
        var task = await response.Content.ReadFromJsonAsync<TaskResponse>();
        Assert.NotNull(task);
        Assert.Equal("Test Task", task!.Title);
        Assert.Equal(project.Id, task.ProjectId);
    }

    [Fact]
    public async Task GetTasks_FilterByStatus_Works()
    {
        var client = _factory.CreateAuthenticatedClient();
        var project = await CreateTestProject(client);

        // Create a Todo task
        await client.PostAsJsonAsync("/api/tasks", new CreateTaskRequest
        {
            ProjectId = project.Id,
            Title = "Todo Task",
            Status = TaskItemStatus.Todo
        });

        // Create an InProgress task
        await client.PostAsJsonAsync("/api/tasks", new CreateTaskRequest
        {
            ProjectId = project.Id,
            Title = "InProgress Task",
            Status = TaskItemStatus.InProgress
        });

        // Filter by Todo
        var response = await client.GetAsync($"/api/tasks?status={TaskItemStatus.Todo}&projectId={project.Id}");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var tasks = await response.Content.ReadFromJsonAsync<List<TaskResponse>>();
        Assert.NotNull(tasks);
        Assert.All(tasks!, t => Assert.Equal(TaskItemStatus.Todo, t.Status));
    }

    [Fact]
    public async Task UpdateTaskStatus_Succeeds()
    {
        var client = _factory.CreateAuthenticatedClient();
        var project = await CreateTestProject(client);

        var createResp = await client.PostAsJsonAsync("/api/tasks", new CreateTaskRequest
        {
            ProjectId = project.Id,
            Title = "Status Task",
            Status = TaskItemStatus.Todo
        });
        var created = await createResp.Content.ReadFromJsonAsync<TaskResponse>();

        var updateReq = new UpdateTaskRequest { Status = TaskItemStatus.InProgress };
        var response = await client.PutAsJsonAsync($"/api/tasks/{created!.Id}", updateReq);

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var updated = await response.Content.ReadFromJsonAsync<TaskResponse>();
        Assert.Equal(TaskItemStatus.InProgress, updated!.Status);
    }

    [Fact]
    public async Task AssignTask_ToUser_Succeeds()
    {
        var client = _factory.CreateAuthenticatedClient();
        var project = await CreateTestProject(client);

        var createResp = await client.PostAsJsonAsync("/api/tasks", new CreateTaskRequest
        {
            ProjectId = project.Id,
            Title = "Assign Task"
        });
        var created = await createResp.Content.ReadFromJsonAsync<TaskResponse>();

        var updateReq = new UpdateTaskRequest { AssigneeId = _factory.TestUserId };
        var response = await client.PutAsJsonAsync($"/api/tasks/{created!.Id}", updateReq);

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var updated = await response.Content.ReadFromJsonAsync<TaskResponse>();
        Assert.Equal(_factory.TestUserId, updated!.AssigneeId);
    }

    [Fact]
    public async Task DeleteTask_Succeeds()
    {
        var client = _factory.CreateAuthenticatedClient();
        var project = await CreateTestProject(client);

        var createResp = await client.PostAsJsonAsync("/api/tasks", new CreateTaskRequest
        {
            ProjectId = project.Id,
            Title = "Delete Me"
        });
        var created = await createResp.Content.ReadFromJsonAsync<TaskResponse>();

        var response = await client.DeleteAsync($"/api/tasks/{created!.Id}");
        Assert.Equal(HttpStatusCode.NoContent, response.StatusCode);

        // Verify it's gone
        var getResponse = await client.GetAsync($"/api/tasks/{created.Id}");
        Assert.Equal(HttpStatusCode.NotFound, getResponse.StatusCode);
    }
}
