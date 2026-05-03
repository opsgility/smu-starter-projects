import { useState, useEffect } from 'react';
import { ScrollView, StyleSheet, Text, TextInput, TouchableOpacity, View, Alert } from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { Colors } from '@/constants/Colors';
import { useEquipment } from '@/hooks/useEquipment';
import { Equipment, EquipmentType, EquipmentStatus } from '@/types';

const TYPES: EquipmentType[] = ['electrical', 'mechanical', 'hvac', 'plumbing', 'safety', 'it', 'vehicle', 'other'];
const STATUSES: EquipmentStatus[] = ['active', 'inactive', 'maintenance', 'retired'];

function SelectRow<T extends string>({
  label, options, value, onChange,
}: { label: string; options: T[]; value: T; onChange: (v: T) => void }) {
  return (
    <View style={styles.field}>
      <Text style={styles.label}>{label}</Text>
      <ScrollView horizontal showsHorizontalScrollIndicator={false}>
        {options.map(opt => (
          <TouchableOpacity
            key={opt}
            style={[styles.chip, value === opt && styles.chipActive]}
            onPress={() => onChange(opt)}
          >
            <Text style={[styles.chipText, value === opt && styles.chipTextActive]}>
              {opt.charAt(0).toUpperCase() + opt.slice(1)}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>
    </View>
  );
}

export default function EditEquipmentScreen() {
  const router = useRouter();
  const { id } = useLocalSearchParams<{ id: string }>();
  const { getEquipment, updateEquipment, deleteEquipment } = useEquipment();
  const item = getEquipment(id);

  const [name, setName] = useState(item?.name ?? '');
  const [type, setType] = useState<EquipmentType>(item?.type ?? 'electrical');
  const [status, setStatus] = useState<EquipmentStatus>(item?.status ?? 'active');
  const [location, setLocation] = useState(item?.location ?? '');
  const [serialNumber, setSerialNumber] = useState(item?.serialNumber ?? '');
  const [manufacturer, setManufacturer] = useState(item?.manufacturer ?? '');
  const [model, setModel] = useState(item?.model ?? '');
  const [notes, setNotes] = useState(item?.notes ?? '');
  const [saving, setSaving] = useState(false);

  if (!item) {
    return (
      <View style={styles.centered}>
        <Text style={styles.notFound}>Equipment not found.</Text>
      </View>
    );
  }

  const handleSave = async () => {
    if (!name.trim()) { Alert.alert('Validation', 'Name is required'); return; }
    setSaving(true);
    try {
      await updateEquipment(id, { name: name.trim(), type, status, location: location.trim(), serialNumber: serialNumber.trim() || undefined, manufacturer: manufacturer.trim() || undefined, model: model.trim() || undefined, notes: notes.trim() || undefined });
      router.back();
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = () => {
    Alert.alert('Delete Equipment', `Remove "${item.name}"?`, [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Delete', style: 'destructive', onPress: async () => { await deleteEquipment(id); router.back(); } },
    ]);
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.field}>
        <Text style={styles.label}>Name *</Text>
        <TextInput style={styles.input} value={name} onChangeText={setName} placeholderTextColor={Colors.textLight} />
      </View>
      <SelectRow label="Type *" options={TYPES} value={type} onChange={setType} />
      <SelectRow label="Status *" options={STATUSES} value={status} onChange={setStatus} />
      <View style={styles.field}>
        <Text style={styles.label}>Location *</Text>
        <TextInput style={styles.input} value={location} onChangeText={setLocation} placeholderTextColor={Colors.textLight} />
      </View>
      <View style={styles.field}>
        <Text style={styles.label}>Serial Number</Text>
        <TextInput style={styles.input} value={serialNumber} onChangeText={setSerialNumber} placeholder="Optional" placeholderTextColor={Colors.textLight} />
      </View>
      <View style={styles.field}>
        <Text style={styles.label}>Manufacturer</Text>
        <TextInput style={styles.input} value={manufacturer} onChangeText={setManufacturer} placeholder="Optional" placeholderTextColor={Colors.textLight} />
      </View>
      <View style={styles.field}>
        <Text style={styles.label}>Model</Text>
        <TextInput style={styles.input} value={model} onChangeText={setModel} placeholder="Optional" placeholderTextColor={Colors.textLight} />
      </View>
      <View style={styles.field}>
        <Text style={styles.label}>Notes</Text>
        <TextInput style={[styles.input, styles.multiline]} value={notes} onChangeText={setNotes} placeholder="Optional" placeholderTextColor={Colors.textLight} multiline numberOfLines={3} />
      </View>
      <TouchableOpacity style={[styles.saveBtn, saving && styles.disabled]} onPress={handleSave} disabled={saving}>
        <Text style={styles.saveBtnText}>{saving ? 'Saving...' : 'Save Changes'}</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.deleteBtn} onPress={handleDelete}>
        <Text style={styles.deleteBtnText}>Delete Equipment</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  content: { padding: 20, paddingBottom: 40, gap: 4 },
  centered: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  notFound: { color: Colors.textSecondary },
  field: { marginBottom: 16 },
  label: { fontSize: 13, fontWeight: '600', color: Colors.textSecondary, marginBottom: 6, textTransform: 'uppercase', letterSpacing: 0.5 },
  input: { backgroundColor: Colors.surface, borderRadius: 10, borderWidth: 1, borderColor: Colors.border, padding: 12, fontSize: 15, color: Colors.text },
  multiline: { height: 80, textAlignVertical: 'top' },
  chip: { paddingHorizontal: 14, paddingVertical: 8, borderRadius: 20, borderWidth: 1, borderColor: Colors.border, marginRight: 8, backgroundColor: Colors.surface },
  chipActive: { backgroundColor: Colors.primary, borderColor: Colors.primary },
  chipText: { fontSize: 13, color: Colors.textSecondary },
  chipTextActive: { color: '#fff', fontWeight: '600' },
  saveBtn: { marginTop: 8, backgroundColor: Colors.primary, borderRadius: 12, padding: 16, alignItems: 'center' },
  disabled: { opacity: 0.6 },
  saveBtnText: { color: '#fff', fontSize: 16, fontWeight: '700' },
  deleteBtn: { marginTop: 12, borderRadius: 12, padding: 16, alignItems: 'center', borderWidth: 1, borderColor: Colors.danger },
  deleteBtnText: { color: Colors.danger, fontSize: 16, fontWeight: '600' },
});
