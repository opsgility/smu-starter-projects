using TeamTrackr.Models;

namespace TeamTrackr.Services;

public interface IFileStorageService
{
    Task<FileAttachment> UploadAsync(int tenantId, int taskId, string fileName, string contentType, Stream stream, string userId);
    Task<(Stream Stream, string ContentType, string FileName)?> DownloadAsync(int attachmentId);
    Task<bool> DeleteAsync(int attachmentId);
    Task<long> GetStorageUsageAsync(int tenantId);
}
