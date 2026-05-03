import { useState, useEffect, useCallback } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as FileSystem from 'expo-file-system';
import { Inspection, InspectionPhoto, PhotoAnalysis } from '@/types';

const STORAGE_KEY = 'inspectai_inspections';
const PHOTOS_DIR = FileSystem.documentDirectory + 'inspectai_photos/';

function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).slice(2);
}

async function ensurePhotosDir() {
  const info = await FileSystem.getInfoAsync(PHOTOS_DIR);
  if (!info.exists) await FileSystem.makeDirectoryAsync(PHOTOS_DIR, { intermediates: true });
}

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
      checklistItems: [],
    };
    await save([inspection, ...inspections]);
    return inspection;
  };

  const addPhoto = async (inspectionId: string, uri: string): Promise<InspectionPhoto> => {
    await ensurePhotosDir();
    const photoId = generateId();
    const destPath = PHOTOS_DIR + photoId + '.jpg';
    await FileSystem.copyAsync({ from: uri, to: destPath });

    const photo: InspectionPhoto = {
      id: photoId,
      uri: destPath,
      takenAt: new Date().toISOString(),
    };

    const updated = inspections.map(i =>
      i.id === inspectionId ? { ...i, photos: [...i.photos, photo] } : i
    );
    await save(updated);
    return photo;
  };

  const updatePhotoAnalysis = async (
    inspectionId: string,
    photoId: string,
    analysis: PhotoAnalysis
  ) => {
    const updated = inspections.map(i =>
      i.id === inspectionId
        ? {
            ...i,
            photos: i.photos.map(p =>
              p.id === photoId ? { ...p, analysis } : p
            ),
          }
        : i
    );
    await save(updated);
  };

  const removePhoto = async (inspectionId: string, photoId: string) => {
    const inspection = inspections.find(i => i.id === inspectionId);
    const photo = inspection?.photos.find(p => p.id === photoId);
    if (photo) await FileSystem.deleteAsync(photo.uri, { idempotent: true });
    const updated = inspections.map(i =>
      i.id === inspectionId
        ? { ...i, photos: i.photos.filter(p => p.id !== photoId) }
        : i
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
    completeInspection,
    getInspection,
    reload: load,
  };
}
