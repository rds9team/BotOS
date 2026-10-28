"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Terminal,
  Puzzle,
  ShieldCheck,
  FileText,
  Sliders,
  HelpCircle,
  ExternalLink,
} from "lucide-react";

const NAV_GROUPS = [
  {
    title: "ワークスペース",
    items: [
      { href: "/", label: "概要", icon: LayoutDashboard },
      { href: "/commands", label: "コマンド管理", icon: Terminal },
      { href: "/plugins", label: "プラグイン", icon: Puzzle },
    ],
  },
  {
    title: "セキュリティ & ログ",
    items: [
      { href: "/sandbox", label: "ASTサンドボックス", icon: ShieldCheck },
      { href: "/audit-logs", label: "監査ログ", icon: FileText },
    ],
  },
  {
    title: "システム",
    items: [
      { href: "/settings", label: "設定", icon: Sliders },
      { href: "/help", label: "ヘルプ", icon: HelpCircle },
    ],
  },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-56 border-r border-neutral-200 dark:border-neutral-800/80 bg-neutral-50/50 dark:bg-[#0c0d10] p-3 flex flex-col justify-between hidden md:flex min-h-[calc(100vh-3.5rem)]">
      <div className="space-y-5">
        {NAV_GROUPS.map((group) => (
          <div key={group.title} className="space-y-1">
            <p className="px-2.5 py-1 text-[11px] font-mono uppercase tracking-wider text-neutral-400 dark:text-neutral-500">
              {group.title}
            </p>
            <nav className="space-y-0.5">
              {group.items.map((item) => {
                const Icon = item.icon;
                const isActive = pathname === item.href;
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`flex items-center gap-2.5 px-2.5 py-1.5 rounded-md text-xs font-medium transition-colors ${
                      isActive
                        ? "bg-neutral-200/80 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 border border-neutral-300/60 dark:border-neutral-700/60"
                        : "text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 hover:bg-neutral-100 dark:hover:bg-neutral-800/40"
                    }`}
                  >
                    <Icon className={`w-3.5 h-3.5 ${isActive ? "text-[#5865f2]" : "text-neutral-400 dark:text-neutral-500"}`} />
                    <span>{item.label}</span>
                  </Link>
                );
              })}
            </nav>
          </div>
        ))}
      </div>

      <div className="pt-3 border-t border-neutral-200 dark:border-neutral-800/80">
        <Link
          href="https://github.com/rds9team/BotOS"
          target="_blank"
          className="flex items-center justify-between px-2.5 py-1.5 text-[11px] text-neutral-400 dark:text-neutral-500 hover:text-neutral-700 dark:hover:text-neutral-300 transition-colors"
        >
          <span>GitHub</span>
          <ExternalLink className="w-3 h-3" />
        </Link>
      </div>
    </aside>
  );
}
