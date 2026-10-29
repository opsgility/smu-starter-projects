type Route = {
  id: string;
  name: string;
  distance_km: number;
  difficulty: string;
  hero_image: string;
};

async function fetchRoutes(): Promise<Route[]> {
  const base =
    process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8787";
  try {
    const res = await fetch(`${base}/routes`, { cache: "no-store" });
    const data = await res.json();
    return data.routes ?? [];
  } catch {
    return [];
  }
}

export default async function HomePage() {
  const routes = await fetchRoutes();

  return (
    <main style={{ maxWidth: 920, margin: "0 auto", padding: "48px 24px" }}>
      <h1 style={{ fontSize: 36, marginBottom: 8 }}>Lumen Trail</h1>
      <p style={{ marginTop: 0, color: "#4b5e4b" }}>
        Featured hiking routes, curated by the community.
      </p>

      {routes.length === 0 ? (
        <p style={{ color: "#8a3a3a" }}>
          Could not reach the API. Is it running on{" "}
          {process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8787"}?
        </p>
      ) : (
        <ul style={{ listStyle: "none", padding: 0, marginTop: 32 }}>
          {routes.map((r) => (
            <li
              key={r.id}
              style={{
                background: "white",
                padding: 20,
                marginBottom: 16,
                borderRadius: 12,
                boxShadow: "0 2px 10px rgba(0,0,0,0.05)"
              }}
            >
              <h2 style={{ margin: "0 0 6px 0" }}>{r.name}</h2>
              <small style={{ color: "#4b5e4b" }}>
                {r.distance_km} km · {r.difficulty}
              </small>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
