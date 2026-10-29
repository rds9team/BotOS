import Link from "next/link";
import { ArrowUpRight } from "lucide-react";

const FAQ_ITEMS = [
  {
    q: "BotOSとは何ですか？",
    a: "Discord BotのコマンドやプラグインをWeb上で作成・管理できる運用基盤です。",
  },
  {
    q: "スラッシュコマンドを追加するには？",
    a: "コマンド管理画面から作成するか、プラグインを有効化するとDiscordサーバーへ自動登録されます。",
  },
  {
    q: "ASTサンドボックスとは何ですか？",
    a: "Pythonコードの構文木（AST）を静的解析し、ファイルアクセスや危険な組み込み関数の実行を事前に遮断する仕組みです。",
  },
  {
    q: "コマンドが反映されない場合は？",
    a: "ダッシュボードの「同期」ボタンを押してDiscord APIへ再登録を行ってください。",
  },
];

export default function HelpPage() {
  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="pb-3 border-b border-neutral-200 dark:border-neutral-800">
        <h1 className="text-base font-medium tracking-tight text-neutral-900 dark:text-neutral-100">
          ヘルプ
        </h1>
      </div>

      {/* ドキュメントリンク（クリーンで統一感のあるデザイン） */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <Link
          href="https://github.com/rds9team/BotOS/tree/main/docs"
          target="_blank"
          className="group p-3.5 rounded-lg border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#111215] hover:border-neutral-300 dark:hover:border-neutral-700 transition-colors"
        >
          <div className="flex items-center justify-between text-xs font-medium text-neutral-900 dark:text-neutral-100">
            <span>コマンド作成</span>
            <ArrowUpRight className="w-3.5 h-3.5 text-neutral-400 group-hover:text-neutral-900 dark:group-hover:text-neutral-100 transition-colors" />
          </div>
          <p className="mt-1 text-[11px] text-neutral-500 leading-normal">
            引数とレスポンス仕様
          </p>
        </Link>

        <Link
          href="https://github.com/rds9team/BotOS/blob/main/docs/spec.md"
          target="_blank"
          className="group p-3.5 rounded-lg border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#111215] hover:border-neutral-300 dark:hover:border-neutral-700 transition-colors"
        >
          <div className="flex items-center justify-between text-xs font-medium text-neutral-900 dark:text-neutral-100">
            <span>プラグイン仕様</span>
            <ArrowUpRight className="w-3.5 h-3.5 text-neutral-400 group-hover:text-neutral-900 dark:group-hover:text-neutral-100 transition-colors" />
          </div>
          <p className="mt-1 text-[11px] text-neutral-500 leading-normal">
            マニフェスト構成規約
          </p>
        </Link>

        <Link
          href="https://github.com/rds9team/BotOS/blob/main/docs/architecture.md"
          target="_blank"
          className="group p-3.5 rounded-lg border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#111215] hover:border-neutral-300 dark:hover:border-neutral-700 transition-colors"
        >
          <div className="flex items-center justify-between text-xs font-medium text-neutral-900 dark:text-neutral-100">
            <span>セキュリティ規約</span>
            <ArrowUpRight className="w-3.5 h-3.5 text-neutral-400 group-hover:text-neutral-900 dark:group-hover:text-neutral-100 transition-colors" />
          </div>
          <p className="mt-1 text-[11px] text-neutral-500 leading-normal">
            AST制限事項一覧
          </p>
        </Link>
      </div>

      {/* FAQ セクション */}
      <section className="space-y-3">
        <h2 className="text-xs font-mono uppercase tracking-wider text-neutral-400 dark:text-neutral-500">
          よくある質問
        </h2>

        <div className="rounded-lg border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#111215] divide-y divide-neutral-100 dark:divide-neutral-800/80 text-xs">
          {FAQ_ITEMS.map((item, idx) => (
            <div key={idx} className="p-4 space-y-1">
              <div className="font-medium text-neutral-900 dark:text-neutral-100">
                {item.q}
              </div>
              <p className="text-[11px] text-neutral-500 leading-relaxed">
                {item.a}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* サポートリンク */}
      <div className="p-3.5 rounded-lg border border-neutral-200 dark:border-neutral-800 bg-neutral-50/60 dark:bg-neutral-900/30 flex items-center justify-between text-xs">
        <span className="text-neutral-500">
          問題が解決しない場合
        </span>
        <Link
          href="https://github.com/rds9team/BotOS/issues"
          target="_blank"
          className="inline-flex items-center gap-1 font-mono text-[11px] text-[#5865f2] hover:underline"
        >
          <span>Issueを開く</span>
          <ArrowUpRight className="w-3 h-3" />
        </Link>
      </div>
    </div>
  );
}
