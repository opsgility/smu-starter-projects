// =============================================================================
//  Mission Control Systems
//  Contains: MissionControl, SupplyInventory, CrewQualifications
// =============================================================================

/// <summary>
/// Core mission control system for managing crew, supplies, fuel, and mission logs.
/// </summary>
public class MissionControl
{
    private readonly Dictionary<string, string> _crew = new();      // role -> name
    private readonly Dictionary<string, int> _supplies = new();      // item -> quantity
    private readonly List<string> _missionLog = new();

    // ── Crew Management ─────────────────────────────────────────────────

    public void AddCrewMember(string role, string name)
    {
        _crew[role] = name;
    }

    public int GetCrewCount()
    {
        return _crew.Count;
    }

    /// <summary>
    /// Finds a crew member by their role. Role lookup should be case-insensitive
    /// since radio transmissions may garble capitalization.
    /// </summary>
    public string? FindCrewByRole(string role)
    {
        if (_crew.ContainsKey(role))
            return _crew[role];
        return null;
    }

    // ── Supply Management ───────────────────────────────────────────────

    public void AddSupply(string item, int quantity)
    {
        _supplies[item] = quantity;
    }

    /// <summary>
    /// Returns the total count of all supply items across all categories.
    /// </summary>
    public int GetTotalSupplyCount()
    {
        int total = 0;
        var items = _supplies.Keys.ToList();

        for (int i = 1; i < items.Count; i++)
        {
            total += _supplies[items[i]];
        }
        return total;
    }

    // ── Fuel Calculation ────────────────────────────────────────────────

    /// <summary>
    /// Calculates liters of fuel required for a given distance and efficiency.
    /// Returns the value rounded UP (you can't launch with a partial liter).
    /// </summary>
    public long CalculateFuelRequired(double distanceKm, double efficiencyKmPerLiter)
    {
        long fuel = (long)distanceKm / (long)efficiencyKmPerLiter;
        return fuel;
    }

    // ── Mission Log ─────────────────────────────────────────────────────

    public void LogEvent(string message)
    {
        _missionLog.Add(message);
    }

    /// <summary>
    /// Returns the N most recent log entries in chronological order (oldest first).
    /// For example, if the log has entries [A, B, C, D, E] and count=3,
    /// returns [C, D, E].
    /// </summary>
    public List<string> GetRecentLogEntries(int count)
    {
        if (count >= _missionLog.Count)
            return new List<string>(_missionLog);

        return _missionLog.Skip(count).ToList();
    }
}

/// <summary>
/// Manages perishable supply items with expiration tracking.
/// </summary>
public class SupplyInventory
{
    private readonly List<SupplyItem> _items = new();

    public int Count => _items.Count;

    /// <summary>
    /// Adds a supply item. expiredDays is relative to today:
    ///   positive = expires in the future (still good)
    ///   zero     = expires today (still good)
    ///   negative = already expired
    /// </summary>
    public void AddItem(string name, int expiredDays)
    {
        _items.Add(new SupplyItem
        {
            Name = name,
            ExpirationDate = DateTime.Today.AddDays(expiredDays)
        });
    }

    /// <summary>
    /// Removes all items that have expired (expiration date is before today).
    /// Items expiring today are still considered valid.
    /// </summary>
    public void RemoveExpiredItems()
    {
        foreach (var item in _items)
        {
            if (item.ExpirationDate < DateTime.Today)
            {
                _items.Remove(item);
            }
        }
    }
}

public class SupplyItem
{
    public string Name { get; set; } = "";
    public DateTime ExpirationDate { get; set; }
}

/// <summary>
/// Tracks qualification test scores for crew members.
/// </summary>
public class CrewQualifications
{
    private readonly Dictionary<string, List<int>> _scores = new();

    public void RecordScore(string crewMember, int score)
    {
        if (!_scores.ContainsKey(crewMember))
            _scores[crewMember] = new List<int>();
        _scores[crewMember].Add(score);
    }

    /// <summary>
    /// Gets the average score for a crew member, rounded to 2 decimal places.
    /// </summary>
    public double GetAverage(string crewMember)
    {
        if (!_scores.ContainsKey(crewMember))
            return 0.0;

        var scores = _scores[crewMember];

        int sum = 0;
        for (int i = 0; i < scores.Count; i++)
            sum += scores[i];

        double average = sum / scores.Count;
        return Math.Round(average, 2);
    }
}
