"use client";

import { useState } from "react";
import { FileText, Download, Shield, FileCheck2, ExternalLink, Calendar, CheckCircle2, Plus } from "lucide-react";

export default function ReportsDashboard() {
  const [auditMode, setAuditMode] = useState(false);

  return (
    <div className="flex flex-col gap-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight">Audit & Reports</h1>
          <p className="text-sm text-slate-500 mt-1">Generate compliance packs, evidence indexes, and executive summaries.</p>
        </div>
        <div className="flex items-center gap-3">
          <label className="flex items-center gap-2 cursor-pointer">
            <span className="text-sm font-medium text-slate-600 dark:text-slate-400">Read-Only Audit Mode</span>
            <div className="relative inline-block w-10 mr-2 align-middle select-none transition duration-200 ease-in">
              <input type="checkbox" name="toggle" id="toggle" checked={auditMode} onChange={() => setAuditMode(!auditMode)} className="toggle-checkbox absolute block w-5 h-5 rounded-full bg-white border-4 appearance-none cursor-pointer border-slate-300 dark:border-slate-600 checked:right-0 checked:border-brand-500 z-10 top-0 bottom-0 m-auto right-5 transition-all duration-200" />
              <label htmlFor="toggle" className={`toggle-label block overflow-hidden h-5 rounded-full cursor-pointer ${auditMode ? 'bg-brand-500' : 'bg-slate-300 dark:bg-slate-700'}`}></label>
            </div>
          </label>
          <button className="bg-brand-500 hover:bg-brand-600 text-white px-4 py-2 rounded-md font-medium text-sm flex items-center gap-2 transition-colors">
            <Plus className="w-4 h-4" />
            Custom Report
          </button>
        </div>
      </div>

      {auditMode && (
        <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-lg p-4 flex items-start gap-3">
          <Shield className="w-5 h-5 text-emerald-500 mt-0.5" />
          <div>
            <h4 className="font-semibold text-emerald-700 dark:text-emerald-400">Audit Mode Active</h4>
            <p className="text-sm text-emerald-600 dark:text-emerald-500 mt-1">Internal comments, draft risks, and sensitive metadata are now hidden. You can safely share this view or export reports for external regulators/auditors.</p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-3 gap-6 mt-2">
        {/* Report Template Cards */}
        <div className="bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm flex flex-col hover:border-brand-500 transition-colors cursor-pointer group">
          <div className="bg-blue-500/10 w-12 h-12 rounded-lg flex items-center justify-center mb-4 text-blue-600 dark:text-blue-400 group-hover:scale-110 transition-transform">
            <FileCheck2 className="w-6 h-6" />
          </div>
          <h3 className="font-semibold text-lg">EU AI Act Audit Pack</h3>
          <p className="text-sm text-slate-500 mt-2 flex-1">Generates Technical Documentation, Risk Management system records, and logging procedures for High-Risk systems.</p>
          <div className="mt-6 flex items-center justify-between text-sm">
            <span className="text-slate-400 flex items-center gap-1"><Calendar className="w-3.5 h-3.5" /> Updated today</span>
            <span className="text-brand-500 font-medium flex items-center gap-1">Generate <Download className="w-3.5 h-3.5" /></span>
          </div>
        </div>

        <div className="bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm flex flex-col hover:border-brand-500 transition-colors cursor-pointer group">
          <div className="bg-emerald-500/10 w-12 h-12 rounded-lg flex items-center justify-center mb-4 text-emerald-600 dark:text-emerald-400 group-hover:scale-110 transition-transform">
            <Shield className="w-6 h-6" />
          </div>
          <h3 className="font-semibold text-lg">NIST AI RMF Report</h3>
          <p className="text-sm text-slate-500 mt-2 flex-1">Summarizes implementation of Map, Measure, Manage, and Govern functions with linked evidence.</p>
          <div className="mt-6 flex items-center justify-between text-sm">
            <span className="text-slate-400 flex items-center gap-1"><Calendar className="w-3.5 h-3.5" /> Last run 2d ago</span>
            <span className="text-brand-500 font-medium flex items-center gap-1">Generate <Download className="w-3.5 h-3.5" /></span>
          </div>
        </div>

        <div className="bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm flex flex-col hover:border-brand-500 transition-colors cursor-pointer group">
          <div className="bg-purple-500/10 w-12 h-12 rounded-lg flex items-center justify-center mb-4 text-purple-600 dark:text-purple-400 group-hover:scale-110 transition-transform">
            <FileText className="w-6 h-6" />
          </div>
          <h3 className="font-semibold text-lg">Board Risk Summary</h3>
          <p className="text-sm text-slate-500 mt-2 flex-1">One-page executive PDF highlighting top exposures, compliance posture trends, and major incidents.</p>
          <div className="mt-6 flex items-center justify-between text-sm">
            <span className="text-slate-400 flex items-center gap-1"><Calendar className="w-3.5 h-3.5" /> Last run 1w ago</span>
            <span className="text-brand-500 font-medium flex items-center gap-1">Generate <Download className="w-3.5 h-3.5" /></span>
          </div>
        </div>
      </div>

      <div className="bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm flex flex-col flex-1 overflow-hidden mt-4">
        <div className="p-4 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50">
          <h3 className="font-semibold">Recent Evidence Index</h3>
        </div>
        <div className="divide-y divide-slate-200 dark:divide-slate-800">
          <div className="p-4 flex items-center justify-between hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
            <div className="flex items-center gap-4">
              <div className="bg-slate-100 dark:bg-slate-800 p-2 rounded"><FileText className="w-4 h-4 text-slate-500" /></div>
              <div>
                <h4 className="font-medium text-sm">Credit Scoring Bias Assessment Q3.pdf</h4>
                <p className="text-xs text-slate-500 mt-0.5">Linked to <span className="font-medium text-slate-700 dark:text-slate-300">SYS-001</span> • Uploaded by Alice Compliance</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <span className="flex items-center gap-1 text-xs font-medium text-emerald-600 bg-emerald-50 dark:bg-emerald-900/20 px-2 py-1 rounded border border-emerald-200 dark:border-emerald-800/30">
                <CheckCircle2 className="w-3 h-3" /> Validated
              </span>
              <button className="text-slate-400 hover:text-brand-500"><ExternalLink className="w-4 h-4" /></button>
            </div>
          </div>
          <div className="p-4 flex items-center justify-between hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
            <div className="flex items-center gap-4">
              <div className="bg-slate-100 dark:bg-slate-800 p-2 rounded"><FileText className="w-4 h-4 text-slate-500" /></div>
              <div>
                <h4 className="font-medium text-sm">Data Lineage Diagram v2.png</h4>
                <p className="text-xs text-slate-500 mt-0.5">Linked to <span className="font-medium text-slate-700 dark:text-slate-300">SYS-001</span> • Uploaded by Bob Data</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <span className="flex items-center gap-1 text-xs font-medium text-emerald-600 bg-emerald-50 dark:bg-emerald-900/20 px-2 py-1 rounded border border-emerald-200 dark:border-emerald-800/30">
                <CheckCircle2 className="w-3 h-3" /> Validated
              </span>
              <button className="text-slate-400 hover:text-brand-500"><ExternalLink className="w-4 h-4" /></button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
