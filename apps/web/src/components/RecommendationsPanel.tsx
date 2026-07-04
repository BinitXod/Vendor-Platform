"use client";

import { useState } from "react";

import {
  Button,
  Card,
  EmptyState,
  ErrorBlock,
  LoadingBlock,
  Pill,
} from "@/components/ui";
import {
  useRecommendations,
  useTriggerReport,
} from "@/lib/hooks/recommendations";
import type { Recommendation, UUID } from "@/lib/types";

function scoreTone(score: number) {
  if (score >= 75) return "green" as const;
  if (score >= 50) return "amber" as const;
  return "red" as const;
}

export function RecommendationsPanel({
  workRequirementId,
}: {
  workRequirementId: UUID;
}) {
  const recs = useRecommendations(workRequirementId);
  const trigger = useTriggerReport();
  const [reportMsg, setReportMsg] = useState<string | null>(null);

  async function handleReport() {
    setReportMsg(null);
    try {
      const res = await trigger.mutateAsync(workRequirementId);
      setReportMsg(res.message);
    } catch {
      // error surfaced below
    }
  }

  return (
    <Card>
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-sm font-semibold text-slate-700">
            AI recommendations
          </h2>
          <p className="text-xs text-slate-500">
            Ranked out of 100 · 40 semantic · 30 rating · 30 budget
          </p>
        </div>
        <Button
          variant="secondary"
          onClick={handleReport}
          disabled={trigger.isPending || !recs.data || recs.data.length === 0}
        >
          {trigger.isPending ? "Queuing…" : "Generate report"}
        </Button>
      </div>

      {reportMsg && (
        <p className="mt-3 rounded-md bg-emerald-50 px-3 py-2 text-xs text-emerald-800">
          {reportMsg} Check <code>apps/backend/reports/{workRequirementId}/</code> for the JSON.
        </p>
      )}
      {trigger.error && (
        <div className="mt-3">
          <ErrorBlock error={trigger.error} />
        </div>
      )}

      <div className="mt-4">
        {recs.isLoading && <LoadingBlock label="Ranking vendors…" />}
        {recs.error && <ErrorBlock error={recs.error} />}
        {recs.data && recs.data.length === 0 && (
          <EmptyState
            title="No candidates found"
            hint="Add an Active vendor whose operating_location matches this work requirement."
          />
        )}
        {recs.data && recs.data.length > 0 && (
          <div className="space-y-3">
            {recs.data.map((r) => (
              <RecommendationRow key={r.vendor_id} rec={r} />
            ))}
          </div>
        )}
      </div>
    </Card>
  );
}

function RecommendationRow({ rec }: { rec: Recommendation }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="rounded-md border border-surface-border p-3">
      <button
        type="button"
        className="flex w-full items-center justify-between text-left"
        onClick={() => setOpen((v) => !v)}
      >
        <div>
          <div className="font-medium">{rec.name}</div>
          <div className="text-xs text-slate-500">
            {rec.category} · {rec.contact_email}
          </div>
        </div>
        <Pill tone={scoreTone(rec.score)}>
          {rec.score.toFixed(1)} / 100
        </Pill>
      </button>
      {open && (
        <dl className="mt-3 grid grid-cols-3 gap-2 text-xs">
          <ScoreCell label="Semantic (40)" value={rec.breakdown.semantic_match_score} />
          <ScoreCell label="Rating (30)" value={rec.breakdown.rating_score} />
          <ScoreCell label="Budget (30)" value={rec.breakdown.budget_score} />
        </dl>
      )}
    </div>
  );
}

function ScoreCell({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded bg-slate-50 p-2">
      <dt className="text-slate-500">{label}</dt>
      <dd className="mt-0.5 font-semibold text-slate-800">{value.toFixed(2)}</dd>
    </div>
  );
}
