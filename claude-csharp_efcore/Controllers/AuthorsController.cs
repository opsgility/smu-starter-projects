using Microsoft.AspNetCore.Mvc;
using Project.Models;
using Project.Repositories;

namespace Project.Controllers;

[ApiController]
[Route("api/[controller]")]
public class AuthorsController : ControllerBase
{
    private readonly IAuthorRepository _authorRepository;

    public AuthorsController(IAuthorRepository authorRepository)
    {
        _authorRepository = authorRepository;
    }

    [HttpGet]
    public ActionResult<List<Author>> GetAll()
    {
        return Ok(_authorRepository.GetAll());
    }

    [HttpGet("{id}")]
    public ActionResult<Author> GetById(int id)
    {
        var author = _authorRepository.GetById(id);
        if (author == null) return NotFound();
        return Ok(author);
    }

    [HttpPost]
    public ActionResult<Author> Create([FromBody] Author author)
    {
        var created = _authorRepository.Create(author);
        return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
    }

    [HttpPut("{id}")]
    public ActionResult<Author> Update(int id, [FromBody] Author author)
    {
        var updated = _authorRepository.Update(id, author);
        if (updated == null) return NotFound();
        return Ok(updated);
    }

    [HttpDelete("{id}")]
    public IActionResult Delete(int id)
    {
        var deleted = _authorRepository.Delete(id);
        if (!deleted) return NotFound();
        return NoContent();
    }
}
