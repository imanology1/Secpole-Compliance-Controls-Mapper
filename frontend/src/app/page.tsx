"use client";

import { ShieldCheck, Target, AlertTriangle, FileText, ArrowRight } from "lucide-react";
import Link from "next/link";

export default function ExecutiveDashboard() {
  return (
    <div className="flex flex-col gap-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-semibold tracking-tight">Executive Summary</h1>
        <p className="text-sm text-slate-500 mt-1">Real-time overview of organizational AI compliance and risk posture.</p>
      </div>

      {/* KPI Row */}
      <div className="grid grid-cols-4 gap-4">
        <div className="bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-800 rounded-xl p-5 shadow-sm">
          <div className="flex items-center gap-3 mb-2 text-slate-500">
            <Target className="w-4 h-4" />
            <h3 className="text-sm font-medium">Active AI Systems</h3>
          </div>
          <p className="text-3xl font-bold">12</p>
        </div>
        <div className="bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-800 rounded-xl p-5 shadow-sm">
          <div className="flex items-center gap-3 mb-2 text-slate-500">
            <ShieldCheck className="w-4 h-4" />
            <h3 className="text-sm font-medium">Control Coverage</h3>
          </div>
          <div className="flex items-baseline gap-2">
            <p className="text-3xl font-bold">68%</p>
            <span className="text-xs text-emerald-500 font-medium">↑ 12%</span>
          </div>
        </div>
        <div className="bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-800 rounded-xl p-5 shadow-sm">
          <div className="flex items-center gap-3 mb-2 text-slate-500">
            <AlertTriangle className="w-4 h-4" />
            <h3 className="text-sm font-medium">High/Critical Risks</h3>
          </div>
          <div className="flex items-baseline gap-2">
            <p className="text-3xl font-bold text-risk-high">4</p>
            <span className="text-xs text-risk-high font-medium">Action Required</span>
          </div>
        </div>
        <div className="bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-800 rounded-xl p-5 shadow-sm">
          <div className="flex items-center gap-3 mb-2 text-slate-500">
            <FileText className="w-4 h-4" />
            <h3 className="text-sm font-medium">Audit Readiness</h3>
          </div>
          <div className="flex items-baseline gap-2">
            <p className="text-3xl font-bold text-brand-500">B+</p>
            <span className="text-xs text-slate-400 font-medium">EU AI Act</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-8">
        {/* Main Column */}
        <div className="col-span-2 flex flex-col gap-6">
          <div className="bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6">
            <h3 className="text-lg font-semibold mb-6">Top AI Risk Exposures</h3>
            <div className="space-y-4">
              <div className="flex items-start gap-4 p-4 bg-slate-50 dark:bg-slate-900 rounded-lg border border-slate-100 dark:border-slate-800">
                <div className="w-2 h-2 mt-2 rounded-full bg-risk-high flex-shrink-0"></div>
                <div>
                  <h4 className="font-medium">Payments classification model has 3 open high-severity risks; 2 controls missing.</h4>
                  <p className="text-sm text-slate-500 mt-1">Impacts NIST AI RMF &quot;Map&quot; function compliance. Target resolution: 14 days.</p>
                </div>
              </div>
              <div className="flex items-start gap-4 p-4 bg-slate-50 dark:bg-slate-900 rounded-lg border border-slate-100 dark:border-slate-800">
                <div className="w-2 h-2 mt-2 rounded-full bg-risk-limited flex-shrink-0"></div>
                <div>
                  <h4 className="font-medium">EU AI Act technical documentation for 2 high-risk systems due for annual review.</h4>
                  <p className="text-sm text-slate-500 mt-1">Systems: Credit Scoring Bot, HR Resume Screener.</p>
                </div>
              </div>
            </div>
            <Link href="/risks" className="inline-flex items-center gap-2 mt-4 text-sm font-medium text-brand-500 hover:text-brand-600 transition-colors">
              View all risks <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>

        {/* Side Column */}
        <div className="flex flex-col gap-6">
          <div className="bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6">
            <h3 className="text-lg font-semibold mb-4">Framework Coverage</h3>
            <div className="space-y-5">
              <div>
                <div className="flex justify-between text-sm font-medium mb-1">
                  <span>EU AI Act</span>
                  <span className="text-brand-500">42%</span>
                </div>
                <div className="w-full bg-slate-100 dark:bg-slate-800 rounded-full h-2">
                  <div className="bg-brand-500 h-2 rounded-full" style={{ width: '42%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm font-medium mb-1">
                  <span>NIST AI RMF</span>
                  <span className="text-brand-500">81%</span>
                </div>
                <div className="w-full bg-slate-100 dark:bg-slate-800 rounded-full h-2">
                  <div className="bg-brand-500 h-2 rounded-full" style={{ width: '81%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm font-medium mb-1">
                  <span>ISO 42001</span>
                  <span className="text-brand-500">15%</span>
                </div>
                <div className="w-full bg-slate-100 dark:bg-slate-800 rounded-full h-2">
                  <div className="bg-brand-500 h-2 rounded-full" style={{ width: '15%' }}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
