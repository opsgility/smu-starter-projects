namespace LumenLogistics.Api.Models;

public record Package(
    string Id,
    string Recipient,
    string Destination,
    string Status);
