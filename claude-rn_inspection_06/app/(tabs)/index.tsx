import { useCallback } from 'react';
import { ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { useFocusEffect, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '@/constants/Colors';
import { useEquipment } from '@/hooks/useEquipment';
import { useInspection } from '@/hooks/useInspection';

export default function DashboardScreen() {
  const router = useRouter();
  const { equipment, reload: reloadEquipment } = useEquipment();
  const { inspections, reload: reloadInspections } = useInspection();

  // Reload whenever the dashboard regains focus so newly-added equipment and
  // completed inspections show up without a manual pull-to-refresh.
  useFocusEffect(
    useCallback(() => {
      reloadEquipment();
      reloadInspections();
    }, [reloadEquipment, reloadInspections])
  );

  const activeCount = equipment.filter(e => e.status === 'active').length;
  const inProgressCount = inspections.filter(i => i.status === 'in_progress').length;
  const completedCount = inspections.filter(i => i.status === 'completed').length;

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.title}>InspectAI</Text>
        <Text style={styles.subtitle}>AI-Powered Field Inspections</Text>
      </View>

      <View style={styles.statsRow}>
        <View style={styles.statCard}>
          <Text style={styles.statNum}>{activeCount}</Text>
          <Text style={styles.statLabel}>Equipment</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statNum}>{inProgressCount}</Text>
          <Text style={styles.statLabel}>In Progress</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statNum}>{completedCount}</Text>
          <Text style={styles.statLabel}>Completed</Text>
        </View>
      </View>

      <TouchableOpacity style={styles.startBtn} onPress={() => router.push('/inspection/new')}>
        <Ionicons name="add-circle" size={22} color="#fff" />
        <Text style={styles.startBtnText}>Start New Inspection</Text>
      </TouchableOpacity>

      {inProgressCount > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>In Progress</Text>
          {inspections.filter(i => i.status === 'in_progress').map(i => (
            <TouchableOpacity
              key={i.id}
              style={styles.inspectionRow}
              onPress={() => router.push(`/inspection/${i.id}`)}
            >
              <View style={styles.inspIconBox}>
                <Ionicons name="clipboard" size={20} color={Colors.primary} />
              </View>
              <View style={styles.inspInfo}>
                <Text style={styles.inspName}>{i.equipmentName}</Text>
                <Text style={styles.inspMeta}>{i.photos.length} photo{i.photos.length !== 1 ? 's' : ''} · {new Date(i.startedAt).toLocaleDateString()}</Text>
              </View>
              <Ionicons name="chevron-forward" size={18} color={Colors.textLight} />
            </TouchableOpacity>
          ))}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  content: { padding: 20, paddingBottom: 40 },
  header: { marginBottom: 20 },
  title: { fontSize: 28, fontWeight: '700', color: Colors.text },
  subtitle: { fontSize: 14, color: Colors.textSecondary, marginTop: 4 },
  statsRow: { flexDirection: 'row', gap: 12, marginBottom: 20 },
  statCard: { flex: 1, backgroundColor: Colors.surface, borderRadius: 12, padding: 14, alignItems: 'center', borderWidth: 1, borderColor: Colors.border },
  statNum: { fontSize: 24, fontWeight: '700', color: Colors.primary },
  statLabel: { fontSize: 11, color: Colors.textSecondary, marginTop: 2 },
  startBtn: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, backgroundColor: Colors.primary, borderRadius: 12, padding: 16, marginBottom: 24 },
  startBtnText: { color: '#fff', fontSize: 16, fontWeight: '700' },
  section: { gap: 10 },
  sectionTitle: { fontSize: 16, fontWeight: '600', color: Colors.text, marginBottom: 4 },
  inspectionRow: { flexDirection: 'row', alignItems: 'center', gap: 12, backgroundColor: Colors.surface, borderRadius: 12, padding: 14, borderWidth: 1, borderColor: Colors.border },
  inspIconBox: { width: 40, height: 40, borderRadius: 8, backgroundColor: Colors.primaryLight, alignItems: 'center', justifyContent: 'center' },
  inspInfo: { flex: 1 },
  inspName: { fontSize: 14, fontWeight: '600', color: Colors.text },
  inspMeta: { fontSize: 12, color: Colors.textSecondary, marginTop: 2 },
});
