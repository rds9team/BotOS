import Link from "next/link";
import { Server, Cpu, Shield, ArrowRight, Code, Sparkles } from "lucide-react";

export default function Home() {
  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* ヒーローセクション */}
      <section className="relative overflow-hidden rounded-2xl border border-white/10 bg-[#111214] p-8 md:p-12">
        <div className="absolute top-0 right-0 -mt-12 -mr-12 w-96 h-96 bg-[#5865f2]/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 space-y-4 max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs font-mono text-gray-300">
            <Sparkles className="w-3.5 h-3.5 text-[#5865f2]" />
            <span>次世代プラグイン型 Discord Bot プラットフォーム</span>
          </div>
          <h1 className="text-3xl md:text-5xl font-bold tracking-tight text-white">
            BotOS <span className="text-[#5865f2]">Dashboard</span>
          </h1>
          <p className="text-gray-400 text-sm md:text-base leading-relaxed">
            安全なASTサンドボックスとWeb UIで、Discord Botのコマンド・イベントを動的に作成・管理できる統合コントロールパネルです。
          </p>
          <div className="pt-2 flex flex-wrap gap-3">
            <Link
              href="/servers"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[#5865f2] hover:bg-[#4752c4] text-white text-sm font-medium transition-all shadow-lg shadow-[#5865f2]/20 active:scale-95"
            >
              <Server className="w-4 h-4" />
              <span>管理サーバーを選択</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
            <Link
              href="/plugins"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[#16181d] hover:bg-white/5 border border-white/10 text-gray-300 hover:text-white text-sm font-medium transition-all"
            >
              <Code className="w-4 h-4" />
              <span>プラグイン一覧を見る</span>
            </Link>
          </div>
        </div>
      </section>

      {/* ステータスカードグリッド */}
      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div className="p-6 rounded-xl border border-white/10 bg-[#111214] space-y-2">
          <div className="flex items-center justify-between text-gray-400">
            <span className="text-sm font-medium">参加サーバー数</span>
            <Server className="w-5 h-5 text-gray-500" />
          </div>
          <p className="text-2xl font-bold text-white font-mono">--</p>
          <p className="text-xs text-gray-500">ログイン後に同期されます</p>
        </div>

        <div className="p-6 rounded-xl border border-white/10 bg-[#111214] space-y-2">
          <div className="flex items-center justify-between text-gray-400">
            <span className="text-sm font-medium">有効プラグイン</span>
            <Cpu className="w-5 h-5 text-gray-500" />
          </div>
          <p className="text-2xl font-bold text-white font-mono">0</p>
          <p className="text-xs text-gray-500">標準コマンドプラグイン利用可能</p>
        </div>

        <div className="p-6 rounded-xl border border-white/10 bg-[#111214] space-y-2">
          <div className="flex items-center justify-between text-gray-400">
            <span className="text-sm font-medium">サンドボックス保護</span>
            <Shield className="w-5 h-5 text-emerald-500" />
          </div>
          <p className="text-2xl font-bold text-emerald-400 font-mono">AST Shield</p>
          <p className="text-xs text-gray-500">危険な組み込み関数・属性アクセスを遮断</p>
        </div>
      </section>

      {/* クイックガイドセクション */}
      <section className="rounded-xl border border-white/10 bg-[#111214] p-6 space-y-4">
        <h2 className="text-lg font-semibold text-white">クイックスタート</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div className="p-4 rounded-lg bg-[#16181d] border border-white/5 space-y-2">
            <div className="font-mono text-xs text-[#5865f2]">STEP 01</div>
            <div className="font-medium text-white">Discord 認証</div>
            <p className="text-xs text-gray-400">
              右上のログインボタンから Discord アカウントで認証し、管理権限を持つサーバーを読み込みます。
            </p>
          </div>
          <div className="p-4 rounded-lg bg-[#16181d] border border-white/5 space-y-2">
            <div className="font-mono text-xs text-[#5865f2]">STEP 02</div>
            <div className="font-medium text-white">サーバー設定</div>
            <p className="text-xs text-gray-400">
              BotOS を導入したいサーバーを選択し、使用するプラグインやコマンドの有効/無効を切り替えます。
            </p>
          </div>
          <div className="p-4 rounded-lg bg-[#16181d] border border-white/5 space-y-2">
            <div className="font-mono text-xs text-[#5865f2]">STEP 03</div>
            <div className="font-medium text-white">カスタム拡張</div>
            <p className="text-xs text-gray-400">
              AST サンドボックス上で動作する Python プラグインを作成し、サーバー専用の機能を即時デプロイできます。
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
