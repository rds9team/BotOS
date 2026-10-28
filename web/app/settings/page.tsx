import Link from "next/link";
import {
  Cpu,
  ShieldCheck,
  Server,
  Code2,
  Database,
  Info,
  Sliders,
  Bell,
  Lock,
} from "lucide-react";

export default function SettingsPage() {
  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="pb-3 border-b border-neutral-200 dark:border-neutral-800">
        <h1 className="text-base font-medium tracking-tight text-neutral-900 dark:text-neutral-100">
          設定
        </h1>
      </div>

      {/* サーバー一般設定 */}
      <section className="space-y-3">
        <div className="text-xs font-mono uppercase tracking-wider text-neutral-400 dark:text-neutral-500">
          全般設定
        </div>

        <div className="rounded border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#111215] divide-y divide-neutral-100 dark:divide-neutral-800/80 text-xs">
          <div className="flex items-center justify-between p-3.5">
            <div className="space-y-0.5">
              <div className="font-medium text-neutral-900 dark:text-neutral-100">コマンド自動同期</div>
              <div className="text-[11px] text-neutral-500">プラグイン追加・編集時にDiscordのスラッシュコマンドを自動登録します</div>
            </div>
            <input
              type="checkbox"
              defaultChecked
              className="rounded border-neutral-300 dark:border-neutral-700 text-[#5865f2] focus:ring-[#5865f2] h-4 w-4"
            />
          </div>

          <div className="flex items-center justify-between p-3.5">
            <div className="space-y-0.5">
              <div className="font-medium text-neutral-900 dark:text-neutral-100">サンドボックス強制モード</div>
              <div className="text-[11px] text-neutral-500">AST検証を通過しないコードの実行を即時遮断します</div>
            </div>
            <input
              type="checkbox"
              defaultChecked
              disabled
              className="rounded border-neutral-300 dark:border-neutral-700 text-emerald-500 h-4 w-4 opacity-80 cursor-not-allowed"
            />
          </div>
        </div>
      </section>

      {/* 詳細 (Technical Details) */}
      <section className="space-y-3 pt-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-wider text-neutral-400 dark:text-neutral-500">
            <Info className="w-3.5 h-3.5" />
            <span>詳細（ランタイム・システム環境）</span>
          </div>
          <span className="text-[11px] font-mono text-neutral-400">システム情報</span>
        </div>

        <div className="rounded border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#111215] divide-y divide-neutral-100 dark:divide-neutral-800/80 font-mono text-xs">
          <div className="flex items-center justify-between p-3">
            <div className="flex items-center gap-2.5 text-neutral-600 dark:text-neutral-400">
              <Cpu className="w-4 h-4 text-neutral-400" />
              <span>実行エンジン</span>
            </div>
            <div className="text-right text-neutral-900 dark:text-neutral-200">
              BotOS Core v0.1.0-alpha
            </div>
          </div>

          <div className="flex items-center justify-between p-3">
            <div className="flex items-center gap-2.5 text-neutral-600 dark:text-neutral-400">
              <Code2 className="w-4 h-4 text-neutral-400" />
              <span>Python ランタイム</span>
            </div>
            <div className="text-right text-neutral-900 dark:text-neutral-200">
              Python 3.14 (AsyncIO / FastAPI)
            </div>
          </div>

          <div className="flex items-center justify-between p-3">
            <div className="flex items-center gap-2.5 text-neutral-600 dark:text-neutral-400">
              <ShieldCheck className="w-4 h-4 text-emerald-500" />
              <span>AST サンドボックス Guard</span>
            </div>
            <div className="text-right flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
              <span>Enforced (AST Verification)</span>
            </div>
          </div>

          <div className="flex items-center justify-between p-3">
            <div className="flex items-center gap-2.5 text-neutral-600 dark:text-neutral-400">
              <Server className="w-4 h-4 text-neutral-400" />
              <span>API ゲートウェイ</span>
            </div>
            <div className="text-right text-neutral-500">
              http://localhost:8000
            </div>
          </div>

          <div className="flex items-center justify-between p-3">
            <div className="flex items-center gap-2.5 text-neutral-600 dark:text-neutral-400">
              <Database className="w-4 h-4 text-neutral-400" />
              <span>ストレージ層</span>
            </div>
            <div className="text-right text-neutral-500">
              SQLite (WAL Mode) / JSON Schema
            </div>
          </div>
        </div>
      </section>

      {/* サンドボックス規約 */}
      <section className="space-y-3 pt-2">
        <div className="text-xs font-mono uppercase tracking-wider text-neutral-400 dark:text-neutral-500">
          詳細（AST 実行セキュリティ規約）
        </div>

        <div className="p-3.5 rounded border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#111215] space-y-2 text-xs text-neutral-600 dark:text-neutral-400 leading-relaxed font-mono">
          <div className="flex items-start gap-2">
            <span className="text-[#5865f2]">•</span>
            <span>禁止ノード: <code className="px-1 py-0.5 rounded bg-neutral-100 dark:bg-neutral-800 text-neutral-800 dark:text-neutral-200">Import</code>, <code className="px-1 py-0.5 rounded bg-neutral-100 dark:bg-neutral-800 text-neutral-800 dark:text-neutral-200">ImportFrom</code>, <code className="px-1 py-0.5 rounded bg-neutral-100 dark:bg-neutral-800 text-neutral-800 dark:text-neutral-200">Exec</code>, <code className="px-1 py-0.5 rounded bg-neutral-100 dark:bg-neutral-800 text-neutral-800 dark:text-neutral-200">Global</code></span>
          </div>
          <div className="flex items-start gap-2">
            <span className="text-[#5865f2]">•</span>
            <span>遮断属性: <code className="px-1 py-0.5 rounded bg-neutral-100 dark:bg-neutral-800 text-neutral-800 dark:text-neutral-200">__builtins__</code>, <code className="px-1 py-0.5 rounded bg-neutral-100 dark:bg-neutral-800 text-neutral-800 dark:text-neutral-200">__class__</code>, <code className="px-1 py-0.5 rounded bg-neutral-100 dark:bg-neutral-800 text-neutral-800 dark:text-neutral-200">__subclasses__</code></span>
          </div>
          <div className="flex items-start gap-2">
            <span className="text-[#5865f2]">•</span>
            <span>実行タイムアウト: 500ms（無限ループ防止）</span>
          </div>
        </div>
      </section>
    </div>
  );
}
