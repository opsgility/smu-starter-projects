import { StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '@/constants/Colors';

export default function HistoryScreen() {
  return (
    <View style={styles.container}>
      <View style={styles.empty}>
        <Ionicons name="time-outline" size={56} color={Colors.textLight} />
        <Text style={styles.emptyTitle}>History</Text>
        <Text style={styles.emptyText}>Completed inspections will appear here.</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  empty: { alignItems: 'center', paddingTop: 80, gap: 12 },
  emptyTitle: { fontSize: 18, fontWeight: '600', color: Colors.text },
  emptyText: { fontSize: 14, color: Colors.textSecondary, textAlign: 'center', lineHeight: 22 },
});
