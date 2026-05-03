import { StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '@/constants/Colors';

export default function HistoryScreen() {
  return (
    <View style={styles.container}>
      <Ionicons name="time-outline" size={56} color={Colors.textLight} />
      <Text style={styles.title}>Inspection History</Text>
      <Text style={styles.subtitle}>
        Coming in Lab 6 — Checklists & Findings.{'\n'}
        Completed inspections with findings and reports will appear here.
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 32,
    gap: 12,
  },
  title: { fontSize: 20, fontWeight: '600', color: Colors.text },
  subtitle: {
    fontSize: 14,
    color: Colors.textSecondary,
    textAlign: 'center',
    lineHeight: 22,
  },
});
