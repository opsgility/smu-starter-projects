using TeamTrackr.DTOs;

namespace TeamTrackr.Services;

public interface ISearchService
{
    Task<SearchResponse<TaskResponse>> SearchTasksAsync(SearchRequest request);
    Task<SearchResponse<ProjectResponse>> SearchProjectsAsync(string query, int page = 1, int pageSize = 20);
    Task<SearchResponse<GlobalSearchResult>> GlobalSearchAsync(string query, int page = 1, int pageSize = 20);
}
