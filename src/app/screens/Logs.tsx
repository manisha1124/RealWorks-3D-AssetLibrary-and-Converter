import React, { useState } from "react";
import { Info, AlertTriangle, XCircle, Search, Filter, X } from "lucide-react";
import { useAppContext, LogEntry } from "../context/AppContext";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { motion, AnimatePresence } from "motion/react";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function Logs() {
  const { logs } = useAppContext();
  const [filter, setFilter] = useState<"All" | "Info" | "Warning" | "Error">("All");
  const [search, setSearch] = useState("");
  const [selectedLog, setSelectedLog] = useState<LogEntry | null>(null);

  const filteredLogs = logs.filter(log => {
    if (filter !== "All" && log.severity !== filter) return false;
    if (search && !log.message.toLowerCase().includes(search.toLowerCase()) && !log.asset.toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  });

  return (
    <div className="flex-1 flex flex-col min-w-0 min-h-0 bg-[#1e1e1e] relative">
      <div className="h-14 border-b border-[#333] flex items-center justify-between px-6 shrink-0">
        <h1 className="text-lg font-semibold text-neutral-200">System Logs</h1>
        <div className="flex items-center gap-4">
          <div className="flex items-center bg-[#111] border border-[#333] rounded p-0.5">
            {["All", "Info", "Warning", "Error"].map(f => (
              <button
                key={f}
                onClick={() => setFilter(f as any)}
                className={cn(
                  "px-3 py-1 text-sm rounded transition-colors",
                  filter === f ? "bg-[#333] text-white" : "text-neutral-500 hover:text-neutral-300"
                )}
              >
                {f}
              </button>
            ))}
          </div>
          <div className="relative group">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-neutral-500 group-focus-within:text-blue-400 transition-colors" />
            <input 
              type="text" 
              placeholder="Search logs..." 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-64 bg-[#111] border border-[#333] rounded pl-9 pr-3 py-1.5 text-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all placeholder:text-neutral-600 text-neutral-200"
            />
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-auto p-6 custom-scrollbar">
        <div className="bg-[#1a1a1a] rounded-lg border border-[#333] overflow-hidden">
          <table className="w-full text-left text-sm whitespace-nowrap">
            <thead className="bg-[#222] border-b border-[#333]">
              <tr>
                <th className="px-4 py-3 font-medium text-neutral-400 w-32">Timestamp</th>
                <th className="px-4 py-3 font-medium text-neutral-400 w-32">Severity</th>
                <th className="px-4 py-3 font-medium text-neutral-400 w-64">Asset</th>
                <th className="px-4 py-3 font-medium text-neutral-400">Message</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#2a2a2a] font-mono">
              {filteredLogs.length === 0 ? (
                <tr>
                  <td colSpan={4} className="px-4 py-8 text-center text-neutral-500 font-sans">
                    No logs found
                  </td>
                </tr>
              ) : (
                filteredLogs.map(log => (
                  <tr 
                    key={log.id} 
                    className="hover:bg-[#222] transition-colors cursor-pointer"
                    onClick={() => setSelectedLog(log)}
                  >
                    <td className="px-4 py-2.5 text-neutral-500">{log.timestamp}</td>
                    <td className="px-4 py-2.5">
                      <div className="flex items-center gap-2">
                        {log.severity === "Info" && <Info className="w-4 h-4 text-blue-400" />}
                        {log.severity === "Warning" && <AlertTriangle className="w-4 h-4 text-amber-400" />}
                        {log.severity === "Error" && <XCircle className="w-4 h-4 text-red-400" />}
                        <span className={cn(
                          log.severity === "Info" && "text-blue-400/80",
                          log.severity === "Warning" && "text-amber-400/80",
                          log.severity === "Error" && "text-red-400/80",
                        )}>{log.severity}</span>
                      </div>
                    </td>
                    <td className="px-4 py-2.5 text-neutral-300 truncate max-w-[200px]">{log.asset}</td>
                    <td className="px-4 py-2.5 text-neutral-400 truncate max-w-xl">{log.message}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      <AnimatePresence>
        {selectedLog && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.15 }}
            className="absolute inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-6"
            onClick={() => setSelectedLog(null)}
          >
            <motion.div
              initial={{ scale: 0.95, opacity: 0, y: 10 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.95, opacity: 0, y: 10 }}
              transition={{ type: "spring", stiffness: 300, damping: 30 }}
              className="bg-[#1a1a1a] border border-[#333] rounded-lg shadow-2xl w-full max-w-2xl flex flex-col max-h-[80vh] overflow-hidden pointer-events-auto"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="h-14 border-b border-[#333] flex items-center justify-between px-6 shrink-0 bg-[#222]">
                <h2 className="text-sm font-semibold text-neutral-200 flex items-center gap-2">
                  {selectedLog.severity === "Info" && <Info className="w-4 h-4 text-blue-400" />}
                  {selectedLog.severity === "Warning" && <AlertTriangle className="w-4 h-4 text-amber-400" />}
                  {selectedLog.severity === "Error" && <XCircle className="w-4 h-4 text-red-400" />}
                  Log Details
                </h2>
                <button
                  onClick={() => setSelectedLog(null)}
                  className="text-neutral-500 hover:text-white transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar">
                <div className="grid grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-2">Timestamp</h3>
                    <div className="text-sm text-neutral-300 font-mono bg-[#111] border border-[#333] px-3 py-2 rounded">{selectedLog.timestamp}</div>
                  </div>
                  <div>
                    <h3 className="text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-2">Asset</h3>
                    <div className="text-sm text-neutral-300 font-mono bg-[#111] border border-[#333] px-3 py-2 rounded truncate">{selectedLog.asset}</div>
                  </div>
                </div>
                <div>
                  <h3 className="text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-2">Message</h3>
                  <div className="text-sm text-neutral-300 font-mono bg-[#111] border border-[#333] p-4 rounded whitespace-pre-wrap leading-relaxed">
                    {selectedLog.message}
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
