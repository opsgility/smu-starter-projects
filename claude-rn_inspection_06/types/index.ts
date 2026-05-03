export type EquipmentType =
  | 'electrical'
  | 'mechanical'
  | 'hvac'
  | 'plumbing'
  | 'safety'
  | 'it'
  | 'other';

export type EquipmentStatus = 'operational' | 'degraded' | 'failed' | 'offline';
export type InspectionStatus = 'in_progress' | 'completed';
export type FindingSeverity = 'good' | 'fair' | 'poor' | 'critical';

export interface Equipment {
  id: string;
  name: string;
  type: EquipmentType;
  location: string;
  serialNumber?: string;
  notes?: string;
  status: EquipmentStatus;
  lastInspectedAt?: string;
  createdAt: string;
}

export interface InspectionPhoto {
  id: string;
  uri: string;
  takenAt: string;
  analysis?: PhotoAnalysis;
}

export interface PhotoAnalysis {
  findings: string[];
  readings: MeterReading[];
  condition: FindingSeverity;
  confidence: number;
  summary: string;
}

export interface MeterReading {
  label: string;
  value: string;
  unit?: string;
}

export interface ChecklistItem {
  id: string;
  label: string;
  checked: boolean;
  notes?: string;
  required: boolean;
  category: string;
}

export interface Finding {
  id: string;
  description: string;
  severity: FindingSeverity;
  photoId?: string;
  recommendedAction?: string;
}

export interface Inspection {
  id: string;
  equipmentId: string;
  equipmentName: string;
  equipmentLocation: string;
  status: InspectionStatus;
  startedAt: string;
  completedAt?: string;
  photos: InspectionPhoto[];
  checklistItems: ChecklistItem[];
  findings: Finding[];
  overallCondition?: FindingSeverity;
  notes?: string;
}
