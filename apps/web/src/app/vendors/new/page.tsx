"use client";

import { useRouter } from "next/navigation";

import { VendorForm } from "@/components/forms/VendorForm";
import { Card, ErrorBlock } from "@/components/ui";
import { useCreateVendor } from "@/lib/hooks/vendors";

export default function NewVendorPage() {
  const router = useRouter();
  const create = useCreateVendor();

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">New vendor</h1>
      {create.error && <ErrorBlock error={create.error} />}
      <Card>
        <VendorForm
          submitLabel="Create vendor"
          submitting={create.isPending}
          onSubmit={async (values) => {
            const {
              rating: _rating,
              current_status: _status,
              ...create_input
            } = values;
            const created = await create.mutateAsync(create_input);
            router.push(`/vendors/${created.id}`);
          }}
        />
      </Card>
    </div>
  );
}
