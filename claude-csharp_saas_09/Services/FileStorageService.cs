using Microsoft.EntityFrameworkCore;
using TeamTrackr.Data;
using TeamTrackr.Models;

namespace TeamTrackr.Services;

public class FileStorageService : IFileStorageService
{
    private readonly AppDbContext _db;
    private readonly IBillingService _billingService;
    private readonly string _uploadRoot;
    private const long MaxFileSizeBytes = 10 * 1024 * 1024; // 10 MB

    public FileStorageService(AppDbContext db, IBillingService billingService, IWebHostEnvironment env)
    {
        _db = db;
        _billingService = billingService;
        _uploadRoot = Path.Combine(env.ContentRootPath, "uploads");
        Directory.CreateDirectory(_uploadRoot);
    }

    public async Task<FileAttachment> UploadAsync(int tenantId, int taskId, string fileName, string contentType, Stream stream, string userId)
    {
        // Validate file size
        if (stream.Length > MaxFileSizeBytes)
        {
            throw new InvalidOperationException($"File size exceeds maximum of {MaxFileSizeBytes / (1024 * 1024)} MB.");
        }

        // Check storage quota
        var subscription = await _billingService.GetSubscriptionAsync(tenantId);
        var limits = _billingService.GetPlanLimits(subscription?.Plan ?? SubscriptionPlan.Free);
        var currentUsage = await GetStorageUsageAsync(tenantId);
        var maxStorageBytes = (long)limits.MaxFileStorageMB * 1024 * 1024;

        if (currentUsage + stream.Length > maxStorageBytes)
        {
            throw new InvalidOperationException(
                $"Storage quota exceeded. Used: {currentUsage / (1024 * 1024)} MB, " +
                $"Limit: {limits.MaxFileStorageMB} MB. Upgrade your plan for more storage.");
        }

        // Create tenant-specific directory
        var tenantDir = Path.Combine(_uploadRoot, tenantId.ToString());
        Directory.CreateDirectory(tenantDir);

        // Generate unique file path
        var storedFileName = $"{Guid.NewGuid():N}_{fileName}";
        var storagePath = Path.Combine(tenantDir, storedFileName);

        // Save file to disk
        using (var fileStream = new FileStream(storagePath, FileMode.Create))
        {
            await stream.CopyToAsync(fileStream);
        }

        var attachment = new FileAttachment
        {
            TenantId = tenantId,
            TaskItemId = taskId,
            FileName = fileName,
            ContentType = contentType,
            FileSizeBytes = stream.Length,
            StoragePath = storagePath,
            UploadedByUserId = userId,
            UploadedAt = DateTime.UtcNow
        };

        _db.FileAttachments.Add(attachment);
        await _db.SaveChangesAsync();

        return attachment;
    }

    public async Task<(Stream Stream, string ContentType, string FileName)?> DownloadAsync(int attachmentId)
    {
        var attachment = await _db.FileAttachments.FindAsync(attachmentId);
        if (attachment == null) return null;

        if (!File.Exists(attachment.StoragePath))
            return null;

        var stream = new FileStream(attachment.StoragePath, FileMode.Open, FileAccess.Read);
        return (stream, attachment.ContentType, attachment.FileName);
    }

    public async Task<bool> DeleteAsync(int attachmentId)
    {
        var attachment = await _db.FileAttachments.FindAsync(attachmentId);
        if (attachment == null) return false;

        // Delete physical file
        if (File.Exists(attachment.StoragePath))
        {
            File.Delete(attachment.StoragePath);
        }

        _db.FileAttachments.Remove(attachment);
        await _db.SaveChangesAsync();
        return true;
    }

    public async Task<long> GetStorageUsageAsync(int tenantId)
    {
        return await _db.FileAttachments
            .Where(f => f.TenantId == tenantId)
            .SumAsync(f => f.FileSizeBytes);
    }
}
