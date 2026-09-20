import { StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '@/constants/Colors';

export default function EquipmentScreen() {
  return (
    <View style={styles.container}>
      <Ionicons name="cube-outline" size={56} color={Colors.textLight} />
      <Text style={styles.title}>Equipment</Text>
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
});
