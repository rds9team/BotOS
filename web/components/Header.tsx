import Link from "next/link";
import { ThemeToggle } from "@/components/ThemeToggle";
import { Terminal, LogIn, ChevronDown } from "lucide-react";

export function Header() {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-neutral-200 dark:border-neutral-800/80 bg-white/80 dark:bg-[#090a0c]/80 backdrop-blur-md">
      <div className="flex h-14 items-center justify-between px-4 sm:px-6">
        <div className="flex items-center gap-4">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="p-1.5 rounded-md bg-neutral-100 dark:bg-neutral-800 border border-neutral-200 dark:border-neutral-700">
              <Terminal className="w-4 h-4 text-[#5865f2]" />
            </div>
            <span className="font-semibold text-sm tracking-tight text-neutral-900 dark:text-neutral-100">
              BotOS
            </span>
          </Link>

          <span className="text-neutral-300 dark:text-neutral-700">/</span>

          {/* サーバー選択モック */}
          <button
            type="button"
            className="flex items-center gap-2 px-2.5 py-1 text-xs rounded-md bg-neutral-100 dark:bg-neutral-800/60 border border-neutral-200 dark:border-neutral-700/60 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-800 transition-colors"
          >
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            <span className="font-medium">rds9 Dev Guild</span>
            <ChevronDown className="w-3 h-3 text-neutral-400" />
          </button>
        </div>

        <div className="flex items-center gap-2.5">
          <ThemeToggle />
          <Link
            href="/api/auth/login"
            className="flex items-center gap-2 px-3 py-1.5 text-xs font-medium rounded-md bg-[#5865f2] hover:bg-[#4752c4] text-white transition-colors active:scale-95 shadow-sm shadow-[#5865f2]/20"
          >
            <LogIn className="w-3.5 h-3.5" />
            <span>Discord連携</span>
          </Link>
        </div>
      </div>
    </header>
  );
}
