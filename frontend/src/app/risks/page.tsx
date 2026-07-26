"use client";

import { useEffect, useState } from "react";
import { AlertCircle, TrendingUp, AlertOctagon, Filter, CheckCircle2 } from "lucide-react";
import Link from "next/link";

interface Risk {
  id: string;
  system_id: string;
  name: string;
  description: string;
  severity: string;
  status: string;
  owner: string;
}

export default function RisksDashboard() {
  const [risks, setRisks] = useState<Risk[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/risks/")
      .then(res => res.json())
      .then(data => {
        setRisks(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const getSeverityBadge = (severity: string) => {
    switch (severity) {
      case "critical": return <span className="text-risk-unacceptable bg-risk-unacceptable/10 px-2 py-1 rounded text-xs font-semibold uppercase border border-risk-unacceptable/20">Critical</span>;
      case "high": return <span className="text-risk-high bg-risk-high/10 px-2 py-1 rounded text-xs font-semibold uppercase border border-risk-high/20">High</span>;
      case "medium": return <span className="text-risk-limited bg-risk-limited/10 px-2 py-1 rounded text-xs font-semibold uppercase border border-risk-limited/20">Medium</span>;
      case "low": return <span className="text-slate-500 bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded text-xs font-semibold uppercase border border-slate-200 dark:border-slate-700">Low</span>;
      default: return null;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "open": return <AlertCircle className="w-4 h-4 text-risk-high" />;
      case "in_progress": return <TrendingUp className="w-4 h-4 text-brand-500" />;
      case "mitigated": return <CheckCircle2 className="w-4 h-4 text-risk-minimal" />;
      default: return <AlertCircle className="w-4 h-4 text-slate-500" />;
    }
  };

  return (
    <div className="flex flex-col gap-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight">Risks & Incidents</h1>
          <p className="text-sm text-slate-500 mt-1">Monitor the top risks across your AI systems and track mitigation progress.</p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm flex items-center justify-between">
          <div>
            <h3 className="text-sm font-medium text-slate-500">Critical & High Risks</h3>
            <p className="text-3xl font-semibold mt-2 text-risk-high">{risks.filter(r => r.severity === 'high' || r.severity === 'critical').length}</p>
          </div>
          <div className="bg-risk-high/10 p-3 rounded-full"><AlertOctagon className="w-6 h-6 text-risk-high" /></div>
        </div>
        <div className="bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm flex items-center justify-between">
          <div>
            <h3 className="text-sm font-medium text-slate-500">Open Incidents (30d)</h3>
            <p className="text-3xl font-semibold mt-2 text-risk-limited">0</p>
          </div>
          <div className="bg-risk-limited/10 p-3 rounded-full"><AlertCircle className="w-6 h-6 text-risk-limited" /></div>
        </div>
        <div className="bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm flex items-center justify-between">
          <div>
            <h3 className="text-sm font-medium text-slate-500">Risks Mitigated</h3>
            <p className="text-3xl font-semibold mt-2 text-risk-minimal">{risks.filter(r => r.status === 'mitigated').length}</p>
          </div>
          <div className="bg-risk-minimal/10 p-3 rounded-full"><CheckCircle2 className="w-6 h-6 text-risk-minimal" /></div>
        </div>
      </div>

      <div className="bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm flex flex-col flex-1 overflow-hidden mt-2">
        <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex justify-between items-center bg-slate-50 dark:bg-slate-900/50">
          <h3 className="font-semibold">Top Risk Exposures</h3>
          <button className="flex items-center gap-2 px-3 py-1.5 border border-slate-200 dark:border-slate-700 rounded-md text-xs font-medium hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
            <Filter className="w-3.5 h-3.5" /> Filter
          </button>
        </div>
        <div className="divide-y divide-slate-200 dark:divide-slate-800">
          {loading ? (
            <div className="p-6 text-center text-slate-500">Loading risks...</div>
          ) : risks.length === 0 ? (
            <div className="p-6 text-center text-slate-500">No risks documented yet.</div>
          ) : (
            risks.map(risk => (
              <div key={risk.id} className="p-4 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors flex items-start gap-4">
                <div className="mt-1">{getStatusIcon(risk.status)}</div>
                <div className="flex-1">
                  <div className="flex items-center gap-3">
                    <h4 className="font-medium text-slate-900 dark:text-slate-100">{risk.name}</h4>
                    {getSeverityBadge(risk.severity)}
                  </div>
                  <p className="text-sm text-slate-500 mt-1 line-clamp-2">{risk.description}</p>
                  <div className="flex items-center gap-4 mt-3 text-xs text-slate-500 font-medium">
                    <span className="bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded">System: <Link href={`/systems/${risk.system_id}`} className="text-brand-500 hover:underline">{risk.system_id}</Link></span>
                    <span>Owner: {risk.owner}</span>
                    <span className="uppercase tracking-wider">Status: {risk.status.replace("_", " ")}</span>
                  </div>
                </div>
                <button className="text-sm text-brand-600 dark:text-brand-400 font-medium hover:underline">
                  View Detail
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
