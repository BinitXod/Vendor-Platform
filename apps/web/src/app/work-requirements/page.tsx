"use client";

import Link from "next/link";

import {
  Button,
  Card,
  EmptyState,
  ErrorBlock,
  LoadingBlock,
  Pill,
} from "@/components/ui";
import {
  useDeleteWorkRequirement,
  useWorkRequirementList,
} from "@/lib/hooks/work-requirements";

function statusTone(s: string) {
  switch (s) {
    case "Open":
      return "blue" as const;
    case "Sourcing":
      return "amber" as const;
    case "Awarded":
      return "green" as const;
    case "Closed":
      return "slate" as const;
    default:
      return "slate" as const;
  }
}
function priorityTone(p: string) {
  if (p === "High") return "red" as const;
  if (p === "Medium") return "amber" as const;
  return "slate" as const;
}

export default function WorkRequirementListPage() {
  const list = useWorkRequirementList();
  const del = useDeleteWorkRequirement();

  async function handleDelete(id: string, title: string) {
    if (!confirm(`Soft-delete "${title}"?`)) return;
    await del.mutateAsync(id);
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Work requirements</h1>
          <p className="text-sm text-slate-500">
            {list.data ? `${list.data.total} record(s)` : " "}
          </p>
        </div>
        <Link href="/work-requirements/new">
          <Button>New requirement</Button>
        </Link>
      </div>

      {list.isLoading && <LoadingBlock />}
      {list.error && <ErrorBlock error={list.error} />}
      {list.data && list.data.items.length === 0 && (
        <EmptyState
          title="No work requirements yet"
          hint="Create one to get vendor recommendations."
        />
      )}

      {list.data && list.data.items.length > 0 && (
        <Card className="overflow-x-auto p-0">
          <table className="min-w-full text-sm">
            <thead className="border-b border-surface-border bg-slate-50 text-left text-xs uppercase text-slate-500">
              <tr>
                <th className="px-4 py-2">Title</th>
                <th className="px-4 py-2">Category</th>
                <th className="px-4 py-2">Location</th>
                <th className="px-4 py-2">Value</th>
                <th className="px-4 py-2">Priority</th>
                <th className="px-4 py-2">Status</th>
                <th className="px-4 py-2 text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              {list.data.items.map((w) => (
                <tr key={w.id} className="border-b border-surface-border last:border-b-0">
                  <td className="px-4 py-2">
                    <div className="font-medium">{w.title}</div>
                    <div className="text-xs text-slate-500">
                      starts {w.expected_start_date}
                    </div>
                  </td>
                  <td className="px-4 py-2">{w.category}</td>
                  <td className="px-4 py-2">{w.location}</td>
                  <td className="px-4 py-2">
                    {w.estimated_value.toLocaleString()}
                  </td>
                  <td className="px-4 py-2">
                    <Pill tone={priorityTone(w.priority)}>{w.priority}</Pill>
                  </td>
                  <td className="px-4 py-2">
                    <Pill tone={statusTone(w.status)}>{w.status}</Pill>
                  </td>
                  <td className="px-4 py-2">
                    <div className="flex justify-end gap-2">
                      <Link href={`/work-requirements/${w.id}`}>
                        <Button variant="secondary">Open</Button>
                      </Link>
                      <Button
                        variant="danger"
                        onClick={() => handleDelete(w.id, w.title)}
                        disabled={del.isPending}
                      >
                        Delete
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      )}
    </div>
  );
}
