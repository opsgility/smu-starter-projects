using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Processing;

namespace Anchorline.Functions.Thumbnails;

public class ThumbnailFunction
{
    private readonly ILogger<ThumbnailFunction> _log;

    public ThumbnailFunction(ILogger<ThumbnailFunction> log) => _log = log;

    [Function("Thumbnail")]
    [BlobOutput("product-thumbnails/{name}.jpg", Connection = "AnchorlineStorage")]
    public byte[] Run(
        [BlobTrigger("product-uploads/{name}", Connection = "AnchorlineStorage")] byte[] originalImage,
        string name)
    {
        _log.LogInformation("Thumbnail {Name}: input size {Size} bytes", name, originalImage.Length);

        using var image = Image.Load(originalImage);
        image.Mutate(x => x.Resize(new ResizeOptions
        {
            Size = new Size(300, 300),
            Mode = ResizeMode.Max
        }));

        using var ms = new MemoryStream();
        image.SaveAsJpeg(ms);
        var output = ms.ToArray();
        _log.LogInformation("Thumbnail {Name}: output size {Size} bytes", name, output.Length);
        return output;
    }
}
