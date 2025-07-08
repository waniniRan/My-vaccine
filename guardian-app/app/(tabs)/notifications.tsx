import React, { useEffect, useState, useCallback } from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';
import { guardianService } from '../../services/guardianService';
import { useAuth } from '../AuthContext';

const NotificationsTab = () => {
  const { user } = useAuth();
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  const fetchNotifications = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await guardianService.getNotifications();
      setNotifications(data);
    } catch (err) {
      setError('Failed to load notifications.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchNotifications();
  }, [fetchNotifications]);

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchNotifications();
    setRefreshing(false);
  };

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: '#fff' }}>
      <ScrollView style={styles.container}>
        <Text style={styles.headerTitle}>Notifications</Text>
        {notifications.map((notif) => (
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
};

export default NotificationsTab;

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
