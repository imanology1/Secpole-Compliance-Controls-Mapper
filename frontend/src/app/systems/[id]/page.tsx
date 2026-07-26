"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { ArrowLeft, ShieldCheck, Target } from "lucide-react";

interface AISystem {
  id: string;
  name: string;
  owner: string;
  business_unit: string;
  eu_ai_act_risk_classification: string;
  framework_profiles: string[];
  intended_purpose: string;
  model_type: string;
}

interface ControlsInfo {
  system_id: string;
  applicable_frameworks: {
    framework: string;
    total_controls: number;
    sample_controls: { id: string; name: string }[];
  }[];
}

export default function SystemDetail() {
  const params = useParams();
  const router = useRouter();
  const [system, setSystem] = useState<AISystem | null>(null);
  const [controlsInfo, setControlsInfo] = useState<ControlsInfo | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch system details and applicable controls concurrently
    Promise.all([
      fetch(`http://localhost:8000/api/systems/${params.id}`).then(r => r.json()),
      fetch(`http://localhost:8000/api/systems/${params.id}/controls`).then(r => r.json())
    ])
      .then(([sysData, ctrlData]) => {
        setSystem(sysData);
        setControlsInfo(ctrlData);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, [params.id]);

  if (loading) return <div className="animate-pulse">Loading system details...</div>;
  if (!system) return <div>System not found.</div>;

  return (
    <div className="flex flex-col gap-6">
      {/* Breadcrumbs */}
      <button onClick={() => router.back()} className="flex items-center gap-2 text-sm text-slate-500 hover:text-slate-900 dark:hover:text-slate-100 transition-colors self-start">
        <ArrowLeft className="w-4 h-4" />
        Back to Systems
      </button>

      {/* Header Summary Card */}
      <div className="bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">{system.name}</h1>
          <p className="text-slate-500 mt-1">{system.id} • Owned by {system.owner} ({system.business_unit})</p>
          <div className="mt-4 flex gap-2">
            <span className="bg-risk-high/10 text-risk-high border border-risk-high/20 px-2 py-1 rounded text-xs font-semibold uppercase">
              {system.eu_ai_act_risk_classification} RISK
            </span>
            <span className="bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 px-2 py-1 rounded text-xs font-medium border border-slate-200 dark:border-slate-700">
              {system.model_type.replace('_', ' ')}
            </span>
          </div>
        </div>
        <div className="flex gap-4">
          <div className="text-center px-6 py-2 border-l border-slate-200 dark:border-slate-800">
            <p className="text-xs text-slate-500 font-medium uppercase tracking-wider mb-1">Controls mapped</p>
            <p className="text-2xl font-semibold text-brand-500">
              {controlsInfo?.applicable_frameworks?.reduce((acc: number, f) => acc + f.total_controls, 0) || 0}
            </p>
          </div>
        </div>
      </div>

      {/* Main Tabs Layout */}
      <div className="bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm overflow-hidden flex flex-col">
        <div className="flex border-b border-slate-200 dark:border-slate-800">
          <button className="px-6 py-3 text-sm font-medium text-brand-600 dark:text-brand-400 border-b-2 border-brand-500 bg-brand-50 dark:bg-brand-900/10">Overview</button>
          <button className="px-6 py-3 text-sm font-medium text-slate-500 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">Controls</button>
          <button className="px-6 py-3 text-sm font-medium text-slate-500 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">Risks</button>
          <button className="px-6 py-3 text-sm font-medium text-slate-500 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">Documentation</button>
          <button className="px-6 py-3 text-sm font-medium text-slate-500 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">Activity</button>
        </div>

        {/* Tab Content - Overview */}
        <div className="p-6 grid grid-cols-3 gap-8">
          <div className="col-span-2 space-y-8">
            <div>
              <h3 className="text-lg font-semibold flex items-center gap-2 mb-4">
                <Target className="w-5 h-5 text-brand-500" />
                Intended Purpose
              </h3>
              <p className="text-slate-600 dark:text-slate-300 text-sm leading-relaxed cursor-text hover:bg-slate-50 dark:hover:bg-slate-800 p-2 -ml-2 rounded transition-colors group relative">
                {system.intended_purpose}
                <span className="absolute right-2 top-2 opacity-0 group-hover:opacity-100 text-xs text-slate-400 font-medium">Click to edit</span>
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
              <div className="space-y-4 relative before:absolute before:inset-0 before:ml-2.5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-200 dark:before:via-slate-800 before:to-transparent">
                <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                  <div className="flex items-center justify-center w-6 h-6 rounded-full border border-white dark:border-slate-900 bg-slate-200 dark:bg-slate-700 text-slate-500 shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow"></div>
                  <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] bg-slate-50 dark:bg-slate-800/50 p-3 rounded-lg border border-slate-200 dark:border-slate-700">
                    <p className="text-sm"><span className="font-medium text-slate-900 dark:text-slate-100">Alice Compliance</span> updated risk <span className="font-mono text-xs text-brand-500">RSK-001</span> status to <span className="font-medium text-emerald-500">Mitigated</span>.</p>
                    <time className="block text-xs font-medium text-slate-500 mt-1">2 hours ago</time>
                  </div>
                </div>
                <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                  <div className="flex items-center justify-center w-6 h-6 rounded-full border border-white dark:border-slate-900 bg-slate-200 dark:bg-slate-700 text-slate-500 shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow"></div>
                  <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] bg-slate-50 dark:bg-slate-800/50 p-3 rounded-lg border border-slate-200 dark:border-slate-700">
                    <p className="text-sm"><span className="font-medium text-slate-900 dark:text-slate-100">Bob Data</span> attached new evidence <span className="italic">Data Lineage Diagram.png</span> to control <span className="font-mono text-xs text-brand-500">NIST-AIRMF MAP 1.1</span>.</p>
                    <time className="block text-xs font-medium text-slate-500 mt-1">Yesterday at 4:32 PM</time>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div>
            <h3 className="text-lg font-semibold flex items-center gap-2 mb-4">
              <ShieldCheck className="w-5 h-5 text-emerald-500" />
              Compliance Scope
            </h3>
            <div className="space-y-4">
              {controlsInfo?.applicable_frameworks?.map((fw) => (
                <div key={fw.framework} className="bg-slate-50 dark:bg-slate-900 p-4 rounded-lg border border-slate-200 dark:border-slate-800">
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-semibold">{fw.framework}</span>
                    <span className="text-xs text-slate-500">{fw.total_controls} controls</span>
                  </div>
                  <div className="w-full bg-slate-200 dark:bg-slate-800 rounded-full h-2">
                    <div className="bg-brand-500 h-2 rounded-full" style={{ width: '45%' }}></div>
                  </div>
                  <p className="text-xs text-slate-500 mt-2 text-right">45% implemented</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
