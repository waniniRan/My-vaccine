// TypeScript interfaces for Guardian App data models

export interface Child {
  child_id: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: 'M' | 'F';
  birth_weight: number;
  birth_height: number;
  national_id: string; // Guardian ID
  registered_by: string;
  date_registered: string;
  is_active: boolean;
  age_in_months?: number;
  age_in_years?: number;
}

export interface VaccinationRecord {
  recordID: string;
  child_id: string;
  v_ID: string;
  administrationDate: string;
  doseNumber: number;
  remarks?: string;
  administered_by: string;
  side_effects?: string;
  vaccine_name?: string; // For display purposes
}

export interface GrowthRecord {
  child_id: string;
  date_recorded: string;
  weight: number;
  height: number;
  recorded_by: string;
  notes?: string;
  date_created: string;
}

export interface Notification {
  guardian: string;
  notification_type: 'WEEK_BEFORE' | 'TWO_DAYS_BEFORE' | 'MISSED_APPOINTMENT';
  message: string;
  is_sent: boolean;
  date_sent?: string;
  date_created: string;
}

export interface Guardian {
  national_id: string;
  fullname: string;
  phone_number: string;
  email?: string;
  address?: string;
  children?: Child[];
}

export interface Vaccine {
  v_ID: string;
  name: string;
  description?: string;
  recommended_age_months?: number;
  doses_required?: number;
}

// Mock data types for read-only app
export interface MockData {
  children: Child[];
  vaccinationRecords: VaccinationRecord[];
  growthRecords: GrowthRecord[];
  notifications: Notification[];
  vaccines: Vaccine[];
} 