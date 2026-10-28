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
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-neutral-200 dark:border-neutral-800">
        <div>
          <h1 className="text-xl font-semibold tracking-tight text-neutral-900 dark:text-neutral-100">
            システム概要
          </h1>
          <p className="text-xs text-neutral-500 mt-0.5">
            現在接続中のギルド環境とコマンド実行エンジンの稼働状況
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-md border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800 text-xs font-medium text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
          >
            <RotateCw className="w-3.5 h-3.5" />
            <span>同期</span>
          </button>
          <Link
            href="/commands/new"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-[#5865f2] hover:bg-[#4752c4] text-white text-xs font-medium transition-colors shadow-sm"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>コマンド作成</span>
          </Link>
        </div>
      </div>

      {/* メトリクスバー */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="p-3.5 rounded-lg border border-neutral-200 dark:border-neutral-800/90 bg-white dark:bg-[#111215] space-y-1">
          <div className="flex items-center justify-between text-xs text-neutral-500">
            <span>登録コマンド</span>
            <Terminal className="w-3.5 h-3.5 text-neutral-400" />
          </div>
          <div className="text-xl font-bold font-mono text-neutral-900 dark:text-neutral-100">8</div>
          <div className="text-[11px] text-neutral-500 flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
            <span>同期済み: 8件</span>
          </div>
        </div>

        <div className="p-3.5 rounded-lg border border-neutral-200 dark:border-neutral-800/90 bg-white dark:bg-[#111215] space-y-1">
          <div className="flex items-center justify-between text-xs text-neutral-500">
            <span>有効プラグイン</span>
            <Activity className="w-3.5 h-3.5 text-neutral-400" />
          </div>
          <div className="text-xl font-bold font-mono text-neutral-900 dark:text-neutral-100">3</div>
          <div className="text-[11px] text-neutral-500">標準: 2 / カスタム: 1</div>
        </div>

        <div className="p-3.5 rounded-lg border border-neutral-200 dark:border-neutral-800/90 bg-white dark:bg-[#111215] space-y-1">
          <div className="flex items-center justify-between text-xs text-neutral-500">
            <span>AST検証</span>
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />
          </div>
          <div className="text-xl font-bold font-mono text-emerald-600 dark:text-emerald-400">100%</div>
          <div className="text-[11px] text-neutral-500">全コード静的検査済み</div>
        </div>

        <div className="p-3.5 rounded-lg border border-neutral-200 dark:border-neutral-800/90 bg-white dark:bg-[#111215] space-y-1">
          <div className="flex items-center justify-between text-xs text-neutral-500">
            <span>平均実行レイテンシ</span>
            <Clock className="w-3.5 h-3.5 text-neutral-400" />
          </div>
          <div className="text-xl font-bold font-mono text-neutral-900 dark:text-neutral-100">14ms</div>
          <div className="text-[11px] text-neutral-500">FastAPI & Python 3.14</div>
        </div>
      </div>

      {/* 2カラムレイアウト: コマンド一覧と直近の実行ログ */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* コマンド一覧テーブル */}
        <div className="lg:col-span-2 space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-xs font-mono uppercase tracking-wider text-neutral-500">
              登録スラッシュコマンド
            </h2>
            <Link href="/commands" className="text-xs text-[#5865f2] hover:underline">
              すべて表示
            </Link>
          </div>

          <div className="rounded-lg border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#111215] overflow-hidden">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="border-b border-neutral-200 dark:border-neutral-800 bg-neutral-50/50 dark:bg-neutral-900/40 text-neutral-500 font-mono">
                  <th className="py-2.5 px-3.5 font-normal">コマンド名</th>
                  <th className="py-2.5 px-3.5 font-normal">種別</th>
                  <th className="py-2.5 px-3.5 font-normal">プラグイン</th>
                  <th className="py-2.5 px-3.5 font-normal">状態</th>
                  <th className="py-2.5 px-3.5 font-normal text-right">アクション</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-neutral-200 dark:divide-neutral-800 font-mono">
                <tr className="hover:bg-neutral-50 dark:hover:bg-neutral-900/20 transition-colors">
                  <td className="py-2.5 px-3.5 font-medium text-neutral-900 dark:text-neutral-100">
                    /omikuji
                  </td>
                  <td className="py-2.5 px-3.5 text-neutral-500">標準コマンド</td>
                  <td className="py-2.5 px-3.5 text-neutral-600 dark:text-neutral-400">fortune</td>
                  <td className="py-2.5 px-3.5">
                    <span className="inline-flex items-center gap-1 text-[11px] text-emerald-600 dark:text-emerald-400">
                      <CheckCircle2 className="w-3 h-3" /> 有効
                    </span>
                  </td>
                  <td className="py-2.5 px-3.5 text-right">
                    <button type="button" className="text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-200">
                      <Play className="w-3 h-3 inline" />
                    </button>
                  </td>
                </tr>

                <tr className="hover:bg-neutral-50 dark:hover:bg-neutral-900/20 transition-colors">
                  <td className="py-2.5 px-3.5 font-medium text-neutral-900 dark:text-neutral-100">
                    /dice [sides]
                  </td>
                  <td className="py-2.5 px-3.5 text-neutral-500">標準コマンド</td>
                  <td className="py-2.5 px-3.5 text-neutral-600 dark:text-neutral-400">dice-roller</td>
                  <td className="py-2.5 px-3.5">
                    <span className="inline-flex items-center gap-1 text-[11px] text-emerald-600 dark:text-emerald-400">
                      <CheckCircle2 className="w-3 h-3" /> 有効
                    </span>
                  </td>
                  <td className="py-2.5 px-3.5 text-right">
                    <button type="button" className="text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-200">
                      <Play className="w-3 h-3 inline" />
                    </button>
                  </td>
                </tr>

                <tr className="hover:bg-neutral-50 dark:hover:bg-neutral-900/20 transition-colors">
                  <td className="py-2.5 px-3.5 font-medium text-neutral-900 dark:text-neutral-100">
                    /welcome_config
                  </td>
                  <td className="py-2.5 px-3.5 text-neutral-500">イベント駆動</td>
                  <td className="py-2.5 px-3.5 text-neutral-600 dark:text-neutral-400">welcome-bot</td>
                  <td className="py-2.5 px-3.5">
                    <span className="inline-flex items-center gap-1 text-[11px] text-emerald-600 dark:text-emerald-400">
                      <CheckCircle2 className="w-3 h-3" /> 有効
                    </span>
                  </td>
                  <td className="py-2.5 px-3.5 text-right">
                    <button type="button" className="text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-200">
                      <Play className="w-3 h-3 inline" />
                    </button>
                  </td>
                </tr>

                <tr className="hover:bg-neutral-50 dark:hover:bg-neutral-900/20 transition-colors">
                  <td className="py-2.5 px-3.5 font-medium text-neutral-900 dark:text-neutral-100">
                    /custom_echo
                  </td>
                  <td className="py-2.5 px-3.5 text-neutral-500">スクリプト</td>
                  <td className="py-2.5 px-3.5 text-neutral-600 dark:text-neutral-400">user-script</td>
                  <td className="py-2.5 px-3.5">
                    <span className="inline-flex items-center gap-1 text-[11px] text-amber-600 dark:text-amber-400">
                      <AlertTriangle className="w-3 h-3" /> レビュー中
                    </span>
                  </td>
                  <td className="py-2.5 px-3.5 text-right">
                    <button type="button" className="text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-200">
                      <Play className="w-3 h-3 inline" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* 右カラム: ASTセキュリティ監査ログ */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-xs font-mono uppercase tracking-wider text-neutral-500">
              AST 検査ログ
            </h2>
            <span className="text-[11px] font-mono text-neutral-500">リアルタイム</span>
          </div>

          <div className="rounded-lg border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#111215] p-3.5 space-y-3 font-mono text-[11px]">
            <div className="space-y-1 pb-2.5 border-b border-neutral-100 dark:border-neutral-800/80">
              <div className="flex items-center justify-between text-neutral-500 text-[10px]">
                <span>20:34:12</span>
                <span className="text-emerald-500">PASSED</span>
              </div>
              <div className="text-neutral-800 dark:text-neutral-200">
                plugin:fortune AST validation
              </div>
              <div className="text-neutral-500 text-[10px]">
                Disallowed nodes: 0, Imports: safe
              </div>
            </div>

            <div className="space-y-1 pb-2.5 border-b border-neutral-100 dark:border-neutral-800/80">
              <div className="flex items-center justify-between text-neutral-500 text-[10px]">
                <span>20:31:05</span>
                <span className="text-emerald-500">PASSED</span>
              </div>
              <div className="text-neutral-800 dark:text-neutral-200">
                plugin:dice-roller AST validation
              </div>
              <div className="text-neutral-500 text-[10px]">
                Disallowed nodes: 0, Imports: safe
              </div>
            </div>

            <div className="space-y-1">
              <div className="flex items-center justify-between text-neutral-500 text-[10px]">
                <span>20:28:44</span>
                <span className="text-amber-500">BLOCKED</span>
              </div>
              <div className="text-neutral-800 dark:text-neutral-200">
                sandbox: attempt eval() call
              </div>
              <div className="text-neutral-500 text-[10px]">
                Rule: dangerous_builtin_intercepted
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
