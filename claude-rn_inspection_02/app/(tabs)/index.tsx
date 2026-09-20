import { ScrollView, StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '@/constants/Colors';

const milestones = [
  { lab: 'Lab 2', name: 'Setup & Navigation', desc: 'Tab navigation and screen structure' },
  { lab: 'Lab 3', name: 'Equipment Management', desc: 'CRUD operations with AsyncStorage' },
  { lab: 'Lab 4', name: 'Camera & Photos', desc: 'Photo capture during inspections' },
  { lab: 'Lab 5', name: 'Claude Vision AI', desc: 'AI-powered defect analysis' },
  { lab: 'Lab 6', name: 'Checklists & Findings', desc: 'Structured inspection workflows' },
  { lab: 'Lab 7', name: 'PDF Reports', desc: 'Generate and share inspection reports' },
];

export default function DashboardScreen() {
  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.title}>InspectAI</Text>
        <Text style={styles.subtitle}>AI-Powered Field Inspections</Text>
      </View>

      <View style={styles.heroCard}>
        <Ionicons name="construct-outline" size={56} color={Colors.primary} />
        <Text style={styles.heroTitle}>Starter Project Ready</Text>
        <Text style={styles.heroText}>
          Use Claude Code to build InspectAI step by step. Each lab adds a new
          layer of functionality — from navigation to AI-powered defect detection.
        </Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Course Roadmap</Text>
        {milestones.map((m) => (
          <View key={m.lab} style={styles.milestoneRow}>
            <View style={styles.labBadge}>
              <Text style={styles.labBadgeText}>{m.lab}</Text>
            </View>
            <View style={styles.milestoneContent}>
              <Text style={styles.milestoneName}>{m.name}</Text>
              <Text style={styles.milestoneDesc}>{m.desc}</Text>
            </View>
          </View>
        ))}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  content: { padding: 20, paddingBottom: 40 },
  header: { marginBottom: 24 },
  title: { fontSize: 28, fontWeight: '700', color: Colors.text },
  subtitle: { fontSize: 14, color: Colors.textSecondary, marginTop: 4 },
  heroCard: {
    backgroundColor: Colors.surface,
    borderRadius: 16,
    padding: 24,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: Colors.border,
    marginBottom: 24,
    gap: 12,
  },
  heroTitle: { fontSize: 20, fontWeight: '700', color: Colors.text },
  heroText: {
    fontSize: 14,
    color: Colors.textSecondary,
    textAlign: 'center',
    lineHeight: 22,
  },
  section: { gap: 10 },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: Colors.text,
    marginBottom: 4,
  },
  milestoneRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.surface,
    borderRadius: 10,
    padding: 14,
    borderWidth: 1,
    borderColor: Colors.border,
    gap: 14,
  },
  labBadge: {
    backgroundColor: Colors.primaryLight,
    borderRadius: 8,
    paddingHorizontal: 10,
    paddingVertical: 6,
    minWidth: 52,
    alignItems: 'center',
  },
  labBadgeText: { fontSize: 11, fontWeight: '700', color: Colors.primary },
  milestoneContent: { flex: 1 },
  milestoneName: { fontSize: 14, fontWeight: '600', color: Colors.text },
  milestoneDesc: { fontSize: 12, color: Colors.textSecondary, marginTop: 2 },
});
