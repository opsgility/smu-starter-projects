import { useState } from 'react';
import { ActivityIndicator, Image, ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { useLocalSearchParams } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '@/constants/Colors';
import { useInspection } from '@/hooks/useInspection';
import { useEquipment } from '@/hooks/useEquipment';
import { analyzeInspectionPhoto } from '@/services/claudeVision';
import { PhotoAnalysis } from '@/types';

const CONDITION_COLORS = {
  good: Colors.success,
  fair: Colors.warning,
  poor: Colors.danger,
  critical: '#7C0A02',
};

const URGENCY_COLORS = {
  routine: Colors.success,
  soon: Colors.warning,
  immediate: Colors.danger,
};

export default function AnalyzeScreen() {
  const { id, photoId } = useLocalSearchParams<{ id: string; photoId: string }>();
  const { getInspection, updatePhotoAnalysis, reload } = useInspection();
  const { getEquipment } = useEquipment();
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const inspection = getInspection(id);
  const photo = inspection?.photos.find(p => p.id === photoId);
  const equipment = inspection ? getEquipment(inspection.equipmentId) : undefined;

  if (!inspection || !photo) {
    return (
      <View style={styles.centered}>
        <Text style={styles.notFound}>Photo not found.</Text>
      </View>
    );
  }

  const handleAnalyze = async () => {
    const apiKey = process.env.EXPO_PUBLIC_CLAUDE_API_KEY;
    if (!apiKey) {
      setError('EXPO_PUBLIC_CLAUDE_API_KEY is not set. Add it to your .env file.');
      return;
    }
    setAnalyzing(true);
    setError(null);
    try {
      const analysis = await analyzeInspectionPhoto(
        photo.uri,
        inspection.equipmentName,
        equipment?.type ?? 'general',
        apiKey
      );
      await updatePhotoAnalysis(id, photoId, analysis);
      await reload();
    } catch (e: any) {
      setError(e.message ?? 'Analysis failed.');
    } finally {
      setAnalyzing(false);
    }
  };

  const analysis: PhotoAnalysis | undefined = photo.analysis;

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Image source={{ uri: photo.uri }} style={styles.photo} resizeMode="cover" />

      {error && (
        <View style={styles.errorCard}>
          <Ionicons name="alert-circle" size={20} color={Colors.danger} />
          <Text style={styles.errorText}>{error}</Text>
        </View>
      )}

      {!analysis && !analyzing && (
        <TouchableOpacity style={styles.analyzeBtn} onPress={handleAnalyze}>
          <Ionicons name="sparkles" size={20} color="#fff" />
          <Text style={styles.analyzeBtnText}>Analyze with Claude Vision</Text>
        </TouchableOpacity>
      )}

      {analyzing && (
        <View style={styles.loadingCard}>
          <ActivityIndicator color={Colors.primary} size="large" />
          <Text style={styles.loadingText}>Analyzing photo with Claude Vision AI...</Text>
        </View>
      )}

      {analysis && (
        <>
          <View style={styles.resultCard}>
            <View style={styles.resultHeader}>
              <View style={[styles.conditionBadge, { backgroundColor: CONDITION_COLORS[analysis.condition] }]}>
                <Text style={styles.conditionText}>{analysis.condition.toUpperCase()}</Text>
              </View>
              <View style={[styles.urgencyBadge, { backgroundColor: URGENCY_COLORS[analysis.urgency] + '22' }]}>
                <Text style={[styles.urgencyText, { color: URGENCY_COLORS[analysis.urgency] }]}>
                  {analysis.urgency} attention
                </Text>
              </View>
            </View>
            <Text style={styles.summary}>{analysis.summary}</Text>
          </View>

          {analysis.defects.length > 0 && (
            <View style={styles.listCard}>
              <Text style={styles.listTitle}>Defects Observed</Text>
              {analysis.defects.map((d, i) => (
                <View key={i} style={styles.listRow}>
                  <Ionicons name="warning" size={14} color={Colors.warning} />
                  <Text style={styles.listText}>{d}</Text>
                </View>
              ))}
            </View>
          )}

          {analysis.recommendations.length > 0 && (
            <View style={styles.listCard}>
              <Text style={styles.listTitle}>Recommendations</Text>
              {analysis.recommendations.map((r, i) => (
                <View key={i} style={styles.listRow}>
                  <Ionicons name="checkmark-circle" size={14} color={Colors.success} />
                  <Text style={styles.listText}>{r}</Text>
                </View>
              ))}
            </View>
          )}

          <TouchableOpacity style={styles.reanalyzeBtn} onPress={handleAnalyze}>
            <Text style={styles.reanalyzeBtnText}>Re-analyze</Text>
          </TouchableOpacity>
        </>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  content: { paddingBottom: 40 },
  centered: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  notFound: { color: Colors.textSecondary },
  photo: { width: '100%', height: 240 },
  errorCard: { flexDirection: 'row', gap: 8, margin: 16, padding: 14, backgroundColor: Colors.dangerLight, borderRadius: 10 },
  errorText: { flex: 1, color: Colors.danger, fontSize: 13 },
  analyzeBtn: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, margin: 16, backgroundColor: Colors.primary, borderRadius: 12, padding: 16 },
  analyzeBtnText: { color: '#fff', fontSize: 16, fontWeight: '700' },
  loadingCard: { margin: 16, padding: 32, alignItems: 'center', gap: 16, backgroundColor: Colors.surface, borderRadius: 12, borderWidth: 1, borderColor: Colors.border },
  loadingText: { color: Colors.textSecondary, textAlign: 'center' },
  resultCard: { margin: 16, marginBottom: 0, padding: 16, backgroundColor: Colors.surface, borderRadius: 12, borderWidth: 1, borderColor: Colors.border, gap: 10 },
  resultHeader: { flexDirection: 'row', gap: 10 },
  conditionBadge: { borderRadius: 6, paddingHorizontal: 10, paddingVertical: 4 },
  conditionText: { color: '#fff', fontSize: 12, fontWeight: '700' },
  urgencyBadge: { borderRadius: 6, paddingHorizontal: 10, paddingVertical: 4 },
  urgencyText: { fontSize: 12, fontWeight: '600' },
  summary: { fontSize: 14, color: Colors.text, lineHeight: 20 },
  listCard: { margin: 16, marginBottom: 0, padding: 16, backgroundColor: Colors.surface, borderRadius: 12, borderWidth: 1, borderColor: Colors.border, gap: 8 },
  listTitle: { fontSize: 14, fontWeight: '600', color: Colors.text, marginBottom: 4 },
  listRow: { flexDirection: 'row', gap: 8, alignItems: 'flex-start' },
  listText: { flex: 1, fontSize: 13, color: Colors.textSecondary, lineHeight: 18 },
  reanalyzeBtn: { margin: 16, padding: 14, borderRadius: 10, borderWidth: 1, borderColor: Colors.border, alignItems: 'center' },
  reanalyzeBtnText: { color: Colors.textSecondary, fontWeight: '600' },
});
