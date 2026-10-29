import type { Context } from "hono";

const FEATURED_ROUTES = [
  {
    id: "rt_rainier_wonderland",
    name: "Rainier Wonderland Loop",
    distance_km: 150,
    difficulty: "advanced",
    hero_image: "/images/rainier.jpg"
  },
  {
    id: "rt_zion_narrows",
    name: "Zion Narrows Bottom-Up",
    distance_km: 15,
    difficulty: "intermediate",
    hero_image: "/images/zion.jpg"
  },
  {
    id: "rt_angels_rest",
    name: "Angels Rest Out-and-Back",
    distance_km: 7,
    difficulty: "beginner",
    hero_image: "/images/angels-rest.jpg"
  }
];

export function routesHandler(c: Context) {
  return c.json({ routes: FEATURED_ROUTES });
}
