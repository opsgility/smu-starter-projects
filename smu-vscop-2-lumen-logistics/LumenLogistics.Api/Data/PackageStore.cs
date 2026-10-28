using System.Collections.Concurrent;
using LumenLogistics.Api.Models;

namespace LumenLogistics.Api.Data;

public class PackageStore
{
    private readonly ConcurrentDictionary<string, Package> _packages = new();

    public PackageStore()
    {
        Seed();
    }

    public IReadOnlyCollection<Package> All() => _packages.Values.ToList();

    public Package? Get(string id) =>
        _packages.TryGetValue(id, out var p) ? p : null;

    public Package Add(Package pkg)
    {
        var withId = string.IsNullOrWhiteSpace(pkg.Id)
            ? pkg with { Id = Guid.NewGuid().ToString("N")[..8] }
            : pkg;
        _packages[withId.Id] = withId;
        return withId;
    }

    private void Seed()
    {
        Add(new Package("LMN0001", "Michael Peters",   "Seattle, WA", "InTransit"));
        Add(new Package("LMN0002", "Alex Rivera",      "Austin, TX",  "Delivered"));
        Add(new Package("LMN0003", "Jordan Nakamura",  "Boston, MA",  "Pending"));
    }
}
