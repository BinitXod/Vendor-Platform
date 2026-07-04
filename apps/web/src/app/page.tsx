"use client";

import Link from "next/link";

import { Card } from "@/components/ui";
import { useVendorList } from "@/lib/hooks/vendors";
import { useWorkRequirementList } from "@/lib/hooks/work-requirements";

export default function DashboardPage() {
  const vendors = useVendorList(0, 1);
  const work = useWorkRequirementList(0, 1);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Dashboard</h1>
        <p className="text-sm text-slate-500">
          Quick overview of the vendor recommendation platform.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Link href="/vendors" className="block">
          <Card className="transition hover:border-slate-400">
            <p className="text-xs uppercase tracking-wide text-slate-500">
              Vendors
            </p>
            <p className="mt-2 text-3xl font-semibold">
              {vendors.isLoading ? "…" : vendors.data?.total ?? 0}
            </p>
            <p className="mt-1 text-xs text-slate-500">Manage vendor list →</p>
          </Card>
        </Link>

        <Link href="/work-requirements" className="block">
          <Card className="transition hover:border-slate-400">
            <p className="text-xs uppercase tracking-wide text-slate-500">
              Work requirements
            </p>
            <p className="mt-2 text-3xl font-semibold">
              {work.isLoading ? "…" : work.data?.total ?? 0}
            </p>
            <p className="mt-1 text-xs text-slate-500">
              View, edit, get recommendations →
            </p>
          </Card>
        </Link>
      </div>

      <Card>
        <h2 className="text-sm font-semibold text-slate-700">Getting started</h2>
        <ol className="mt-3 list-decimal space-y-1 pl-5 text-sm text-slate-600">
          <li>
            Create a few <Link className="underline" href="/vendors">vendors</Link> so
            the recommendation engine has candidates.
          </li>
          <li>
            Create a{" "}
            <Link className="underline" href="/work-requirements">
              work requirement
            </Link>{" "}
            with a matching location.
          </li>
          <li>Open the work requirement to see ranked recommendations and trigger the AI report.</li>
        </ol>
      </Card>
    </div>
  );
}
