export default function Home() {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight">Dashboard</h1>
          <p className="text-sm text-slate-500 mt-1">Welcome to Secpol AI Compliance OS.</p>
        </div>
      </div>
      <div className="grid grid-cols-3 gap-6">
        <div className="bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm">
          <h3 className="text-sm font-medium text-slate-500">Total AI Systems</h3>
          <p className="text-3xl font-semibold mt-2">12</p>
        </div>
        <div className="bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm">
          <h3 className="text-sm font-medium text-slate-500">High Risk Systems</h3>
          <p className="text-3xl font-semibold mt-2 text-risk-high">4</p>
        </div>
        <div className="bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm">
          <h3 className="text-sm font-medium text-slate-500">Open Incidents</h3>
          <p className="text-3xl font-semibold mt-2 text-risk-limited">2</p>
        </div>
      </div>
    </div>
  );
}
