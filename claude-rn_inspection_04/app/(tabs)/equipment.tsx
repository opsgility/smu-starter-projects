import { FlatList, StyleSheet, Text, TouchableOpacity, View, Alert } from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '@/constants/Colors';
import { EquipmentCard } from '@/components/EquipmentCard';
import { useEquipment } from '@/hooks/useEquipment';

export default function EquipmentScreen() {
  const router = useRouter();
  const { equipment, loading, deleteEquipment } = useEquipment();

  const confirmDelete = (id: string, name: string) => {
    Alert.alert('Delete Equipment', `Remove "${name}"?`, [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Delete', style: 'destructive', onPress: () => deleteEquipment(id) },
    ]);
  };

  if (loading) {
    return (
      <View style={styles.centered}>
        <Text style={styles.loadingText}>Loading...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={equipment}
        keyExtractor={item => item.id}
        contentContainerStyle={styles.list}
        ItemSeparatorComponent={() => <View style={{ height: 10 }} />}
        ListEmptyComponent={
          <View style={styles.empty}>
            <Ionicons name="cube-outline" size={56} color={Colors.textLight} />
            <Text style={styles.emptyTitle}>No Equipment Yet</Text>
            <Text style={styles.emptyText}>Add your first piece of equipment to start tracking inspections.</Text>
          </View>
        }
        renderItem={({ item }) => (
          <EquipmentCard
            item={item}
            onPress={() => router.push(`/equipment/${item.id}`)}
            onDelete={() => confirmDelete(item.id, item.name)}
          />
        )}
      />
      <TouchableOpacity style={styles.fab} onPress={() => router.push('/equipment/add')}>
        <Ionicons name="add" size={28} color="#fff" />
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  centered: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  loadingText: { color: Colors.textSecondary },
  list: { padding: 16, paddingBottom: 100 },
  empty: { alignItems: 'center', paddingTop: 80, gap: 12 },
  emptyTitle: { fontSize: 18, fontWeight: '600', color: Colors.text },
  emptyText: { fontSize: 14, color: Colors.textSecondary, textAlign: 'center', lineHeight: 22 },
  fab: {
    position: 'absolute',
    bottom: 24,
    right: 24,
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: Colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.2,
    shadowRadius: 6,
    elevation: 6,
  },
});
