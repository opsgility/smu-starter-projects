import { FlatList, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '@/constants/Colors';
import { useEquipment } from '@/hooks/useEquipment';
import { useInspection } from '@/hooks/useInspection';

export default function NewInspectionScreen() {
  const router = useRouter();
  const { equipment } = useEquipment();
  const { startInspection } = useInspection();

  const activeEquipment = equipment.filter(e => e.status === 'active');

  const handleSelect = async (id: string, name: string) => {
    const inspection = await startInspection(id, name);
    router.replace(`/inspection/${inspection.id}`);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.prompt}>Select equipment to inspect:</Text>
      {activeEquipment.length === 0 ? (
        <View style={styles.empty}>
          <Ionicons name="cube-outline" size={48} color={Colors.textLight} />
          <Text style={styles.emptyText}>No active equipment found.{'\n'}Add equipment in the Equipment tab first.</Text>
        </View>
      ) : (
        <FlatList
          data={activeEquipment}
          keyExtractor={item => item.id}
          contentContainerStyle={styles.list}
          ItemSeparatorComponent={() => <View style={{ height: 10 }} />}
          renderItem={({ item }) => (
            <TouchableOpacity style={styles.row} onPress={() => handleSelect(item.id, item.name)} activeOpacity={0.7}>
              <View style={styles.iconBox}>
                <Ionicons name="cube" size={22} color={Colors.primary} />
              </View>
              <View style={styles.info}>
                <Text style={styles.name}>{item.name}</Text>
                <Text style={styles.meta}>{item.type} · {item.location}</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color={Colors.textLight} />
            </TouchableOpacity>
          )}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  prompt: { fontSize: 14, color: Colors.textSecondary, padding: 16, paddingBottom: 8 },
  list: { padding: 16, paddingTop: 0 },
  empty: { flex: 1, alignItems: 'center', justifyContent: 'center', gap: 12 },
  emptyText: { fontSize: 14, color: Colors.textSecondary, textAlign: 'center', lineHeight: 22 },
  row: { flexDirection: 'row', alignItems: 'center', gap: 12, backgroundColor: Colors.surface, borderRadius: 12, padding: 14, borderWidth: 1, borderColor: Colors.border },
  iconBox: { width: 40, height: 40, borderRadius: 8, backgroundColor: Colors.primaryLight, alignItems: 'center', justifyContent: 'center' },
  info: { flex: 1 },
  name: { fontSize: 15, fontWeight: '600', color: Colors.text },
  meta: { fontSize: 12, color: Colors.textSecondary, marginTop: 2 },
});
