"use client";

import {
  useMutation,
  useQuery,
  useQueryClient,
  type UseQueryResult,
} from "@tanstack/react-query";

import { api } from "@/lib/api-client";
import type {
  Page,
  UUID,
  Vendor,
  VendorCreate,
  VendorUpdate,
} from "@/lib/types";

const KEYS = {
  all: ["vendors"] as const,
  list: (skip: number, limit: number) =>
    ["vendors", "list", { skip, limit }] as const,
  detail: (id: UUID) => ["vendors", "detail", id] as const,
};

export function useVendorList(
  skip = 0,
  limit = 50
): UseQueryResult<Page<Vendor>> {
  return useQuery({
    queryKey: KEYS.list(skip, limit),
    queryFn: () =>
      api.get<Page<Vendor>>(`/vendors?skip=${skip}&limit=${limit}`),
  });
}

export function useVendor(id: UUID | undefined) {
  return useQuery({
    enabled: !!id,
    queryKey: KEYS.detail(id ?? ""),
    queryFn: () => api.get<Vendor>(`/vendors/${id}`),
  });
}

export function useCreateVendor() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (input: VendorCreate) => api.post<Vendor>("/vendors", input),
    onSuccess: () => qc.invalidateQueries({ queryKey: KEYS.all }),
  });
}

export function useUpdateVendor(id: UUID) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (input: VendorUpdate) =>
      api.patch<Vendor>(`/vendors/${id}`, input),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: KEYS.all });
      qc.invalidateQueries({ queryKey: KEYS.detail(id) });
    },
  });
}

export function useDeleteVendor() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: UUID) => api.del<void>(`/vendors/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: KEYS.all }),
  });
}
