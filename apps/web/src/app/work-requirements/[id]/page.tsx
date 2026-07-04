"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";

import { RecommendationsPanel } from "@/components/RecommendationsPanel";
import { WorkRequirementForm } from "@/components/forms/WorkRequirementForm";
import {
  Button,
  Card,
  ErrorBlock,
  LoadingBlock,
  Pill,
} from "@/components/ui";
import {
  useDeleteWorkRequirement,
  useUpdateWorkRequirement,
  useWorkRequirement,
} from "@/lib/hooks/work-requirements";

export default function WorkRequirementDetailPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const id = params?.id ?? "";

  const detail = useWorkRequirement(id);
  const update = useUpdateWorkRequirement(id);
  const del = useDeleteWorkRequirement();

  if (detail.isLoading) return <LoadingBlock />;
  if (detail.error) return <ErrorBlock error={detail.error} />;
  if (!detail.data) return null;
  const w = detail.data;

  async function handleDelete() {
    if (!confirm(`Soft-delete "${w.title}"?`)) return;
    await del.mutateAsync(id);
    router.push("/work-requirements");
  }

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-semibold">{w.title}</h1>
          <div className="mt-1 flex items-center gap-2 text-xs text-slate-500">
            <Pill tone="blue">{w.status}</Pill>
            <span>{w.category}</span>
            <span>· {w.location}</span>
            <span>· starts {w.expected_start_date}</span>
          </div>
        </div>
        <div className="flex gap-2">
          <Link href="/work-requirements">
            <Button variant="secondary">Back</Button>
          </Link>
          <Button variant="danger" onClick={handleDelete} disabled={del.isPending}>
            Delete
          </Button>
        </div>
      </div>

      {update.error && <ErrorBlock error={update.error} />}

      <Card>
        <h2 className="text-sm font-semibold text-slate-700">Details</h2>
        <div className="mt-3">
          <WorkRequirementForm
            initial={w}
            showStatus
            submitLabel="Save changes"
            submitting={update.isPending}
            onSubmit={async (values) => {
              await update.mutateAsync(values);
            }}
          />
        </div>
      </Card>

      <RecommendationsPanel workRequirementId={id} />
    </div>
  );
}
