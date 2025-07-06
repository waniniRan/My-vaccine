import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { mockGrowthRecords, mockChildren } from '@/services/mockData';
import { GrowthRecord, Child } from '@/types';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function GrowthScreen() {
  const [selectedChildIdx, setSelectedChildIdx] = useState(0);

  const selectedChild = mockChildren[selectedChildIdx];

  const filteredRecords = mockGrowthRecords.filter(
    record => record.child_id === selectedChild.child_id
  );

  return (
   <SafeAreaView style={{ flex: 1, backgroundColor: '#fff' }}> 
    <ScrollView style={styles.container}>
      {/* Profile Card with Switch */}
      <View style={styles.profileCard}>
        <View style={styles.profileAvatar}>
          <Text style={styles.avatarText}>
            {selectedChild.first_name.charAt(0)}
            {selectedChild.last_name.charAt(0)}
          </Text>
        </View>
        <View style={styles.profileInfo}>
          <Text style={styles.profileName}>
            {selectedChild.first_name} {selectedChild.last_name}
          </Text>
          <Text style={styles.profileAge}>
            Age: {selectedChild.age_in_years} years
          </Text>
          <Text style={styles.profileDob}>
            DOB: {new Date(selectedChild.date_of_birth).toLocaleDateString()}
          </Text>
        </View>
        <TouchableOpacity
          style={styles.switchChildButton}
          onPress={() => {
            setSelectedChildIdx((selectedChildIdx + 1) % mockChildren.length);
          }}
        >
          <Ionicons name="swap-horizontal-outline" size={18} color="#2a5ca4" />
          <Text style={styles.switchChildText}>Switch</Text>
        </TouchableOpacity>
      </View>

      {/* Growth Records */}
      <View style={styles.sectionCard}>
        <Text style={styles.sectionTitle}>Growth Measurements</Text>
        {filteredRecords.length > 0 ? (
          filteredRecords.map(record => (
            <View
            key={`${record.child_id}-${record.date_recorded}-${record.weight}-${record.height}`}
             style={styles.recordRow}>
              <View style={{ flex: 1 }}>
                <Text style={styles.recordDate}>
                  {new Date(record.date_recorded).toLocaleDateString()}
                </Text>
                <Text style={styles.recordNote}>
                  {record.notes || "No additional notes"}
                </Text>
              </View>
              <View style={styles.recordStats}>
                <Text style={styles.statLabel}>W</Text>
                <Text style={styles.statValue}>{record.weight} kg</Text>
                <Text style={styles.statLabel}>H</Text>
                <Text style={styles.statValue}>{record.height} cm</Text>
              </View>
            </View>
          ))
        ) : (
          <Text style={styles.emptyText}>No growth records found.</Text>
        )}
      </View>
    </ScrollView>
   </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  profileCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginHorizontal: 12,
    marginTop: 12,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 3.84,
    elevation: 2,
  },
  profileAvatar: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: '#e0e6f7',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  avatarText: {
    color: '#2a5ca4',
    fontWeight: 'bold',
    fontSize: 20,
  },
  profileInfo: {
    flex: 1,
  },
  profileName: {
    fontWeight: 'bold',
    fontSize: 16,
    color: '#2a5ca4',
  },
  profileAge: {
    fontSize: 14,
    color: '#333',
    marginTop: 2,
  },
  profileDob: {
    fontSize: 13,
    color: '#555',
    marginTop: 2,
  },
  switchChildButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f0f4fa',
    borderRadius: 8,
    paddingVertical: 4,
    paddingHorizontal: 8,
    marginLeft: 8,
  },
  switchChildText: {
    marginLeft: 4,
    color: '#2a5ca4',
    fontSize: 12,
  },
  sectionCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginHorizontal: 12,
    marginBottom: 14,
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
  recordRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomColor: '#f0f0f0',
    borderBottomWidth: 1,
  },
  recordDate: {
    fontSize: 14,
    color: '#2a5ca4',
    fontWeight: 'bold',
  },
  recordNote: {
    fontSize: 12,
    color: '#666',
    marginTop: 2,
  },
  recordStats: {
    alignItems: 'flex-end',
  },
  statLabel: {
    fontSize: 10,
    color: '#888',
  },
  statValue: {
    fontSize: 14,
    color: '#222',
    fontWeight: 'bold',
  },
  emptyText: {
    textAlign: 'center',
    color: '#888',
    marginTop: 12,
  },
});
