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

export type AnalysisCondition = 'good' | 'fair' | 'poor' | 'critical';
export type AnalysisUrgency = 'routine' | 'soon' | 'immediate';

export interface PhotoAnalysis {
  condition: AnalysisCondition;
  summary: string;
  defects: string[];
  recommendations: string[];
  urgency: AnalysisUrgency;
  analyzedAt: string;
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
