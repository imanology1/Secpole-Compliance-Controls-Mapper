"use client";

import { useEffect, useState } from "react";
import { Search } from "lucide-react";
import { useRouter } from "next/navigation";

export function SearchModal() {
  const [isOpen, setIsOpen] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Cmd/Ctrl + K to open search
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setIsOpen(true);
      }

      // Escape to close
      if (e.key === "Escape") {
        setIsOpen(false);
      }

      // Keyboard navigation (g+a, g+c) handled simplistically here for demo
      // In a real app, you'd use a more robust shortcut manager like react-hotkeys-hook
      if (!isOpen && e.key === "g") {
        const handleSecondKey = (e2: KeyboardEvent) => {
          if (e2.key === "a") router.push("/systems");
          if (e2.key === "c") router.push("/controls");
          document.removeEventListener("keydown", handleSecondKey);
        };
        document.addEventListener("keydown", handleSecondKey);
        setTimeout(() => document.removeEventListener("keydown", handleSecondKey), 1000);
      }
    };

    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, router]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-[20vh] bg-slate-900/50 backdrop-blur-sm" onClick={() => setIsOpen(false)}>
      <div
        className="w-full max-w-2xl bg-surface-light dark:bg-surface-dark rounded-xl shadow-2xl border border-slate-200 dark:border-slate-700 overflow-hidden"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center px-4 py-3 border-b border-slate-200 dark:border-slate-700">
          <Search className="w-5 h-5 text-slate-400 mr-3" />
          <input
            autoFocus
            type="text"
            placeholder="Search AI systems, controls, risks..."
            className="w-full bg-transparent border-none outline-none text-slate-900 dark:text-slate-50 placeholder-slate-400"
          />
          <span className="text-xs font-mono text-slate-400 bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded border border-slate-200 dark:border-slate-700">ESC</span>
        </div>
        <div className="p-4 text-sm text-slate-500">
          Start typing to search...
        </div>
      </div>
    </div>
  );
}
