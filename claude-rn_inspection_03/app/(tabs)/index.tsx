import { useCallback } from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import { useFocusEffect } from 'expo-router';
import { Colors } from '@/constants/Colors';
import { useEquipment } from '@/hooks/useEquipment';

export default function DashboardScreen() {
  const { equipment, reload: reloadEquipment } = useEquipment();

  // Reload whenever the dashboard regains focus so newly-added equipment
  // shows up without a manual pull-to-refresh.
  useFocusEffect(
    useCallback(() => {
      reloadEquipment();
    }, [reloadEquipment])
  );

  const activeCount = equipment.filter(e => e.status === 'active').length;

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
      </View>
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
});
