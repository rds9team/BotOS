import Link from "next/link";

export function Footer() {
  return (
    <footer className="w-full border-t border-white/10 bg-[#090a0c] py-6 px-4 sm:px-6">
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-gray-500">
        <div>
          <span>&copy; 2026 rds9team / BotOS Project.</span>
        </div>
        <div className="flex items-center gap-4 font-mono">
          <Link href="https://github.com/rds9team/BotOS" target="_blank" className="hover:text-gray-300 transition-colors">
            GitHub
          </Link>
          <span>•</span>
          <Link href="/docs" className="hover:text-gray-300 transition-colors">
            API Docs
          </Link>
        </div>
      </div>
    </footer>
  );
}
