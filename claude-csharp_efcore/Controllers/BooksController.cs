using Microsoft.AspNetCore.Mvc;
using Project.DTOs;
using Project.Services;

namespace Project.Controllers;

[ApiController]
[Route("api/[controller]")]
public class BooksController : ControllerBase
{
    private readonly IBookService _bookService;

    public BooksController(IBookService bookService)
    {
        _bookService = bookService;
    }

    [HttpGet]
    public ActionResult<List<BookResponse>> GetAll()
    {
        return Ok(_bookService.GetAll());
    }

    [HttpGet("{id}")]
    public ActionResult<BookResponse> GetById(int id)
    {
        var book = _bookService.GetById(id);
        if (book == null) return NotFound();
        return Ok(book);
    }

    [HttpPost]
    public ActionResult<BookResponse> Create([FromBody] CreateBookRequest request)
    {
        var book = _bookService.Create(request);
        return CreatedAtAction(nameof(GetById), new { id = book.Id }, book);
    }

    [HttpPut("{id}")]
    public ActionResult<BookResponse> Update(int id, [FromBody] CreateBookRequest request)
    {
        var book = _bookService.Update(id, request);
        if (book == null) return NotFound();
        return Ok(book);
    }

    [HttpDelete("{id}")]
    public IActionResult Delete(int id)
    {
        var deleted = _bookService.Delete(id);
        if (!deleted) return NotFound();
        return NoContent();
    }

    [HttpGet("search")]
    public ActionResult<List<BookResponse>> Search([FromQuery] string title)
    {
        return Ok(_bookService.SearchByTitle(title));
    }
}
