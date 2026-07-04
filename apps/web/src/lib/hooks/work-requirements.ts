"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { api } from "@/lib/api-client";
import type {
  Page,
  UUID,
  WorkRequirement,
  WorkRequirementCreate,
  WorkRequirementUpdate,
} from "@/lib/types";

const KEYS = {
  all: ["work-requirements"] as const,
  list: (skip: number, limit: number) =>
    ["work-requirements", "list", { skip, limit }] as const,
  detail: (id: UUID) => ["work-requirements", "detail", id] as const,
};

export function useWorkRequirementList(skip = 0, limit = 50) {
  return useQuery({
    queryKey: KEYS.list(skip, limit),
    queryFn: () =>
      api.get<Page<WorkRequirement>>(
        `/work-requirements?skip=${skip}&limit=${limit}`
      ),
  });
}

export function useWorkRequirement(id: UUID | undefined) {
  return useQuery({
    enabled: !!id,
    queryKey: KEYS.detail(id ?? ""),
    queryFn: () => api.get<WorkRequirement>(`/work-requirements/${id}`),
  });
}

export function useCreateWorkRequirement() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (input: WorkRequirementCreate) =>
      api.post<WorkRequirement>("/work-requirements", input),
    onSuccess: () => qc.invalidateQueries({ queryKey: KEYS.all }),
  });
}

export function useUpdateWorkRequirement(id: UUID) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (input: WorkRequirementUpdate) =>
      api.patch<WorkRequirement>(`/work-requirements/${id}`, input),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: KEYS.all });
      qc.invalidateQueries({ queryKey: KEYS.detail(id) });
    },
  });
}

export function useDeleteWorkRequirement() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: UUID) => api.del<void>(`/work-requirements/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: KEYS.all }),
  });
}
