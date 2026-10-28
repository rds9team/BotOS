import Link from "next/link";
import {
  HelpCircle,
  Terminal,
  Puzzle,
  ShieldCheck,
  BookOpen,
  ArrowRight,
} from "lucide-react";

const FAQ_ITEMS = [
  {
    q: "BotOSとは何ですか？",
    a: "Discord BotのコマンドやイベントハンドラーをWeb上で動的に作成・管理できるオープンソースのBot運用プラットフォームです。",
  },
  {
    q: "スラッシュコマンドを追加するには？",
    a: "「コマンド管理」画面から新規作成するか、「プラグイン」画面で配布されている標準プラグインを有効化することで即座にDiscordサーバーへ登録されます。",
  },
  {
    q: "ASTサンドボックスとは何ですか？",
    a: "実行前にPythonコードの構文木（AST）を静的解析し、ファイルシステムへのアクセス、危険な組み込み関数、外部通信などの悪意あるコードを事前に検知・遮断する保護機構です。",
  },
  {
    q: "コマンドがDiscord上に反映されない場合は？",
    a: "ダッシュボード右上の「同期」ボタンを押してDiscord APIへ再登録を行ってください。ギルド単位のコマンドは即時反映されます。",
  },
];

export default function HelpPage() {
  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="pb-3 border-b border-neutral-200 dark:border-neutral-800">
        <h1 className="text-base font-medium tracking-tight text-neutral-900 dark:text-neutral-100">
          ヘルプ & ガイド
        </h1>
      </div>

      {/* ドキュメントリンクカード */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div className="p-3.5 rounded border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#111215] space-y-1.5">
          <div className="flex items-center gap-2 text-xs font-medium text-neutral-900 dark:text-neutral-100">
            <Terminal className="w-3.5 h-3.5 text-[#5865f2]" />
            <span>コマンド作成ガイド</span>
          </div>
          <p className="text-[11px] text-neutral-500 leading-normal">
            引数定義、レスポンス形式、権限設定の仕様
          </p>
        </div>

        <div className="p-3.5 rounded border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#111215] space-y-1.5">
          <div className="flex items-center gap-2 text-xs font-medium text-neutral-900 dark:text-neutral-100">
            <Puzzle className="w-3.5 h-3.5 text-emerald-500" />
            <span>プラグイン仕様</span>
          </div>
          <p className="text-[11px] text-neutral-500 leading-normal">
            マニフェストJSONとPythonハンドラーの構成規約
          </p>
        </div>

        <div className="p-3.5 rounded border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#111215] space-y-1.5">
          <div className="flex items-center gap-2 text-xs font-medium text-neutral-900 dark:text-neutral-100">
            <ShieldCheck className="w-3.5 h-3.5 text-amber-500" />
            <span>セキュリティ規約</span>
          </div>
          <p className="text-[11px] text-neutral-500 leading-normal">
            ASTサンドボックスの制限事項と利用可能モジュール
          </p>
        </div>
      </div>

      {/* FAQ セクション */}
      <section className="space-y-3 pt-2">
        <div className="text-xs font-mono uppercase tracking-wider text-neutral-400 dark:text-neutral-500">
          よくある質問 (FAQ)
        </div>

        <div className="rounded border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#111215] divide-y divide-neutral-100 dark:divide-neutral-800/80 text-xs">
          {FAQ_ITEMS.map((item, idx) => (
            <div key={idx} className="p-3.5 space-y-1">
              <div className="font-medium text-neutral-900 dark:text-neutral-100 flex items-center gap-2">
                <span className="font-mono text-neutral-400 text-[11px]">Q.</span>
                <span>{item.q}</span>
              </div>
              <div className="text-[11px] text-neutral-500 leading-relaxed pl-5">
                {item.a}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* サポートリンク */}
      <div className="p-3.5 rounded border border-neutral-200 dark:border-neutral-800 bg-neutral-50 dark:bg-neutral-900/40 flex items-center justify-between text-xs">
        <span className="text-neutral-600 dark:text-neutral-400">
          問題が解決しない場合は GitHub Issue または Discord コミュニティへお問い合わせください。
        </span>
        <Link
          href="https://github.com/rds9team/BotOS/issues"
          target="_blank"
          className="inline-flex items-center gap-1 font-mono text-[11px] text-[#5865f2] hover:underline"
        >
          <span>Issueを開く</span>
          <ArrowRight className="w-3 h-3" />
        </Link>
      </div>
    </div>
  );
}
