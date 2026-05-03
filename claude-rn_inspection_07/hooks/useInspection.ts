import { useState, useEffect, useCallback } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { File, Directory, Paths } from 'expo-file-system';
import { Inspection, InspectionPhoto, PhotoAnalysis, Finding, ChecklistItem } from '@/types';

const STORAGE_KEY = 'inspectai_inspections';
const PHOTOS_DIR = Paths.document.uri + 'inspectai_photos/';

function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).slice(2);
}

function ensurePhotosDir() {
  const dir = new Directory(PHOTOS_DIR);
  if (!dir.exists) dir.create({ intermediates: true });
}

const DEFAULT_CHECKLIST: Omit<ChecklistItem, 'id'>[] = [
  { label: 'Visual inspection complete', checked: false, category: 'General' },
  { label: 'No visible leaks or spills', checked: false, category: 'General' },
  { label: 'Safety labels intact', checked: false, category: 'Safety' },
  { label: 'Emergency shutoffs accessible', checked: false, category: 'Safety' },
  { label: 'Operating within normal parameters', checked: false, category: 'Performance' },
  { label: 'Unusual sounds or vibrations noted', checked: false, category: 'Performance' },
];

export function useInspection() {
  const [inspections, setInspections] = useState<Inspection[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    try {
      const raw = await AsyncStorage.getItem(STORAGE_KEY);
      setInspections(raw ? JSON.parse(raw) : []);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const save = async (items: Inspection[]) => {
    await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(items));
    setInspections(items);
  };

  const startInspection = async (equipmentId: string, equipmentName: string): Promise<Inspection> => {
    const now = new Date().toISOString();
    const inspection: Inspection = {
      id: generateId(),
      equipmentId,
      equipmentName,
      status: 'in_progress',
      startedAt: now,
      photos: [],
      findings: [],
      checklistItems: DEFAULT_CHECKLIST.map(item => ({ ...item, id: generateId() })),
    };
    await save([inspection, ...inspections]);
    return inspection;
  };

  const addPhoto = async (inspectionId: string, uri: string): Promise<InspectionPhoto> => {
    ensurePhotosDir();
    const photoId = generateId();
    const destPath = PHOTOS_DIR + photoId + '.jpg';
    new File(uri).copy(new File(destPath));
    const photo: InspectionPhoto = { id: photoId, uri: destPath, takenAt: new Date().toISOString() };
    const updated = inspections.map(i =>
      i.id === inspectionId ? { ...i, photos: [...i.photos, photo] } : i
    );
    await save(updated);
    return photo;
  };

  const updatePhotoAnalysis = async (inspectionId: string, photoId: string, analysis: PhotoAnalysis) => {
    const updated = inspections.map(i =>
      i.id === inspectionId
        ? { ...i, photos: i.photos.map(p => p.id === photoId ? { ...p, analysis } : p) }
        : i
    );
    await save(updated);
  };

  const removePhoto = async (inspectionId: string, photoId: string) => {
    const inspection = inspections.find(i => i.id === inspectionId);
    const photo = inspection?.photos.find(p => p.id === photoId);
    if (photo) { try { new File(photo.uri).delete(); } catch {} }
    const updated = inspections.map(i =>
      i.id === inspectionId ? { ...i, photos: i.photos.filter(p => p.id !== photoId) } : i
    );
    await save(updated);
  };

  const toggleChecklistItem = async (inspectionId: string, itemId: string) => {
    const updated = inspections.map(i =>
      i.id === inspectionId
        ? { ...i, checklistItems: i.checklistItems.map(c => c.id === itemId ? { ...c, checked: !c.checked } : c) }
        : i
    );
    await save(updated);
  };

  const addFinding = async (inspectionId: string, finding: Omit<Finding, 'id' | 'reportedAt'>): Promise<Finding> => {
    const newFinding: Finding = { ...finding, id: generateId(), reportedAt: new Date().toISOString() };
    const updated = inspections.map(i =>
      i.id === inspectionId ? { ...i, findings: [...i.findings, newFinding] } : i
    );
    await save(updated);
    return newFinding;
  };

  const removeFinding = async (inspectionId: string, findingId: string) => {
    const updated = inspections.map(i =>
      i.id === inspectionId ? { ...i, findings: i.findings.filter(f => f.id !== findingId) } : i
    );
    await save(updated);
  };

  const completeInspection = async (inspectionId: string) => {
    const updated = inspections.map(i =>
      i.id === inspectionId
        ? { ...i, status: 'completed' as const, completedAt: new Date().toISOString() }
        : i
    );
    await save(updated);
  };

  const getInspection = (id: string) => inspections.find(i => i.id === id);

  return {
    inspections,
    loading,
    startInspection,
    addPhoto,
    updatePhotoAnalysis,
    removePhoto,
    toggleChecklistItem,
    addFinding,
    removeFinding,
    completeInspection,
    getInspection,
    reload: load,
  };
}
