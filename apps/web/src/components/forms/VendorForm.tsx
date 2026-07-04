"use client";

import { useState, type FormEvent } from "react";

import { Button, Field, Input, Select, Textarea } from "@/components/ui";
import type { VendorCreate } from "@/lib/types";

export type VendorFormValues = VendorCreate & {
  rating?: number;
  current_status?: string;
};

type Props = {
  initial?: Partial<VendorFormValues>;
  onSubmit: (values: VendorFormValues) => Promise<unknown> | void;
  submitLabel?: string;
  submitting?: boolean;
  showStatusFields?: boolean;
  disableEmail?: boolean;
};

export function VendorForm({
  initial,
  onSubmit,
  submitLabel = "Save",
  submitting,
  showStatusFields = false,
  disableEmail = false,
}: Props) {
  const [values, setValues] = useState<VendorFormValues>({
    name: initial?.name ?? "",
    vendor_type: initial?.vendor_type ?? "Contractor",
    category: initial?.category ?? "",
    contact_email: initial?.contact_email ?? "",
    contact_phone: initial?.contact_phone ?? "",
    operating_location: initial?.operating_location ?? "",
    max_budget_capacity: initial?.max_budget_capacity ?? null,
    capabilities_description: initial?.capabilities_description ?? "",
    rating: initial?.rating,
    current_status: initial?.current_status ?? "Active",
  });

  function set<K extends keyof VendorFormValues>(key: K, v: VendorFormValues[K]) {
    setValues((prev) => ({ ...prev, [key]: v }));
  }

  async function handle(e: FormEvent) {
    e.preventDefault();
    await onSubmit(values);
  }

  return (
    <form onSubmit={handle} className="space-y-4">
      <div className="grid gap-4 md:grid-cols-2">
        <Field label="Name" htmlFor="name">
          <Input
            id="name"
            required
            value={values.name}
            onChange={(e) => set("name", e.target.value)}
          />
        </Field>
        <Field label="Vendor type" htmlFor="vendor_type">
          <Input
            id="vendor_type"
            required
            value={values.vendor_type}
            onChange={(e) => set("vendor_type", e.target.value)}
          />
        </Field>
        <Field label="Category" htmlFor="category">
          <Input
            id="category"
            required
            value={values.category}
            onChange={(e) => set("category", e.target.value)}
          />
        </Field>
        <Field label="Operating location" htmlFor="operating_location">
          <Input
            id="operating_location"
            required
            value={values.operating_location}
            onChange={(e) => set("operating_location", e.target.value)}
          />
        </Field>
        <Field label="Contact email" htmlFor="contact_email">
          <Input
            id="contact_email"
            type="email"
            required
            disabled={disableEmail}
            value={values.contact_email}
            onChange={(e) => set("contact_email", e.target.value)}
          />
        </Field>
        <Field label="Contact phone" htmlFor="contact_phone">
          <Input
            id="contact_phone"
            value={values.contact_phone ?? ""}
            onChange={(e) => set("contact_phone", e.target.value)}
          />
        </Field>
        <Field label="Max budget capacity" htmlFor="max_budget_capacity">
          <Input
            id="max_budget_capacity"
            type="number"
            min={0}
            step="0.01"
            value={values.max_budget_capacity ?? ""}
            onChange={(e) =>
              set(
                "max_budget_capacity",
                e.target.value === "" ? null : Number(e.target.value)
              )
            }
          />
        </Field>
        {showStatusFields && (
          <>
            <Field label="Rating (0–5)" htmlFor="rating">
              <Input
                id="rating"
                type="number"
                min={0}
                max={5}
                step="0.1"
                value={values.rating ?? ""}
                onChange={(e) =>
                  set("rating", e.target.value === "" ? undefined : Number(e.target.value))
                }
              />
            </Field>
            <Field label="Status" htmlFor="current_status">
              <Select
                id="current_status"
                value={values.current_status}
                onChange={(e) => set("current_status", e.target.value)}
              >
                <option value="Active">Active</option>
                <option value="Inactive">Inactive</option>
                <option value="Blacklisted">Blacklisted</option>
              </Select>
            </Field>
          </>
        )}
      </div>

      <Field
        label="Capabilities description"
        htmlFor="capabilities_description"
        hint="Feeds the Gemini embedding — the more specific, the better the semantic ranking."
      >
        <Textarea
          id="capabilities_description"
          rows={4}
          value={values.capabilities_description ?? ""}
          onChange={(e) => set("capabilities_description", e.target.value)}
        />
      </Field>

      <div className="flex justify-end">
        <Button type="submit" disabled={submitting}>
          {submitting ? "Saving…" : submitLabel}
        </Button>
      </div>
    </form>
  );
}
