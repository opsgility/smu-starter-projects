import { ScrollView, StyleSheet, Text, TouchableOpacity, View, Image, Alert } from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';
import { Colors } from '@/constants/Colors';
import { useInspection } from '@/hooks/useInspection';

export default function InspectionDetailScreen() {
  const router = useRouter();
  const { id } = useLocalSearchParams<{ id: string }>();
  const { getInspection, addPhoto, removePhoto, completeInspection, reload } = useInspection();
  const inspection = getInspection(id);

  if (!inspection) {
    return (
      <View style={styles.centered}>
        <Text style={styles.notFound}>Inspection not found.</Text>
      </View>
    );
  }

  const handleAddPhoto = async () => {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission Required', 'Camera access is needed to take inspection photos.');
      return;
    }
    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: ['images'],
      quality: 0.8,
      allowsEditing: false,
    });
    if (!result.canceled && result.assets[0]) {
      await addPhoto(id, result.assets[0].uri);
      await reload();
    }
  };

  const handleAddFromLibrary = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission Required', 'Photo library access is needed.');
      return;
    }
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ['images'],
      quality: 0.8,
    });
    if (!result.canceled && result.assets[0]) {
      await addPhoto(id, result.assets[0].uri);
      await reload();
    }
  };

  const confirmDeletePhoto = (photoId: string) => {
    Alert.alert('Remove Photo', 'Delete this photo?', [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Delete', style: 'destructive', onPress: async () => { await removePhoto(id, photoId); await reload(); } },
    ]);
  };

  const handleComplete = () => {
    Alert.alert('Complete Inspection', 'Mark this inspection as complete?', [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Complete', onPress: async () => { await completeInspection(id); router.back(); } },
    ]);
  };

  const isActive = inspection.status === 'in_progress';

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.infoCard}>
        <Text style={styles.equipmentName}>{inspection.equipmentName}</Text>
        <View style={styles.statusRow}>
          <View style={[styles.statusBadge, { backgroundColor: isActive ? Colors.successLight : Colors.border }]}>
            <Text style={[styles.statusText, { color: isActive ? Colors.success : Colors.textSecondary }]}>
              {isActive ? 'In Progress' : 'Completed'}
            </Text>
          </View>
          <Text style={styles.dateText}>{new Date(inspection.startedAt).toLocaleDateString()}</Text>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Photos ({inspection.photos.length})</Text>
        <View style={styles.photoGrid}>
          {inspection.photos.map(photo => (
            <TouchableOpacity
              key={photo.id}
              style={styles.photoThumb}
              onLongPress={() => confirmDeletePhoto(photo.id)}
            >
              <Image source={{ uri: photo.uri }} style={styles.photoImage} />
            </TouchableOpacity>
          ))}
        </View>
        {isActive && (
          <View style={styles.photoButtons}>
            <TouchableOpacity style={styles.photoBtn} onPress={handleAddPhoto}>
              <Ionicons name="camera" size={20} color={Colors.primary} />
              <Text style={styles.photoBtnText}>Camera</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.photoBtn} onPress={handleAddFromLibrary}>
              <Ionicons name="images" size={20} color={Colors.primary} />
              <Text style={styles.photoBtnText}>Library</Text>
            </TouchableOpacity>
          </View>
        )}
      </View>

      {isActive && (
        <TouchableOpacity style={styles.completeBtn} onPress={handleComplete}>
          <Ionicons name="checkmark-circle" size={20} color="#fff" />
          <Text style={styles.completeBtnText}>Complete Inspection</Text>
        </TouchableOpacity>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  content: { padding: 16, paddingBottom: 40, gap: 16 },
  centered: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  notFound: { color: Colors.textSecondary },
  infoCard: { backgroundColor: Colors.surface, borderRadius: 12, padding: 16, borderWidth: 1, borderColor: Colors.border },
  equipmentName: { fontSize: 18, fontWeight: '700', color: Colors.text, marginBottom: 8 },
  statusRow: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  statusBadge: { borderRadius: 6, paddingHorizontal: 10, paddingVertical: 4 },
  statusText: { fontSize: 12, fontWeight: '600' },
  dateText: { fontSize: 12, color: Colors.textSecondary },
  section: { backgroundColor: Colors.surface, borderRadius: 12, padding: 16, borderWidth: 1, borderColor: Colors.border, gap: 12 },
  sectionTitle: { fontSize: 15, fontWeight: '600', color: Colors.text },
  photoGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  photoThumb: { width: 88, height: 88, borderRadius: 8, overflow: 'hidden', backgroundColor: Colors.border },
  photoImage: { width: '100%', height: '100%' },
  photoButtons: { flexDirection: 'row', gap: 12 },
  photoBtn: { flex: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 6, borderWidth: 1, borderColor: Colors.primary, borderRadius: 10, padding: 12 },
  photoBtnText: { color: Colors.primary, fontWeight: '600' },
  completeBtn: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, backgroundColor: Colors.success, borderRadius: 12, padding: 16 },
  completeBtnText: { color: '#fff', fontSize: 16, fontWeight: '700' },
});
