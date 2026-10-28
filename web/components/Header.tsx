import Link from "next/link";
import { Terminal, Shield, LogIn } from "lucide-react";

export function Header() {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-white/10 bg-[#090a0c]/80 backdrop-blur-md">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6">
        <div className="flex items-center gap-3">
          <Link href="/" className="flex items-center gap-2 group">
            <div className="p-2 rounded-lg bg-[#16181d] border border-white/10 group-hover:border-[#5865f2]/50 transition-colors">
              <Terminal className="w-5 h-5 text-[#5865f2]" />
            </div>
            <span className="font-semibold text-lg tracking-tight text-white flex items-center">
              BotOS
              <span className="text-[#5865f2] animate-pulse ml-0.5">.</span>
            </span>
          </Link>
          <span className="hidden sm:inline-block px-2 py-0.5 text-xs font-mono rounded bg-white/5 text-gray-400 border border-white/5">
            v0.1.0-alpha
          </span>
        </div>

        <div className="flex items-center gap-3">
          <Link
            href="/api/auth/login"
            className="flex items-center gap-2 px-3.5 py-1.5 text-sm font-medium rounded-md bg-[#5865f2] hover:bg-[#4752c4] text-white transition-all shadow-sm shadow-[#5865f2]/20 active:scale-95"
          >
            <LogIn className="w-4 h-4" />
            <span>Discordでログイン</span>
          </Link>
        </div>
      </div>
    </header>
  );
}
