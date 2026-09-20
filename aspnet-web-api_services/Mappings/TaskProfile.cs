using AutoMapper;
using TaskFlow.Api.DTOs;
using TaskFlow.Api.Models;

namespace TaskFlow.Api.Mappings;

public class TaskProfile : Profile
{
    public TaskProfile()
    {
        CreateMap<CreateTaskDto, TaskItem>();

        CreateMap<UpdateTaskDto, TaskItem>()
            .ForAllMembers(opts => opts.Condition((src, dest, srcMember) => srcMember != null));

        CreateMap<TaskItem, TaskResponseDto>()
            .ForMember(dest => dest.IsOverdue, opt => opt.MapFrom(src =>
                !src.IsComplete && src.DueDate.HasValue && src.DueDate.Value < DateTime.UtcNow))
            .ForMember(dest => dest.CategoryName, opt => opt.MapFrom(src =>
                src.Category != null ? src.Category.Name : null));
    }
}
