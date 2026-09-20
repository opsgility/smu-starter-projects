import { useState, useEffect, useCallback } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Equipment, EquipmentType, EquipmentStatus } from '@/types';

const STORAGE_KEY = 'inspectai_equipment';

function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).slice(2);
}

export function useEquipment() {
  const [equipment, setEquipment] = useState<Equipment[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    try {
      const raw = await AsyncStorage.getItem(STORAGE_KEY);
      setEquipment(raw ? JSON.parse(raw) : []);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const save = async (items: Equipment[]) => {
    await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(items));
    setEquipment(items);
  };

  const addEquipment = async (data: Omit<Equipment, 'id' | 'createdAt' | 'updatedAt'>) => {
    const now = new Date().toISOString();
    const item: Equipment = { ...data, id: generateId(), createdAt: now, updatedAt: now };
    await save([...equipment, item]);
    return item;
  };

  const updateEquipment = async (id: string, data: Partial<Equipment>) => {
    const updated = equipment.map(e =>
      e.id === id ? { ...e, ...data, updatedAt: new Date().toISOString() } : e
    );
    await save(updated);
  };

  const deleteEquipment = async (id: string) => {
    await save(equipment.filter(e => e.id !== id));
  };

  const getEquipment = (id: string) => equipment.find(e => e.id === id);

  return { equipment, loading, addEquipment, updateEquipment, deleteEquipment, getEquipment, reload: load };
}
