using System.Data.Common;
using Microsoft.Data.SqlClient;
using Microsoft.EntityFrameworkCore.Diagnostics;
using Microsoft.Extensions.Logging;

namespace Anchorline.Resiliency;

// EF Core command interceptor that simulates a transient Azure SQL failure
// by throwing SqlException 40613 the first N times a command executes.
// Used to prove that EnableRetryOnFailure catches and retries the exception.
public class TransientInjector : DbCommandInterceptor
{
    private readonly int _failuresRemaining;
    private int _fired;
    private readonly ILogger _log;

    public TransientInjector(int failuresBeforeSuccess, ILogger log)
    {
        _failuresRemaining = failuresBeforeSuccess;
        _log = log;
    }

    public override InterceptionResult<DbDataReader> ReaderExecuting(
        DbCommand command, CommandEventData eventData, InterceptionResult<DbDataReader> result)
        => Trip("ReaderExecuting") ?? result;

    public override async ValueTask<InterceptionResult<DbDataReader>> ReaderExecutingAsync(
        DbCommand command, CommandEventData eventData, InterceptionResult<DbDataReader> result,
        CancellationToken cancellationToken = default)
        => Trip("ReaderExecutingAsync") ?? result;

    public override InterceptionResult<int> NonQueryExecuting(
        DbCommand command, CommandEventData eventData, InterceptionResult<int> result)
        => TripInt("NonQueryExecuting") ?? result;

    public override async ValueTask<InterceptionResult<int>> NonQueryExecutingAsync(
        DbCommand command, CommandEventData eventData, InterceptionResult<int> result,
        CancellationToken cancellationToken = default)
        => TripInt("NonQueryExecutingAsync") ?? result;

    private InterceptionResult<DbDataReader>? Trip(string where)
    {
        if (Interlocked.Increment(ref _fired) <= _failuresRemaining)
        {
            _log.LogWarning("TransientInjector: throwing 40613 at {where} (attempt {n})", where, _fired);
            throw MakeTransient();
        }
        return null;
    }

    private InterceptionResult<int>? TripInt(string where)
    {
        if (Interlocked.Increment(ref _fired) <= _failuresRemaining)
        {
            _log.LogWarning("TransientInjector: throwing 40613 at {where} (attempt {n})", where, _fired);
            throw MakeTransient();
        }
        return null;
    }

    private static SqlException MakeTransient()
    {
        // 40613 = Database currently unavailable — one of SqlAzureRetryingExecutionStrategy's transient codes.
        // Use reflection via SqlErrorCollection is complicated; simpler: use a factory that returns a
        // SqlException instance via internal helper. Fallback: use a workaround by opening a real invalid
        // command against a dummy connection — but for simplicity here we throw a wrapped exception.
        // For the lab, wrap a synthetic Exception in a way EF's execution strategy still retries:
        // EF's SqlServerRetryingExecutionStrategy.ShouldRetryOn checks SqlException.Number.
        // We can't easily construct SqlException, so we use SqlException's factory via reflection:
        return SqlExceptionFactory.Create(40613, "Database 'AnchorlineOrders' on server is currently unavailable. Please retry the connection later. (Injected by lab)");
    }
}

// Reflection-based SqlException factory. Microsoft.Data.SqlClient exposes SqlException.CreateException
// as internal, so we build the same shape.
internal static class SqlExceptionFactory
{
    public static SqlException Create(int number, string message)
    {
        var errType = typeof(SqlError);
        var errCtor = errType.GetConstructor(
            System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance,
            null,
            new[] { typeof(int), typeof(byte), typeof(byte), typeof(string), typeof(string), typeof(string), typeof(int), typeof(uint), typeof(Exception) },
            null)
            ?? throw new InvalidOperationException("SqlError ctor not found");

        var error = (SqlError)errCtor.Invoke(new object?[]
        {
            number, (byte)0, (byte)13, "server", message, "proc", 0, 0u, null
        });

        var collType = typeof(SqlErrorCollection);
        var collCtor = collType.GetConstructor(
            System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance,
            null, Type.EmptyTypes, null)!;
        var coll = (SqlErrorCollection)collCtor.Invoke(null);
        var addMethod = collType.GetMethod("Add", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance)!;
        addMethod.Invoke(coll, new object[] { error });

        var exType = typeof(SqlException);
        var exCtor = exType.GetMethod("CreateException",
            System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Static,
            null, new[] { typeof(SqlErrorCollection), typeof(string) }, null)!;
        return (SqlException)exCtor.Invoke(null, new object[] { coll, "42.42.42.42" })!;
    }
}
