import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '@/constants/Colors';
import { Equipment, EquipmentStatus } from '@/types';

const STATUS_COLORS: Record<EquipmentStatus, string> = {
  active: Colors.success,
  inactive: Colors.textLight,
  maintenance: Colors.warning,
  retired: Colors.danger,
};

const STATUS_LABELS: Record<EquipmentStatus, string> = {
  active: 'Active',
  inactive: 'Inactive',
  maintenance: 'Maintenance',
  retired: 'Retired',
};

interface Props {
  item: Equipment;
  onPress: () => void;
  onDelete: () => void;
}

export function EquipmentCard({ item, onPress, onDelete }: Props) {
  return (
    <TouchableOpacity style={styles.card} onPress={onPress} activeOpacity={0.7}>
      <View style={styles.row}>
        <View style={styles.iconBox}>
          <Ionicons name="cube" size={24} color={Colors.primary} />
        </View>
        <View style={styles.info}>
          <Text style={styles.name}>{item.name}</Text>
          <Text style={styles.meta}>{item.type} · {item.location}</Text>
          {item.serialNumber ? (
            <Text style={styles.serial}>S/N: {item.serialNumber}</Text>
          ) : null}
        </View>
        <View style={styles.right}>
          <View style={[styles.badge, { backgroundColor: STATUS_COLORS[item.status] + '22' }]}>
            <Text style={[styles.badgeText, { color: STATUS_COLORS[item.status] }]}>
              {STATUS_LABELS[item.status]}
            </Text>
          </View>
          <TouchableOpacity onPress={onDelete} style={styles.deleteBtn} hitSlop={8}>
            <Ionicons name="trash-outline" size={18} color={Colors.danger} />
          </TouchableOpacity>
        </View>
      </View>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: Colors.surface,
    borderRadius: 12,
    padding: 14,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  row: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  iconBox: {
    width: 44,
    height: 44,
    borderRadius: 10,
    backgroundColor: Colors.primaryLight,
    alignItems: 'center',
    justifyContent: 'center',
  },
  info: { flex: 1 },
  name: { fontSize: 15, fontWeight: '600', color: Colors.text },
  meta: { fontSize: 12, color: Colors.textSecondary, marginTop: 2 },
  serial: { fontSize: 11, color: Colors.textLight, marginTop: 1 },
  right: { alignItems: 'flex-end', gap: 8 },
  badge: { borderRadius: 6, paddingHorizontal: 8, paddingVertical: 3 },
  badgeText: { fontSize: 11, fontWeight: '600' },
  deleteBtn: { padding: 4 },
});
