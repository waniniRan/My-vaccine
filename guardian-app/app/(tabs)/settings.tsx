import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { mockGuardian, mockChildren } from '@/services/mockData';

export default function SettingsScreen() {
  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: '#fff' }}>
      <ScrollView style={styles.container}>
        {/* Profile Card */}
        <View style={styles.sectionCard}>
          <Text style={styles.sectionTitle}>Parent Profile</Text>
          <View style={styles.itemRow}>
            <Ionicons name="person-outline" size={18} color="#2a5ca4" style={styles.icon} />
            <Text style={styles.itemText}>{mockGuardian.fullname}</Text>
          </View>
          <View style={styles.itemRow}>
            <Ionicons name="card-outline" size={18} color="#2a5ca4" style={styles.icon} />
            <Text style={styles.itemText}>{mockGuardian.national_id}</Text>
          </View>
          <View style={styles.itemRow}>
            <Ionicons name="mail-outline" size={18} color="#2a5ca4" style={styles.icon} />
            <Text style={styles.itemText}>{mockGuardian.email}</Text>
          </View>
          <View style={styles.itemRow}>
            <Ionicons name="call-outline" size={18} color="#2a5ca4" style={styles.icon} />
            <Text style={styles.itemText}>{mockGuardian.phone_number}</Text>
          </View>
        </View>

        {/* Children Section */}
        <View style={styles.sectionCard}>
          <Text style={styles.sectionTitle}>Children</Text>
          {mockChildren.map(child => (
            <View key={child.child_id} style={styles.itemRow}>
              <Ionicons name="person-circle-outline" size={18} color="#2a5ca4" style={styles.icon} />
              <Text style={styles.itemText}>{child.first_name} {child.last_name}</Text>
            </View>
          ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  sectionCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginHorizontal: 12,
    marginTop: 12,
    marginBottom: 14,
    borderWidth: 1,
    borderColor: '#e0e0e0',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 3.84,
    elevation: 2,
  },
  sectionTitle: {
    fontWeight: 'bold',
    fontSize: 16,
    marginBottom: 12,
    color: '#222',
  },
  itemRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  itemText: {
    fontSize: 14,
    color: '#333',
  },
  icon: {
    marginRight: 8,
  },
});
