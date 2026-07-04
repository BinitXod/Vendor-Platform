// Mirrors the Pydantic schemas in apps/backend/app/schemas/*.
// Keep this file in sync when backend contracts change.

export type UUID = string;
export type ISODate = string;
export type ISODateTime = string;

// -------- Vendors --------

export interface Vendor {
  id: UUID;
  name: string;
  vendor_type: string;
  category: string;
  contact_email: string;
  contact_phone: string | null;
  operating_location: string;
  rating: number;
  current_status: string; // Active | Inactive | Blacklisted
  max_budget_capacity: number | null;
  capabilities_description: string | null;
  created_at: ISODateTime;
  documents: VendorDocument[];
}

export interface VendorCreate {
  name: string;
  vendor_type: string;
  category: string;
  contact_email: string;
  contact_phone?: string | null;
  operating_location: string;
  max_budget_capacity?: number | null;
  capabilities_description?: string | null;
}

export interface VendorUpdate {
  name?: string;
  rating?: number;
  current_status?: string;
  max_budget_capacity?: number | null;
  capabilities_description?: string | null;
}

export interface VendorDocument {
  id: UUID;
  vendor_id: UUID;
  document_type: string;
  file_path: string;
  expiry_date: ISODate | null;
  verification_status: string;
  created_at: ISODateTime;
}

// -------- Work Requirements --------

export interface WorkRequirement {
  id: UUID;
  title: string;
  description: string;
  category: string;
  location: string;
  estimated_value: number;
  priority: string;
  expected_start_date: ISODate;
  status: string; // Open | Sourcing | Awarded | Closed
  created_at: ISODateTime;
}

export interface WorkRequirementCreate {
  title: string;
  description: string;
  category: string;
  location: string;
  estimated_value: number;
  priority?: string;
  expected_start_date: ISODate;
}

export interface WorkRequirementUpdate {
  title?: string;
  description?: string;
  category?: string;
  location?: string;
  estimated_value?: number;
  priority?: string;
  expected_start_date?: ISODate;
  status?: string;
}

// -------- Recommendations --------

export interface RecommendationBreakdown {
  semantic_match_score: number;
  rating_score: number;
  budget_score: number;
}

export interface Recommendation {
  vendor_id: UUID;
  name: string;
  category: string;
  score: number;
  breakdown: RecommendationBreakdown;
  contact_email: string;
}

// -------- Pagination --------

export interface Page<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}
