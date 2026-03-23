namespace TeamTrackr.DTOs;

public class CreateLabelRequest
{
    public string Name { get; set; } = string.Empty;
    public string Color { get; set; } = "#000000";
}

public class LabelResponse
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Color { get; set; } = string.Empty;
}
