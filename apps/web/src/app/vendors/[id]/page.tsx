"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";

import { VendorForm } from "@/components/forms/VendorForm";
import {
  Button,
  Card,
  ErrorBlock,
  LoadingBlock,
  Pill,
} from "@/components/ui";
import {
  useDeleteVendor,
  useUpdateVendor,
  useVendor,
} from "@/lib/hooks/vendors";
import type { VendorUpdate } from "@/lib/types";

export default function VendorEditPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const id = params?.id ?? "";

  const detail = useVendor(id);
  const update = useUpdateVendor(id);
  const del = useDeleteVendor();

  if (detail.isLoading) return <LoadingBlock />;
  if (detail.error) return <ErrorBlock error={detail.error} />;
  if (!detail.data) return null;
  const vendor = detail.data;

  async function handleDelete() {
    if (!confirm(`Soft-delete "${vendor.name}"?`)) return;
    await del.mutateAsync(id);
    router.push("/vendors");
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">{vendor.name}</h1>
          <div className="mt-1 flex items-center gap-2 text-xs text-slate-500">
            <Pill tone={vendor.current_status === "Active" ? "green" : "slate"}>
              {vendor.current_status}
            </Pill>
            <span>{vendor.category}</span>
            <span>· {vendor.operating_location}</span>
          </div>
        </div>
        <div className="flex gap-2">
          <Link href="/vendors">
            <Button variant="secondary">Back</Button>
          </Link>
          <Button variant="danger" onClick={handleDelete} disabled={del.isPending}>
            Delete
          </Button>
        </div>
      </div>

      {update.error && <ErrorBlock error={update.error} />}

      <Card>
        <VendorForm
          initial={vendor}
          disableEmail
          showStatusFields
          submitLabel="Save changes"
          submitting={update.isPending}
          onSubmit={async (values) => {
            const patch: VendorUpdate = {
              name: values.name,
              rating: values.rating,
              current_status: values.current_status,
              max_budget_capacity: values.max_budget_capacity ?? null,
              capabilities_description: values.capabilities_description ?? null,
            };
            await update.mutateAsync(patch);
          }}
        />
      </Card>

      <Card>
        <h2 className="text-sm font-semibold text-slate-700">Documents</h2>
        {vendor.documents.length === 0 ? (
          <p className="mt-2 text-sm text-slate-500">No documents uploaded.</p>
        ) : (
          <ul className="mt-2 space-y-1 text-sm">
            {vendor.documents.map((d) => (
              <li key={d.id} className="flex items-center justify-between">
                <span>
                  <span className="font-medium">{d.document_type}</span>
                  <span className="ml-2 text-slate-500">{d.file_path}</span>
                </span>
                <Pill tone={d.verification_status === "Verified" ? "green" : "amber"}>
                  {d.verification_status}
                </Pill>
              </li>
            ))}
          </ul>
        )}
      </Card>
    </div>
  );
}
