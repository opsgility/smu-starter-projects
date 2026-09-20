import { useState } from 'react';
import { ActivityIndicator, ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { useLocalSearchParams } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import * as Print from 'expo-print';
import * as Sharing from 'expo-sharing';
import { Colors } from '@/constants/Colors';
import { useInspection } from '@/hooks/useInspection';
import { generateReportHtml } from '@/services/reportGenerator';

export default function ReportScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const { getInspection } = useInspection();
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const inspection = getInspection(id);

  if (!inspection) {
    return (
      <View style={styles.centered}>
        <Text style={styles.notFound}>Inspection not found.</Text>
      </View>
    );
  }

  const checkedCount = inspection.checklistItems.filter(c => c.checked).length;
  const highFindings = inspection.findings.filter(f => f.severity === 'high' || f.severity === 'critical');

  const handleGeneratePdf = async () => {
    setGenerating(true);
    setError(null);
    try {
      const html = generateReportHtml(inspection);
      const { uri } = await Print.printToFileAsync({ html, base64: false });

      const canShare = await Sharing.isAvailableAsync();
      if (canShare) {
        await Sharing.shareAsync(uri, {
          mimeType: 'application/pdf',
          dialogTitle: `Inspection Report — ${inspection.equipmentName}`,
          UTI: 'com.adobe.pdf',
        });
      } else {
        setError('Sharing is not available on this device.');
      }
    } catch (e: any) {
      setError(e.message ?? 'Failed to generate PDF.');
    } finally {
      setGenerating(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.previewCard}>
        <Ionicons name="document-text" size={48} color={Colors.primary} />
        <Text style={styles.previewTitle}>{inspection.equipmentName}</Text>
        <Text style={styles.previewDate}>
          {inspection.completedAt
            ? new Date(inspection.completedAt).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
            : 'In Progress'}
        </Text>
      </View>

      <View style={styles.summaryRow}>
        <View style={styles.summaryCard}>
          <Text style={styles.summaryNum}>{inspection.photos.length}</Text>
          <Text style={styles.summaryLabel}>Photos</Text>
        </View>
        <View style={styles.summaryCard}>
          <Text style={styles.summaryNum}>{checkedCount}/{inspection.checklistItems.length}</Text>
          <Text style={styles.summaryLabel}>Checklist</Text>
        </View>
        <View style={styles.summaryCard}>
          <Text style={[styles.summaryNum, { color: inspection.findings.length > 0 ? (highFindings.length > 0 ? Colors.danger : Colors.warning) : Colors.success }]}>
            {inspection.findings.length}
          </Text>
          <Text style={styles.summaryLabel}>Findings</Text>
        </View>
      </View>

      {inspection.findings.length > 0 && (
        <View style={styles.findingsPreview}>
          <Text style={styles.sectionTitle}>Findings Summary</Text>
          {inspection.findings.map(f => (
            <View key={f.id} style={styles.findingRow}>
              <Ionicons
                name="warning"
                size={14}
                color={f.severity === 'high' || f.severity === 'critical' ? Colors.danger : Colors.warning}
              />
              <Text style={styles.findingTitle}>{f.title}</Text>
              <Text style={styles.findingSeverity}>{f.severity}</Text>
            </View>
          ))}
        </View>
      )}

      {error && (
        <View style={styles.errorCard}>
          <Ionicons name="alert-circle" size={16} color={Colors.danger} />
          <Text style={styles.errorText}>{error}</Text>
        </View>
      )}

      <TouchableOpacity
        style={[styles.generateBtn, generating && styles.disabled]}
        onPress={handleGeneratePdf}
        disabled={generating}
      >
        {generating ? (
          <>
            <ActivityIndicator color="#fff" size="small" />
            <Text style={styles.generateBtnText}>Generating PDF...</Text>
          </>
        ) : (
          <>
            <Ionicons name="share" size={20} color="#fff" />
            <Text style={styles.generateBtnText}>Generate & Share PDF</Text>
          </>
        )}
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  content: { padding: 20, paddingBottom: 40, gap: 16 },
  centered: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  notFound: { color: Colors.textSecondary },
  previewCard: { backgroundColor: Colors.surface, borderRadius: 16, padding: 24, alignItems: 'center', gap: 8, borderWidth: 1, borderColor: Colors.border },
  previewTitle: { fontSize: 18, fontWeight: '700', color: Colors.text },
  previewDate: { fontSize: 13, color: Colors.textSecondary },
  summaryRow: { flexDirection: 'row', gap: 12 },
  summaryCard: { flex: 1, backgroundColor: Colors.surface, borderRadius: 12, padding: 14, alignItems: 'center', borderWidth: 1, borderColor: Colors.border },
  summaryNum: { fontSize: 22, fontWeight: '700', color: Colors.primary },
  summaryLabel: { fontSize: 11, color: Colors.textSecondary, marginTop: 2 },
  findingsPreview: { backgroundColor: Colors.surface, borderRadius: 12, padding: 16, borderWidth: 1, borderColor: Colors.border, gap: 10 },
  sectionTitle: { fontSize: 14, fontWeight: '600', color: Colors.text, marginBottom: 4 },
  findingRow: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  findingTitle: { flex: 1, fontSize: 13, color: Colors.text },
  findingSeverity: { fontSize: 11, color: Colors.textSecondary, textTransform: 'capitalize' },
  errorCard: { flexDirection: 'row', gap: 8, padding: 12, backgroundColor: Colors.dangerLight, borderRadius: 10 },
  errorText: { flex: 1, color: Colors.danger, fontSize: 13 },
  generateBtn: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, backgroundColor: Colors.primary, borderRadius: 12, padding: 16 },
  disabled: { opacity: 0.6 },
  generateBtnText: { color: '#fff', fontSize: 16, fontWeight: '700' },
});
