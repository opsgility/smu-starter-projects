using System.Net;
using System.Text.Json;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Extensions.OpenApi.Core.Attributes;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.Extensions.Logging;
using Microsoft.OpenApi.Models;

namespace Anchorline.Functions.RestApi;

public class TodosApi
{
    private readonly ITodoRepository _repo;
    private readonly ILogger<TodosApi> _log;

    public TodosApi(ITodoRepository repo, ILogger<TodosApi> log)
    {
        _repo = repo;
        _log = log;
    }

    [Function("ListTodos")]
    [OpenApiOperation(operationId: "ListTodos", tags: new[] { "todos" }, Summary = "List all todos")]
    [OpenApiResponseWithBody(statusCode: HttpStatusCode.OK, contentType: "application/json", bodyType: typeof(Todo[]))]
    public IActionResult List(
        [HttpTrigger(AuthorizationLevel.Function, "get", Route = "todos")] HttpRequest req)
    {
        _log.LogInformation("ListTodos called");
        return new OkObjectResult(_repo.All());
    }

    [Function("GetTodo")]
    [OpenApiOperation(operationId: "GetTodo", tags: new[] { "todos" }, Summary = "Get a todo by ID")]
    [OpenApiParameter(name: "id", In = ParameterLocation.Path, Required = true, Type = typeof(int))]
    [OpenApiResponseWithBody(statusCode: HttpStatusCode.OK, contentType: "application/json", bodyType: typeof(Todo))]
    [OpenApiResponseWithoutBody(statusCode: HttpStatusCode.NotFound)]
    public IActionResult Get(
        [HttpTrigger(AuthorizationLevel.Function, "get", Route = "todos/{id:int}")] HttpRequest req,
        int id)
    {
        var todo = _repo.Find(id);
        return todo is null ? new NotFoundResult() : new OkObjectResult(todo);
    }

    // EXERCISE 2 will implement CreateTodo, UpdateTodo, DeleteTodo here.
}
