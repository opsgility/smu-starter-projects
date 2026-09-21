using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Processing;

namespace Anchorline.Functions.Thumbnails;

public class ThumbnailFunction
{
    private readonly ILogger<ThumbnailFunction> _log;

    public ThumbnailFunction(ILogger<ThumbnailFunction> log) => _log = log;

    // On Flex Consumption, blob triggers are Event Grid-driven. Bindings use
    // the default AzureWebJobsStorage connection, which the ARM template
    // provisions as AzureWebJobsStorage__accountName (identity-based access —
    // the Function App's system-assigned MI holds Storage Blob Data Owner on
    // the account, so no connection string is required or possible).
    [Function("GenerateThumbnail")]
    [BlobOutput("product-thumbnails/{name}.jpg")]
    public byte[] Run(
        [BlobTrigger("product-uploads/{name}")] byte[] originalImage,
        string name)
    {
        _log.LogInformation("GenerateThumbnail {Name}: input size {Size} bytes", name, originalImage.Length);

        using var image = Image.Load(originalImage);
        image.Mutate(x => x.Resize(new ResizeOptions
        {
            Size = new Size(300, 300),
            Mode = ResizeMode.Max
        }));

        using var ms = new MemoryStream();
        image.SaveAsJpeg(ms);
        var output = ms.ToArray();
        _log.LogInformation("GenerateThumbnail {Name}: output size {Size} bytes", name, output.Length);
        return output;
    }
}
