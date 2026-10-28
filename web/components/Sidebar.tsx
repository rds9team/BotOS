"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, Puzzle, ShieldCheck, Settings, BookOpen } from "lucide-react";

const NAV_ITEMS = [
  { href: "/", label: "ダッシュボード", icon: LayoutDashboard },
  { href: "/plugins", label: "プラグイン", icon: Puzzle },
  { href: "/security", label: "セキュリティ", icon: ShieldCheck },
  { href: "/docs", label: "仕様ドキュメント", icon: BookOpen },
  { href: "/settings", label: "設定", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r border-white/10 bg-[#0c0d10] p-4 flex flex-col justify-between hidden md:flex min-h-[calc(100vh-4rem)]">
      <div className="space-y-4">
        <div className="px-3 py-1">
          <p className="text-xs font-mono uppercase tracking-wider text-gray-500">ナビゲーション</p>
        </div>
        <nav className="space-y-1">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-[#16181d] text-white border border-white/10"
                    : "text-gray-400 hover:text-white hover:bg-white/5"
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? "text-[#5865f2]" : "text-gray-400"}`} />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="p-3 rounded-lg bg-[#111214] border border-white/5 space-y-1.5">
        <p className="text-xs font-semibold text-gray-300">BotOS Core Status</p>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span className="text-xs font-mono text-gray-400">Sandbox: Active</span>
        </div>
      </div>
    </aside>
  );
}
