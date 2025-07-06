import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';
// For now, using mock notifications
const mockNotifications = [
  {
    id: 1,
    type: 'Vaccine Due',
    message: 'MMR vaccine due in 5 days for John.',
    date: '2025-07-10',
  },
  {
    id: 2,
    type: 'Appointment Reminder',
    message: 'Routine checkup scheduled for July 15th.',
    date: '2025-07-05',
  },
];

export default function NotificationsScreen() {
 return (
  <SafeAreaView style={{ flex: 1, backgroundColor: '#fff' }}>
    <ScrollView style={styles.container}>
      <Text style={styles.headerTitle}>Notifications</Text>
      {mockNotifications.map((notif) => (
        <View key={notif.id} style={styles.notificationCard}>
          <View style={styles.cardHeader}>
            <Ionicons
              name="notifications-outline"
              size={20}
              color="#2a5ca4"
              style={{ marginRight: 6 }}
            />
            <Text style={styles.notifType}>{notif.type}</Text>
          </View>
          <Text style={styles.notifMessage}>{notif.message}</Text>
          <Text style={styles.notifDate}>
            {new Date(notif.date).toLocaleDateString()}
          </Text>
        </View>
      ))}
    </ScrollView>
  </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#f5f5f5',
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 16,
    color: '#2a5ca4',
  },
  notificationCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 14,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 3.84,
    elevation: 2,
    borderColor: '#e0e0e0',
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  notifType: {
    fontWeight: 'bold',
    fontSize: 14,
    color: '#222',
  },
  notifMessage: {
    fontSize: 14,
    color: '#333',
    marginBottom: 4,
  },
  notifDate: {
    fontSize: 12,
    color: '#888',
  },
});
