"use client";

import { useState, useEffect } from "react";
import { Search, Filter, Plus, ShieldAlert } from "lucide-react";
import Link from "next/link";

interface AISystem {
  id: string;
  name: string;
  owner: string;
  business_unit: string;
  eu_ai_act_risk_classification: string;
  framework_profiles: string[];
}

export default function SystemsInventory() {
  const [systems, setSystems] = useState<AISystem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch from FastAPI backend
    fetch("http://localhost:8000/api/systems/")
      .then(res => res.json())
      .then(data => {
        setSystems(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const getRiskBadge = (risk: string) => {
    switch(risk) {
      case 'unacceptable': return <span className="bg-risk-unacceptable/10 text-risk-unacceptable border border-risk-unacceptable/20 px-2 py-1 rounded text-xs font-semibold uppercase">Unacceptable</span>;
      case 'high': return <span className="bg-risk-high/10 text-risk-high border border-risk-high/20 px-2 py-1 rounded text-xs font-semibold uppercase">High</span>;
      case 'limited': return <span className="bg-risk-limited/10 text-risk-limited border border-risk-limited/20 px-2 py-1 rounded text-xs font-semibold uppercase">Limited</span>;
      case 'minimal': return <span className="bg-risk-minimal/10 text-risk-minimal border border-risk-minimal/20 px-2 py-1 rounded text-xs font-semibold uppercase">Minimal</span>;
      default: return null;
    }
  };

  return (
    <div className="flex flex-col gap-6 h-full">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight">AI Systems Inventory</h1>
          <p className="text-sm text-slate-500 mt-1">Manage and monitor your organization&apos;s AI deployments and their regulatory posture.</p>
        </div>
        <button className="bg-brand-500 hover:bg-brand-600 text-white px-4 py-2 rounded-md font-medium text-sm flex items-center gap-2 transition-colors">
          <Plus className="w-4 h-4" />
          Add AI System
        </button>
      </div>

      <div className="bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm flex flex-col flex-1 overflow-hidden">
        {/* Toolbar */}
        <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex items-center gap-4">
          <div className="relative flex-1 max-w-md">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search by name, owner, or business unit..."
              className="w-full pl-9 pr-4 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-md text-sm outline-none focus:border-brand-500 dark:text-slate-100 transition-colors"
            />
          </div>
          <button className="flex items-center gap-2 px-3 py-2 border border-slate-200 dark:border-slate-700 rounded-md text-sm font-medium hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
            <Filter className="w-4 h-4 text-slate-500" />
            Filters
          </button>
        </div>

        {/* Table */}
        <div className="overflow-auto flex-1">
          <table className="w-full text-left text-sm whitespace-nowrap">
            <thead className="bg-slate-50 dark:bg-slate-900/50 sticky top-0 border-b border-slate-200 dark:border-slate-800">
              <tr>
                <th className="px-6 py-4 font-semibold text-slate-600 dark:text-slate-400">System Name</th>
                <th className="px-6 py-4 font-semibold text-slate-600 dark:text-slate-400">Owner</th>
                <th className="px-6 py-4 font-semibold text-slate-600 dark:text-slate-400">EU AI Act Risk</th>
                <th className="px-6 py-4 font-semibold text-slate-600 dark:text-slate-400">Frameworks</th>
                <th className="px-6 py-4 font-semibold text-slate-600 dark:text-slate-400 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
              {loading ? (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-slate-500">Loading AI systems...</td>
                </tr>
              ) : systems.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-slate-500">
                    <div className="flex flex-col items-center gap-2">
                      <ShieldAlert className="w-8 h-8 text-slate-300" />
                      <p>No AI systems found in registry.</p>
                    </div>
                  </td>
                </tr>
              ) : (
                systems.map(sys => (
                  <tr key={sys.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors group">
                    <td className="px-6 py-4">
                      <Link href={`/systems/${sys.id}`} className="font-semibold text-brand-600 dark:text-brand-400 hover:underline">
                        {sys.name}
                      </Link>
                      <div className="text-xs text-slate-500 mt-1">{sys.id} • {sys.business_unit}</div>
                    </td>
                    <td className="px-6 py-4">{sys.owner}</td>
                    <td className="px-6 py-4">{getRiskBadge(sys.eu_ai_act_risk_classification)}</td>
                    <td className="px-6 py-4">
                      <div className="flex gap-2">
                        {sys.framework_profiles.map(fw => (
                          <span key={fw} className="bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 px-2 py-1 rounded text-xs font-medium border border-slate-200 dark:border-slate-700">
                            {fw}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <Link href={`/systems/${sys.id}`} className="text-sm font-medium text-slate-500 hover:text-brand-500 transition-colors">
                        View Details →
                      </Link>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
