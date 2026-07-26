import Link from "next/link";
import { LayoutDashboard, Shield, AlertTriangle, FileText } from "lucide-react";

export function Sidebar() {
  return (
    <div className="w-64 h-screen bg-surface-light dark:bg-surface-dark border-r border-slate-200 dark:border-slate-800 flex flex-col">
      <div className="p-6">
        <h1 className="text-2xl font-bold tracking-tight text-brand-500">Secpol</h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 font-medium tracking-wider mt-1">AI COMPLIANCE OS</p>
      </div>
      <nav className="flex-1 px-4 space-y-2">
        <Link href="/" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-100 dark:hover:bg-slate-800 text-sm font-medium transition-colors">
          <LayoutDashboard className="w-4 h-4" />
          Dashboard
        </Link>
        <Link href="/systems" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-100 dark:hover:bg-slate-800 text-sm font-medium transition-colors">
          <Shield className="w-4 h-4" />
          AI Systems
        </Link>
        <Link href="/risks" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-100 dark:hover:bg-slate-800 text-sm font-medium transition-colors">
          <AlertTriangle className="w-4 h-4" />
          Risks & Incidents
        </Link>
        <Link href="/reports" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-100 dark:hover:bg-slate-800 text-sm font-medium transition-colors">
          <FileText className="w-4 h-4" />
          Audit & Reports
        </Link>
      </nav>
      <div className="p-4 text-xs text-slate-500 dark:text-slate-400">
        <p>Shortcuts:</p>
        <div className="flex flex-col gap-1 mt-2 font-mono">
          <span><kbd className="bg-slate-200 dark:bg-slate-700 px-1 rounded">⌘K</kbd> Search</span>
          <span><kbd className="bg-slate-200 dark:bg-slate-700 px-1 rounded">g a</kbd> AI Systems</span>
          <span><kbd className="bg-slate-200 dark:bg-slate-700 px-1 rounded">g c</kbd> Controls</span>
        </div>
      </div>
    </div>
  );
}
