import { redirect } from 'next/navigation';
import { createAccount } from '@/lib/actions/accounts';

const TYPE_OPTIONS = [
  { value: 'taxable', label: 'Taxable' },
  { value: 'traditional_ira', label: 'Traditional IRA' },
  { value: 'roth_ira', label: 'Roth IRA' },
  { value: 'traditional_401k', label: 'Traditional 401k' },
  { value: 'roth_401k', label: 'Roth 401k' },
  { value: 'hsa', label: 'HSA' },
  { value: 'cash', label: 'Cash' },
] as const;

export default function NewAccountPage() {
  async function handleSubmit(formData: FormData) {
    'use server';
    await createAccount({
      userId: 1,
      name: formData.get('name') as string,
      type: formData.get('type') as 'taxable',
      institution: (formData.get('institution') as string) || null,
    });
    redirect('/accounts');
  }

  return (
    <div className="max-w-md mx-auto mt-8">
      <h1 className="text-2xl font-bold text-rs-fg mb-6">Add Account</h1>
      <form
        action={handleSubmit}
        className="bg-rs-surface border border-rs-border rounded-2xl p-6 space-y-4"
      >
        <div>
          <label className="block text-rs-fg-muted text-sm mb-1.5">Name</label>
          <input
            name="name"
            required
            placeholder="Schwab Brokerage"
            className="w-full bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg"
          />
        </div>
        <div>
          <label className="block text-rs-fg-muted text-sm mb-1.5">Type</label>
          <select
            name="type"
            required
            className="w-full bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg"
          >
            {TYPE_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-rs-fg-muted text-sm mb-1.5">
            Institution (optional)
          </label>
          <input
            name="institution"
            placeholder="Schwab"
            className="w-full bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg"
          />
        </div>
        <button
          type="submit"
          className="w-full bg-rs-primary text-rs-primary-fg rounded-lg px-4 py-2 font-medium"
        >
          Create Account
        </button>
      </form>
    </div>
  );
}
