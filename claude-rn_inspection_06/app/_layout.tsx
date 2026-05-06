import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { Colors } from '@/constants/Colors';

export default function RootLayout() {
  return (
    <>
      <Stack
        screenOptions={{
          headerStyle: { backgroundColor: Colors.primary },
          headerTintColor: '#fff',
          headerTitleStyle: { fontWeight: '600' },
        }}
      >
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="equipment/add" options={{ title: 'Add Equipment', presentation: 'modal' }} />
        <Stack.Screen name="equipment/[id]" options={{ title: 'Edit Equipment' }} />
        <Stack.Screen name="inspection/new" options={{ title: 'New Inspection', presentation: 'modal' }} />
        <Stack.Screen name="inspection/[id]/index" options={{ title: 'Inspection' }} />
        <Stack.Screen name="inspection/[id]/analyze" options={{ title: 'AI Analysis' }} />
        <Stack.Screen name="inspection/[id]/checklist" options={{ title: 'Checklist & Findings' }} />
      </Stack>
      <StatusBar style="light" />
    </>
  );
}
