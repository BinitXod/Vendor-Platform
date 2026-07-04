"use client";

import { useState, type FormEvent } from "react";

import { Button, Field, Input, Select, Textarea } from "@/components/ui";

export type WorkRequirementFormValues = {
  title: string;
  description: string;
  category: string;
  location: string;
  estimated_value: number;
  priority: string;
  expected_start_date: string;
  status?: string;
};

type Props = {
  initial?: Partial<WorkRequirementFormValues>;
  onSubmit: (values: WorkRequirementFormValues) => Promise<unknown> | void;
  submitLabel?: string;
  submitting?: boolean;
  showStatus?: boolean;
};

function today(): string {
  return new Date().toISOString().slice(0, 10);
}

export function WorkRequirementForm({
  initial,
  onSubmit,
  submitLabel = "Save",
  submitting,
  showStatus = false,
}: Props) {
  const [values, setValues] = useState<WorkRequirementFormValues>({
    title: initial?.title ?? "",
    description: initial?.description ?? "",
    category: initial?.category ?? "",
    location: initial?.location ?? "",
    estimated_value: initial?.estimated_value ?? 0,
    priority: initial?.priority ?? "Medium",
    expected_start_date: initial?.expected_start_date ?? today(),
    status: initial?.status ?? "Open",
  });

  function set<K extends keyof WorkRequirementFormValues>(
    key: K,
    v: WorkRequirementFormValues[K]
  ) {
    setValues((prev) => ({ ...prev, [key]: v }));
  }

  async function handle(e: FormEvent) {
    e.preventDefault();
    await onSubmit(values);
  }

  return (
    <form onSubmit={handle} className="space-y-4">
      <Field label="Title" htmlFor="title">
        <Input
          id="title"
          required
          value={values.title}
          onChange={(e) => set("title", e.target.value)}
        />
      </Field>

      <Field
        label="Description"
        htmlFor="description"
        hint="Used to build the semantic search query — be specific."
      >
        <Textarea
          id="description"
          rows={4}
          required
          value={values.description}
          onChange={(e) => set("description", e.target.value)}
        />
      </Field>

      <div className="grid gap-4 md:grid-cols-2">
        <Field label="Category" htmlFor="category">
          <Input
            id="category"
            required
            value={values.category}
            onChange={(e) => set("category", e.target.value)}
          />
        </Field>
        <Field
          label="Location"
          htmlFor="location"
          hint="Must exactly match a vendor's operating_location."
        >
          <Input
            id="location"
            required
            value={values.location}
            onChange={(e) => set("location", e.target.value)}
          />
        </Field>

        <Field label="Estimated value" htmlFor="estimated_value">
          <Input
            id="estimated_value"
            type="number"
            min={0}
            step="0.01"
            required
            value={values.estimated_value}
            onChange={(e) => set("estimated_value", Number(e.target.value))}
          />
        </Field>
        <Field label="Priority" htmlFor="priority">
          <Select
            id="priority"
            value={values.priority}
            onChange={(e) => set("priority", e.target.value)}
          >
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
          </Select>
        </Field>

        <Field label="Expected start date" htmlFor="expected_start_date">
          <Input
            id="expected_start_date"
            type="date"
            required
            value={values.expected_start_date}
            onChange={(e) => set("expected_start_date", e.target.value)}
          />
        </Field>

        {showStatus && (
          <Field label="Status" htmlFor="status">
            <Select
              id="status"
              value={values.status}
              onChange={(e) => set("status", e.target.value)}
            >
              <option value="Open">Open</option>
              <option value="Sourcing">Sourcing</option>
              <option value="Awarded">Awarded</option>
              <option value="Closed">Closed</option>
            </Select>
          </Field>
        )}
      </div>

      <div className="flex justify-end">
        <Button type="submit" disabled={submitting}>
          {submitting ? "Saving…" : submitLabel}
        </Button>
      </div>
    </form>
  );
}
