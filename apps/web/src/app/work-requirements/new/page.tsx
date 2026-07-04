"use client";

import { useRouter } from "next/navigation";

import { WorkRequirementForm } from "@/components/forms/WorkRequirementForm";
import { Card, ErrorBlock } from "@/components/ui";
import { useCreateWorkRequirement } from "@/lib/hooks/work-requirements";

export default function NewWorkRequirementPage() {
  const router = useRouter();
  const create = useCreateWorkRequirement();

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">New work requirement</h1>
      {create.error && <ErrorBlock error={create.error} />}
      <Card>
        <WorkRequirementForm
          submitLabel="Create"
          submitting={create.isPending}
          onSubmit={async (values) => {
            const { status: _status, ...create_input } = values;
            const created = await create.mutateAsync(create_input);
            router.push(`/work-requirements/${created.id}`);
          }}
        />
      </Card>
    </div>
  );
}
