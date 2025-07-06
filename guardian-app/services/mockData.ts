import { Child, VaccinationRecord, GrowthRecord, Notification, Vaccine, Guardian } from '../types';

// Mock data for read-only app
export const mockGuardian: Guardian = {
  national_id: "123456789",
  fullname:"Sarah Johnson",
  phone_number: "+1234567890",
  email: "sarah.johnson@email.com",
  address: "123 Main St, City, State 12345"
};

export const mockChildren: Child[] = [
  {
    child_id: "C001",
    first_name: "Emma",
    last_name: "Johnson",
    date_of_birth: "2022-03-15",
    gender: "F",
    birth_weight: 3.2,
    birth_height: 50.5,
    national_id: "123456789",
    registered_by: "HW001",
    date_registered: "2022-03-20T10:00:00Z",
    is_active: true,
    age_in_months: 21,
    age_in_years: 1
  },
  {
    child_id: "C002",
    first_name: "Liam",
    last_name: "Johnson",
    date_of_birth: "2020-08-10",
    gender: "M",
    birth_weight: 3.5,
    birth_height: 52.0,
    national_id: "123456789",
    registered_by: "HW001",
    date_registered: "2020-08-15T14:30:00Z",
    is_active: true,
    age_in_months: 40,
    age_in_years: 3
  }
];

export const mockVaccines: Vaccine[] = [
  {
    v_ID: "V001",
    name: "BCG",
    description: "Bacillus Calmette-Guérin vaccine",
    recommended_age_months: 0,
    doses_required: 1
  },
  {
    v_ID: "V002",
    name: "DPT",
    description: "Diphtheria, Pertussis, Tetanus",
    recommended_age_months: 2,
    doses_required: 3
  },
  {
    v_ID: "V003",
    name: "MMR",
    description: "Measles, Mumps, Rubella",
    recommended_age_months: 12,
    doses_required: 2
  },
  {
    v_ID: "V004",
    name: "Hepatitis B",
    description: "Hepatitis B vaccine",
    recommended_age_months: 0,
    doses_required: 3
  }
];

export const mockVaccinationRecords: VaccinationRecord[] = [
  {
    recordID: "VR001",
    child_id: "C001",
    v_ID: "V001",
    administrationDate: "2022-03-20T10:30:00Z",
    doseNumber: 1,
    remarks: "Administered at birth",
    administered_by: "HW001",
    vaccine_name: "BCG"
  },
  {
    recordID: "VR002",
    child_id: "C001",
    v_ID: "V002",
    administrationDate: "2022-05-15T09:00:00Z",
    doseNumber: 1,
    remarks: "First dose",
    administered_by: "HW002",
    vaccine_name: "DPT"
  },
  {
    recordID: "VR003",
    child_id: "C001",
    v_ID: "V002",
    administrationDate: "2022-07-15T09:00:00Z",
    doseNumber: 2,
    remarks: "Second dose",
    administered_by: "HW002",
    vaccine_name: "DPT"
  },
  {
    recordID: "VR004",
    child_id: "C002",
    v_ID: "V001",
    administrationDate: "2020-08-15T14:30:00Z",
    doseNumber: 1,
    remarks: "Administered at birth",
    administered_by: "HW001",
    vaccine_name: "BCG"
  },
  {
    recordID: "VR005",
    child_id: "C002",
    v_ID: "V003",
    administrationDate: "2021-08-10T10:00:00Z",
    doseNumber: 1,
    remarks: "First dose",
    administered_by: "HW003",
    vaccine_name: "MMR"
  }
];

export const mockGrowthRecords: GrowthRecord[] = [
  {
    child_id: "C001",
    date_recorded: "2022-03-20",
    weight: 3.2,
    height: 50.5,
    recorded_by: "HW001",
    notes: "Birth measurements",
    date_created: "2022-03-20T10:00:00Z"
  },
  {
    child_id: "C001",
    date_recorded: "2022-06-15",
    weight: 6.8,
    height: 65.2,
    recorded_by: "HW002",
    notes: "3-month checkup",
    date_created: "2022-06-15T09:00:00Z"
  },
  {
    child_id: "C001",
    date_recorded: "2022-09-15",
    weight: 8.5,
    height: 70.1,
    recorded_by: "HW002",
    notes: "6-month checkup",
    date_created: "2022-09-15T09:00:00Z"
  },
  {
    child_id: "C002",
    date_recorded: "2020-08-15",
    weight: 3.5,
    height: 52.0,
    recorded_by: "HW001",
    notes: "Birth measurements",
    date_created: "2020-08-15T14:30:00Z"
  },
  {
    child_id: "C002",
    date_recorded: "2023-08-10",
    weight: 15.2,
    height: 95.5,
    recorded_by: "HW003",
    notes: "3-year checkup",
    date_created: "2023-08-10T10:00:00Z"
  }
];

export const mockNotifications: Notification[] = [
  {
    guardian: "G123456789",
    notification_type: "WEEK_BEFORE",
    message: "Reminder: Emma's next vaccination appointment is scheduled for next week on March 15th, 2024.",
    is_sent: true,
    date_sent: "2024-03-08T09:00:00Z",
    date_created: "2024-03-08T09:00:00Z"
  },
  {
    guardian: "G123456789",
    notification_type: "TWO_DAYS_BEFORE",
    message: "Reminder: Liam's growth checkup is scheduled for March 12th, 2024.",
    is_sent: true,
    date_sent: "2024-03-10T09:00:00Z",
    date_created: "2024-03-10T09:00:00Z"
  },
  {
    guardian: "G123456789",
    notification_type: "MISSED_APPOINTMENT",
    message: "You missed Emma's vaccination appointment on March 1st, 2024. Please reschedule.",
    is_sent: true,
    date_sent: "2024-03-02T09:00:00Z",
    date_created: "2024-03-02T09:00:00Z"
  }
];

// Helper functions
export const getChildById = (childId: string): Child | undefined => {
  return mockChildren.find(child => child.child_id === childId);
};

export const getVaccinationRecordsByChild = (childId: string): VaccinationRecord[] => {
  return mockVaccinationRecords.filter(record => record.child_id === childId);
};

export const getGrowthRecordsByChild = (childId: string): GrowthRecord[] => {
  return mockGrowthRecords.filter(record => record.child_id === childId);
};

export const getNotificationsByGuardian = (guardianId: string): Notification[] => {
  return mockNotifications.filter(notification => notification.guardian === guardianId);
}; 