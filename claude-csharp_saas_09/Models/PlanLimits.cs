namespace TeamTrackr.Models;

public class PlanLimits
{
    public int MaxProjects { get; set; }
    public int MaxTasksPerProject { get; set; }
    public int MaxFileStorageMB { get; set; }
    public int MaxTeamMembers { get; set; }
    public bool HasApiAccess { get; set; }
    public bool HasAdvancedSearch { get; set; }

    public static PlanLimits Free() => new()
    {
        MaxProjects = 3,
        MaxTasksPerProject = 25,
        MaxFileStorageMB = 100,
        MaxTeamMembers = 5,
        HasApiAccess = false,
        HasAdvancedSearch = false
    };

    public static PlanLimits Pro() => new()
    {
        MaxProjects = 20,
        MaxTasksPerProject = 200,
        MaxFileStorageMB = 2048,
        MaxTeamMembers = 25,
        HasApiAccess = true,
        HasAdvancedSearch = true
    };

    public static PlanLimits Enterprise() => new()
    {
        MaxProjects = int.MaxValue,
        MaxTasksPerProject = int.MaxValue,
        MaxFileStorageMB = 51200,
        MaxTeamMembers = int.MaxValue,
        HasApiAccess = true,
        HasAdvancedSearch = true
    };
}
