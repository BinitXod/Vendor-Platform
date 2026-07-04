"use client";

import { useMutation, useQuery } from "@tanstack/react-query";

import { api } from "@/lib/api-client";
import type { Recommendation, UUID } from "@/lib/types";

export function useRecommendations(workReqId: UUID | undefined) {
  return useQuery({
    enabled: !!workReqId,
    queryKey: ["recommendations", workReqId ?? ""],
    queryFn: () =>
      api.get<Recommendation[]>(`/recommendations/${workReqId}`),
  });
}

export function useTriggerReport() {
  return useMutation({
    mutationFn: (workReqId: UUID) =>
      api.post<{ message: string; work_requirement_id: UUID }>(
        `/recommendations/${workReqId}/report`
      ),
  });
}
