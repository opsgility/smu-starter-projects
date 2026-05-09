import 'dotenv/config';
import { db } from './client';
import { users } from './schema';

async function seed() {
  const [user] = await db
    .insert(users)
    .values({
      email: 'demo@retirescope.local',
      birthYear: 1965,
      retirementAge: 65,
    })
    .returning();

  console.log('Seeded user:', user);
  process.exit(0);
}

seed().catch((e) => {
  console.error(e);
  process.exit(1);
});
