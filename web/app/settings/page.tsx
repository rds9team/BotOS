"use client";

import { useState } from "react";
import { Check } from "lucide-react";

export default function SettingsPage() {
  const [autoSync, setAutoSync] = useState(true);
  const [auditLogNotification, setAuditLogNotification] = useState(false);
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="flex items-center justify-between pb-3 border-b border-neutral-200 dark:border-neutral-800">
        <div>
          <h1 className="text-base font-medium tracking-tight text-neutral-900 dark:text-neutral-100">
            設定
          </h1>
        </div>

        <button
          type="button"
          onClick={handleSave}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded bg-[#5865f2] hover:bg-[#4752c4] text-white text-xs font-medium transition-colors shadow-sm"
        >
          {saved ? (
            <>
              <Check className="w-3.5 h-3.5" />
              <span>保存完了</span>
            </>
          ) : (
            <span>変更を保存</span>
          )}
        </button>
      </div>

      <div className="space-y-4">
        {/* コマンド同期設定 */}
        <div className="rounded-lg border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-[#111215] divide-y divide-neutral-100 dark:divide-neutral-800/80 text-xs">
          <label className="flex items-start justify-between p-4 cursor-pointer gap-4">
            <div className="space-y-0.5">
              <span className="font-medium text-neutral-900 dark:text-neutral-100 block">
                コマンド自動同期
              </span>
              <span className="text-[11px] text-neutral-500 block leading-relaxed">
                プラグイン作成や更新時にDiscordスラッシュコマンドを自動で同期します。
              </span>
            </div>
            <input
              type="checkbox"
              checked={autoSync}
              onChange={(e) => setAutoSync(e.target.checked)}
              className="mt-0.5 rounded border-neutral-300 dark:border-neutral-700 text-[#5865f2] focus:ring-[#5865f2] h-4 w-4 cursor-pointer"
            />
          </label>

          <label className="flex items-start justify-between p-4 cursor-pointer gap-4">
            <div className="space-y-0.5">
              <span className="font-medium text-neutral-900 dark:text-neutral-100 block">
                セキュリティ警告の通知
              </span>
              <span className="text-[11px] text-neutral-500 block leading-relaxed">
                サンドボックスによる危険構文の遮断や権限昇格の試行を検知した際にログチャンネルへ通知します。
              </span>
            </div>
            <input
              type="checkbox"
              checked={auditLogNotification}
              onChange={(e) => setAuditLogNotification(e.target.checked)}
              className="mt-0.5 rounded border-neutral-300 dark:border-neutral-700 text-[#5865f2] focus:ring-[#5865f2] h-4 w-4 cursor-pointer"
            />
          </label>
        </div>
      </div>
    </div>
  );
}
