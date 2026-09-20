import { useState } from 'react';
import { Alert, Modal, ScrollView, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import { useLocalSearchParams } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '@/constants/Colors';
import { useInspection } from '@/hooks/useInspection';
import { FindingSeverity } from '@/types';

const SEVERITIES: FindingSeverity[] = ['low', 'medium', 'high', 'critical'];
const SEVERITY_COLORS: Record<FindingSeverity, string> = {
  low: Colors.success,
  medium: Colors.warning,
  high: Colors.danger,
  critical: '#7C0A02',
};

export default function ChecklistScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const { getInspection, toggleChecklistItem, addFinding, removeFinding, reload } = useInspection();
  const inspection = getInspection(id);

  const [showAddFinding, setShowAddFinding] = useState(false);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [severity, setSeverity] = useState<FindingSeverity>('medium');
  const [saving, setSaving] = useState(false);

  if (!inspection) {
    return (
      <View style={styles.centered}>
        <Text style={styles.notFound}>Inspection not found.</Text>
      </View>
    );
  }

  const categories = [...new Set(inspection.checklistItems.map(c => c.category))];
  const checkedCount = inspection.checklistItems.filter(c => c.checked).length;

  const handleToggle = async (itemId: string) => {
    await toggleChecklistItem(id, itemId);
    await reload();
  };

  const handleAddFinding = async () => {
    if (!title.trim()) { Alert.alert('Validation', 'Title is required'); return; }
    setSaving(true);
    try {
      await addFinding(id, { title: title.trim(), description: description.trim(), severity });
      await reload();
      setTitle('');
      setDescription('');
      setSeverity('medium');
      setShowAddFinding(false);
    } finally {
      setSaving(false);
    }
  };

  const confirmRemoveFinding = (findingId: string, findingTitle: string) => {
    Alert.alert('Remove Finding', `Remove "${findingTitle}"?`, [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Remove', style: 'destructive', onPress: async () => { await removeFinding(id, findingId); await reload(); } },
    ]);
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.progressCard}>
        <Text style={styles.progressLabel}>Checklist Progress</Text>
        <Text style={styles.progressCount}>{checkedCount} / {inspection.checklistItems.length}</Text>
        <View style={styles.progressBar}>
          <View style={[styles.progressFill, { width: `${inspection.checklistItems.length > 0 ? (checkedCount / inspection.checklistItems.length) * 100 : 0}%` }]} />
        </View>
      </View>

      {categories.map(cat => (
        <View key={cat} style={styles.section}>
          <Text style={styles.sectionTitle}>{cat}</Text>
          {inspection.checklistItems.filter(c => c.category === cat).map(item => (
            <TouchableOpacity key={item.id} style={styles.checkRow} onPress={() => handleToggle(item.id)}>
              <Ionicons
                name={item.checked ? 'checkbox' : 'square-outline'}
                size={22}
                color={item.checked ? Colors.success : Colors.textLight}
              />
              <Text style={[styles.checkLabel, item.checked && styles.checkLabelDone]}>{item.label}</Text>
            </TouchableOpacity>
          ))}
        </View>
      ))}

      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Findings ({inspection.findings.length})</Text>
          {inspection.status === 'in_progress' && (
            <TouchableOpacity style={styles.addFindingBtn} onPress={() => setShowAddFinding(true)}>
              <Ionicons name="add" size={16} color={Colors.primary} />
              <Text style={styles.addFindingBtnText}>Add</Text>
            </TouchableOpacity>
          )}
        </View>
        {inspection.findings.map(finding => (
          <View key={finding.id} style={styles.findingCard}>
            <View style={styles.findingHeader}>
              <View style={[styles.severityBadge, { backgroundColor: SEVERITY_COLORS[finding.severity] + '22' }]}>
                <Text style={[styles.severityText, { color: SEVERITY_COLORS[finding.severity] }]}>
                  {finding.severity.toUpperCase()}
                </Text>
              </View>
              {inspection.status === 'in_progress' && (
                <TouchableOpacity onPress={() => confirmRemoveFinding(finding.id, finding.title)} hitSlop={8}>
                  <Ionicons name="trash-outline" size={16} color={Colors.danger} />
                </TouchableOpacity>
              )}
            </View>
            <Text style={styles.findingTitle}>{finding.title}</Text>
            {finding.description ? <Text style={styles.findingDesc}>{finding.description}</Text> : null}
          </View>
        ))}
        {inspection.findings.length === 0 && (
          <Text style={styles.noFindings}>No findings recorded.</Text>
        )}
      </View>

      <Modal visible={showAddFinding} animationType="slide" presentationStyle="pageSheet">
        <View style={styles.modal}>
          <View style={styles.modalHeader}>
            <Text style={styles.modalTitle}>Add Finding</Text>
            <TouchableOpacity onPress={() => setShowAddFinding(false)}>
              <Ionicons name="close" size={24} color={Colors.text} />
            </TouchableOpacity>
          </View>
          <View style={styles.field}>
            <Text style={styles.label}>Title *</Text>
            <TextInput style={styles.input} value={title} onChangeText={setTitle} placeholder="e.g. Corroded pipe fitting" placeholderTextColor={Colors.textLight} />
          </View>
          <View style={styles.field}>
            <Text style={styles.label}>Description</Text>
            <TextInput style={[styles.input, styles.multiline]} value={description} onChangeText={setDescription} placeholder="Optional details..." placeholderTextColor={Colors.textLight} multiline numberOfLines={3} />
          </View>
          <View style={styles.field}>
            <Text style={styles.label}>Severity</Text>
            <View style={styles.severityRow}>
              {SEVERITIES.map(s => (
                <TouchableOpacity
                  key={s}
                  style={[styles.severityChip, { borderColor: SEVERITY_COLORS[s] }, severity === s && { backgroundColor: SEVERITY_COLORS[s] }]}
                  onPress={() => setSeverity(s)}
                >
                  <Text style={[styles.severityChipText, { color: severity === s ? '#fff' : SEVERITY_COLORS[s] }]}>
                    {s.charAt(0).toUpperCase() + s.slice(1)}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>
          <TouchableOpacity style={[styles.saveBtn, saving && styles.disabled]} onPress={handleAddFinding} disabled={saving}>
            <Text style={styles.saveBtnText}>{saving ? 'Saving...' : 'Add Finding'}</Text>
          </TouchableOpacity>
        </View>
      </Modal>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  content: { padding: 16, paddingBottom: 40, gap: 16 },
  centered: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  notFound: { color: Colors.textSecondary },
  progressCard: { backgroundColor: Colors.surface, borderRadius: 12, padding: 16, borderWidth: 1, borderColor: Colors.border, gap: 8 },
  progressLabel: { fontSize: 13, color: Colors.textSecondary, fontWeight: '600', textTransform: 'uppercase', letterSpacing: 0.5 },
  progressCount: { fontSize: 22, fontWeight: '700', color: Colors.primary },
  progressBar: { height: 6, backgroundColor: Colors.border, borderRadius: 3 },
  progressFill: { height: '100%', backgroundColor: Colors.primary, borderRadius: 3 },
  section: { backgroundColor: Colors.surface, borderRadius: 12, padding: 16, borderWidth: 1, borderColor: Colors.border, gap: 10 },
  sectionHeader: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  sectionTitle: { fontSize: 15, fontWeight: '600', color: Colors.text },
  checkRow: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  checkLabel: { flex: 1, fontSize: 14, color: Colors.text },
  checkLabelDone: { color: Colors.textLight, textDecorationLine: 'line-through' },
  addFindingBtn: { flexDirection: 'row', alignItems: 'center', gap: 4, borderWidth: 1, borderColor: Colors.primary, borderRadius: 6, paddingHorizontal: 8, paddingVertical: 4 },
  addFindingBtnText: { color: Colors.primary, fontSize: 13, fontWeight: '600' },
  findingCard: { backgroundColor: Colors.background, borderRadius: 10, padding: 12, gap: 6 },
  findingHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  severityBadge: { borderRadius: 4, paddingHorizontal: 8, paddingVertical: 3 },
  severityText: { fontSize: 10, fontWeight: '700' },
  findingTitle: { fontSize: 14, fontWeight: '600', color: Colors.text },
  findingDesc: { fontSize: 13, color: Colors.textSecondary, lineHeight: 18 },
  noFindings: { fontSize: 13, color: Colors.textLight, textAlign: 'center', paddingVertical: 8 },
  modal: { flex: 1, padding: 20, backgroundColor: Colors.background, gap: 8 },
  modalHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 },
  modalTitle: { fontSize: 18, fontWeight: '700', color: Colors.text },
  field: { marginBottom: 12 },
  label: { fontSize: 13, fontWeight: '600', color: Colors.textSecondary, marginBottom: 6, textTransform: 'uppercase', letterSpacing: 0.5 },
  input: { backgroundColor: Colors.surface, borderRadius: 10, borderWidth: 1, borderColor: Colors.border, padding: 12, fontSize: 15, color: Colors.text },
  multiline: { height: 80, textAlignVertical: 'top' },
  severityRow: { flexDirection: 'row', gap: 8 },
  severityChip: { flex: 1, alignItems: 'center', paddingVertical: 8, borderRadius: 8, borderWidth: 1.5 },
  severityChipText: { fontSize: 12, fontWeight: '700' },
  saveBtn: { backgroundColor: Colors.primary, borderRadius: 12, padding: 16, alignItems: 'center', marginTop: 8 },
  disabled: { opacity: 0.6 },
  saveBtnText: { color: '#fff', fontSize: 16, fontWeight: '700' },
});
