import { FlatList, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '@/constants/Colors';
import { useInspection } from '@/hooks/useInspection';
import { FindingSeverity } from '@/types';

const SEVERITY_COLORS: Record<FindingSeverity, string> = {
  low: Colors.success,
  medium: Colors.warning,
  high: Colors.danger,
  critical: '#7C0A02',
};

export default function HistoryScreen() {
  const router = useRouter();
  const { inspections, loading } = useInspection();
  const completed = inspections.filter(i => i.status === 'completed');

  if (loading) {
    return <View style={styles.centered}><Text style={styles.loadingText}>Loading...</Text></View>;
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={completed}
        keyExtractor={item => item.id}
        contentContainerStyle={styles.list}
        ItemSeparatorComponent={() => <View style={{ height: 10 }} />}
        ListEmptyComponent={
          <View style={styles.empty}>
            <Ionicons name="time-outline" size={56} color={Colors.textLight} />
            <Text style={styles.emptyTitle}>No Completed Inspections</Text>
            <Text style={styles.emptyText}>Complete an inspection to see it here.</Text>
          </View>
        }
        renderItem={({ item }) => {
          const highFindings = item.findings.filter(f => f.severity === 'high' || f.severity === 'critical');
          const checkedCount = item.checklistItems.filter(c => c.checked).length;
          return (
            <TouchableOpacity
              style={styles.card}
              onPress={() => router.push(`/inspection/${item.id}/checklist`)}
              activeOpacity={0.7}
            >
              <View style={styles.cardHeader}>
                <View style={styles.iconBox}>
                  <Ionicons name="clipboard-outline" size={20} color={Colors.primary} />
                </View>
                <View style={styles.cardInfo}>
                  <Text style={styles.cardTitle}>{item.equipmentName}</Text>
                  <Text style={styles.cardDate}>
                    {item.completedAt ? new Date(item.completedAt).toLocaleDateString() : ''}
                  </Text>
                </View>
              </View>
              <View style={styles.cardStats}>
                <View style={styles.stat}>
                  <Ionicons name="camera-outline" size={14} color={Colors.textSecondary} />
                  <Text style={styles.statText}>{item.photos.length} photo{item.photos.length !== 1 ? 's' : ''}</Text>
                </View>
                <View style={styles.stat}>
                  <Ionicons name="checkbox-outline" size={14} color={Colors.textSecondary} />
                  <Text style={styles.statText}>{checkedCount}/{item.checklistItems.length} checks</Text>
                </View>
                {item.findings.length > 0 && (
                  <View style={styles.stat}>
                    <Ionicons name="warning-outline" size={14} color={highFindings.length > 0 ? Colors.danger : Colors.warning} />
                    <Text style={[styles.statText, { color: highFindings.length > 0 ? Colors.danger : Colors.text }]}>
                      {item.findings.length} finding{item.findings.length !== 1 ? 's' : ''}
                    </Text>
                  </View>
                )}
              </View>
            </TouchableOpacity>
          );
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  centered: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  loadingText: { color: Colors.textSecondary },
  list: { padding: 16, paddingBottom: 40 },
  empty: { alignItems: 'center', paddingTop: 80, gap: 12 },
  emptyTitle: { fontSize: 18, fontWeight: '600', color: Colors.text },
  emptyText: { fontSize: 14, color: Colors.textSecondary, textAlign: 'center', lineHeight: 22 },
  card: { backgroundColor: Colors.surface, borderRadius: 12, padding: 14, borderWidth: 1, borderColor: Colors.border, gap: 10 },
  cardHeader: { flexDirection: 'row', gap: 10, alignItems: 'center' },
  iconBox: { width: 38, height: 38, borderRadius: 8, backgroundColor: Colors.primaryLight, alignItems: 'center', justifyContent: 'center' },
  cardInfo: { flex: 1 },
  cardTitle: { fontSize: 15, fontWeight: '600', color: Colors.text },
  cardDate: { fontSize: 12, color: Colors.textSecondary, marginTop: 2 },
  cardStats: { flexDirection: 'row', gap: 16 },
  stat: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  statText: { fontSize: 12, color: Colors.textSecondary },
});
