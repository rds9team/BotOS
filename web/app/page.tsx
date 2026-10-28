import Link from "next/link";
import {
  Terminal,
  Activity,
  ShieldCheck,
  Plus,
  Play,
  RotateCw,
  Clock,
  CheckCircle2,
  AlertTriangle,
} from "lucide-react";

export default function Home() {
  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* ページタイトル & アクション */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-neutral-200 dark:border-neutral-800">
        <div>
          <h1 className="text-base font-medium tracking-tight text-neutral-900 dark:text-neutral-100">
            ダッシュボード
          </h1>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            className="flex items-center gap-1 px-2.5 py-1 rounded border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800 text-xs text-neutral-600 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-neutral-700 transition-colors"
          >
            <RotateCw className="w-3 h-3 text-neutral-400" />
            <span>同期</span>
          </button>
          <Link
            href="/commands/new"
            className="flex items-center gap-1 px-2.5 py-1 rounded bg-[#5865f2] hover:bg-[#4752c4] text-white text-xs font-medium transition-colors shadow-sm"
          >
            <Plus className="w-3 h-3" />
            <span>新規コマンド</span>
          </Link>
        </div>
      </div>

      {/* メトリクスバー（コンパクト・ミニマル） */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="p-3 rounded border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#111215]">
          <div className="flex items-center justify-between text-[11px] text-neutral-500">
            <span>コマンド</span>
            <Terminal className="w-3.5 h-3.5 text-neutral-400" />
          </div>
          <div className="mt-1 text-lg font-semibold font-mono text-neutral-900 dark:text-neutral-100">8</div>
        </div>

        <div className="p-3 rounded border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#111215]">
          <div className="flex items-center justify-between text-[11px] text-neutral-500">
            <span>プラグイン</span>
            <Activity className="w-3.5 h-3.5 text-neutral-400" />
          </div>
          <div className="mt-1 text-lg font-semibold font-mono text-neutral-900 dark:text-neutral-100">3</div>
        </div>

        <div className="p-3 rounded border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#111215]">
          <div className="flex items-center justify-between text-[11px] text-neutral-500">
            <span>AST検査</span>
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />
          </div>
          <div className="mt-1 text-lg font-semibold font-mono text-emerald-600 dark:text-emerald-400">通過</div>
        </div>

        <div className="p-3 rounded border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#111215]">
          <div className="flex items-center justify-between text-[11px] text-neutral-500">
            <span>平均応答</span>
            <Clock className="w-3.5 h-3.5 text-neutral-400" />
          </div>
          <div className="mt-1 text-lg font-semibold font-mono text-neutral-900 dark:text-neutral-100">14ms</div>
        </div>
      </div>

      {/* 2カラムレイアウト: コマンド一覧と直近の実行ログ */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* コマンド一覧テーブル */}
        <div className="lg:col-span-2 space-y-2">
          <div className="flex items-center justify-between">
            <h2 className="text-[11px] font-mono uppercase tracking-wider text-neutral-400 dark:text-neutral-500">
              スラッシュコマンド
            </h2>
            <Link href="/commands" className="text-[11px] text-[#5865f2] hover:underline">
              一覧
            </Link>
          </div>

          <div className="rounded border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#111215] overflow-hidden">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="border-b border-neutral-200 dark:border-neutral-800 bg-neutral-50/50 dark:bg-neutral-900/30 text-neutral-400 font-mono text-[11px]">
                  <th className="py-2 px-3 font-normal">コマンド</th>
                  <th className="py-2 px-3 font-normal">プラグイン</th>
                  <th className="py-2 px-3 font-normal">状態</th>
                  <th className="py-2 px-3 font-normal text-right">実行</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-neutral-200 dark:divide-neutral-800 font-mono text-xs">
                <tr className="hover:bg-neutral-50 dark:hover:bg-neutral-900/20 transition-colors">
                  <td className="py-2 px-3 text-neutral-900 dark:text-neutral-100">/omikuji</td>
                  <td className="py-2 px-3 text-neutral-500 text-[11px]">fortune</td>
                  <td className="py-2 px-3">
                    <span className="inline-flex items-center gap-1 text-[11px] text-emerald-600 dark:text-emerald-400">
                      <CheckCircle2 className="w-3 h-3" /> 有効
                    </span>
                  </td>
                  <td className="py-2 px-3 text-right">
                    <button type="button" className="text-neutral-400 hover:text-neutral-600 dark:hover:text-neutral-200">
                      <Play className="w-3 h-3 inline" />
                    </button>
                  </td>
                </tr>

                <tr className="hover:bg-neutral-50 dark:hover:bg-neutral-900/20 transition-colors">
                  <td className="py-2 px-3 text-neutral-900 dark:text-neutral-100">/dice</td>
                  <td className="py-2 px-3 text-neutral-500 text-[11px]">dice-roller</td>
                  <td className="py-2 px-3">
                    <span className="inline-flex items-center gap-1 text-[11px] text-emerald-600 dark:text-emerald-400">
                      <CheckCircle2 className="w-3 h-3" /> 有効
                    </span>
                  </td>
                  <td className="py-2 px-3 text-right">
                    <button type="button" className="text-neutral-400 hover:text-neutral-600 dark:hover:text-neutral-200">
                      <Play className="w-3 h-3 inline" />
                    </button>
                  </td>
                </tr>

                <tr className="hover:bg-neutral-50 dark:hover:bg-neutral-900/20 transition-colors">
                  <td className="py-2 px-3 text-neutral-900 dark:text-neutral-100">/welcome_config</td>
                  <td className="py-2 px-3 text-neutral-500 text-[11px]">welcome-bot</td>
                  <td className="py-2 px-3">
                    <span className="inline-flex items-center gap-1 text-[11px] text-emerald-600 dark:text-emerald-400">
                      <CheckCircle2 className="w-3 h-3" /> 有効
                    </span>
                  </td>
                  <td className="py-2 px-3 text-right">
                    <button type="button" className="text-neutral-400 hover:text-neutral-600 dark:hover:text-neutral-200">
                      <Play className="w-3 h-3 inline" />
                    </button>
                  </td>
                </tr>

                <tr className="hover:bg-neutral-50 dark:hover:bg-neutral-900/20 transition-colors">
                  <td className="py-2 px-3 text-neutral-900 dark:text-neutral-100">/custom_echo</td>
                  <td className="py-2 px-3 text-neutral-500 text-[11px]">user-script</td>
                  <td className="py-2 px-3">
                    <span className="inline-flex items-center gap-1 text-[11px] text-amber-600 dark:text-amber-400">
                      <AlertTriangle className="w-3 h-3" /> 審査中
                    </span>
                  </td>
                  <td className="py-2 px-3 text-right">
                    <button type="button" className="text-neutral-400 hover:text-neutral-600 dark:hover:text-neutral-200">
                      <Play className="w-3 h-3 inline" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* 右カラム: ASTセキュリティ監査ログ */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <h2 className="text-[11px] font-mono uppercase tracking-wider text-neutral-400 dark:text-neutral-500">
              AST 検査ログ
            </h2>
            <span className="text-[10px] font-mono text-neutral-400">リアルタイム</span>
          </div>

          <div className="rounded border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#111215] p-3 space-y-2 font-mono text-xs">
            <div className="space-y-0.5 pb-2 border-b border-neutral-100 dark:border-neutral-800/80">
              <div className="flex items-center justify-between text-[10px] text-neutral-400">
                <span>20:34:12</span>
                <span className="text-emerald-500">PASSED</span>
              </div>
              <div className="text-neutral-800 dark:text-neutral-200 text-xs">
                plugin:fortune
              </div>
            </div>

            <div className="space-y-0.5 pb-2 border-b border-neutral-100 dark:border-neutral-800/80">
              <div className="flex items-center justify-between text-[10px] text-neutral-400">
                <span>20:31:05</span>
                <span className="text-emerald-500">PASSED</span>
              </div>
              <div className="text-neutral-800 dark:text-neutral-200 text-xs">
                plugin:dice-roller
              </div>
            </div>

            <div className="space-y-0.5">
              <div className="flex items-center justify-between text-[10px] text-neutral-400">
                <span>20:28:44</span>
                <span className="text-amber-500">BLOCKED</span>
              </div>
              <div className="text-neutral-800 dark:text-neutral-200 text-xs">
                attempt eval() call
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
