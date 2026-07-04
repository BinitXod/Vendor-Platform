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
import { useDeleteVendor, useVendorList } from "@/lib/hooks/vendors";

function statusTone(s: string) {
  if (s === "Active") return "green" as const;
  if (s === "Blacklisted") return "red" as const;
  return "slate" as const;
}

export default function VendorsListPage() {
  const list = useVendorList();
  const del = useDeleteVendor();

  async function handleDelete(id: string, name: string) {
    if (!confirm(`Soft-delete vendor "${name}"? This can be reversed in the DB.`)) return;
    await del.mutateAsync(id);
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Vendors</h1>
          <p className="text-sm text-slate-500">
            {list.data ? `${list.data.total} vendor(s)` : " "}
          </p>
        </div>
        <Link href="/vendors/new">
          <Button>New vendor</Button>
        </Link>
      </div>

      {list.isLoading && <LoadingBlock />}
      {list.error && <ErrorBlock error={list.error} />}
      {list.data && list.data.items.length === 0 && (
        <EmptyState
          title="No vendors yet"
          hint="Create your first vendor to seed the recommendation engine."
        />
      )}

      {list.data && list.data.items.length > 0 && (
        <Card className="overflow-x-auto p-0">
          <table className="min-w-full text-sm">
            <thead className="border-b border-surface-border bg-slate-50 text-left text-xs uppercase text-slate-500">
              <tr>
                <th className="px-4 py-2">Name</th>
                <th className="px-4 py-2">Category</th>
                <th className="px-4 py-2">Location</th>
                <th className="px-4 py-2">Rating</th>
                <th className="px-4 py-2">Status</th>
                <th className="px-4 py-2 text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              {list.data.items.map((v) => (
                <tr key={v.id} className="border-b border-surface-border last:border-b-0">
                  <td className="px-4 py-2">
                    <div className="font-medium text-slate-900">{v.name}</div>
                    <div className="text-xs text-slate-500">{v.contact_email}</div>
                  </td>
                  <td className="px-4 py-2">{v.category}</td>
                  <td className="px-4 py-2">{v.operating_location}</td>
                  <td className="px-4 py-2">{v.rating.toFixed(1)}</td>
                  <td className="px-4 py-2">
                    <Pill tone={statusTone(v.current_status)}>{v.current_status}</Pill>
                  </td>
                  <td className="px-4 py-2">
                    <div className="flex justify-end gap-2">
                      <Link href={`/vendors/${v.id}`}>
                        <Button variant="secondary">Edit</Button>
                      </Link>
                      <Button
                        variant="danger"
                        onClick={() => handleDelete(v.id, v.name)}
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
