import React, { useState } from 'react';
import { SafeAreaView } from 'react-native-safe-area-context';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Dimensions,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import {
  mockChildren,
  mockVaccinationRecords,
  mockGrowthRecords,
} from '@/services/mockData';
import { Child, VaccinationRecord, GrowthRecord } from '@/types';
import { LineChart } from 'react-native-chart-kit';
import { useAuth } from '@/app/AuthContext';

const screenWidth = Dimensions.get('window').width;

function getAgeString(child: Child) {
  if (
    child.age_in_years !== undefined &&
    child.age_in_months !== undefined
  ) {
    const months = child.age_in_months % 12;
    return `${child.age_in_years} years${months > 0 ? ` ${months} months` : ''
      }`;
  }
  return '';
}

function getUpcomingVaccines(child: Child) {
  return [
    {
      name: 'MMR',
      description: 'Measles, Mumps, Rubella',
      dueDate: '2025-01-15',
      daysLeft: 12,
    },
    {
      name: 'Varicella',
      description: 'Chickenpox',
      dueDate: '2025-02-20',
      daysLeft: 48,
    },
  ];
}

function getHealthNotes(child: Child) {
  return [
    {
      note: 'No allergic reactions reported',
      date: 'Dec 28, 2024',
      type: 'last',
    },
    {
      note: 'Regular checkup scheduled for next month',
      date: 'Dec 20, 2024',
      type: 'added',
    },
  ];
}

function getGrowthRecords(child: Child): GrowthRecord[] {
  return mockGrowthRecords
    .filter((r) => r.child_id === child.child_id)
    .sort(
      (a, b) =>
        new Date(a.date_recorded).getTime() -
        new Date(b.date_recorded).getTime()
    );
}

export default function Dashboard() {
  const [selectedChildIdx, setSelectedChildIdx] = useState(0);
  const { setLoggedIn } = useAuth();
  const selectedChild = mockChildren[selectedChildIdx];
  const growthRecords = getGrowthRecords(selectedChild);
  const upcomingVaccines = getUpcomingVaccines(selectedChild);
  const healthNotes = getHealthNotes(selectedChild);

  const chartData = {
    labels: growthRecords.map(
      (r) => `${new Date(r.date_recorded).getMonth() + 1}m`
    ),
    datasets: [
      {
        data: growthRecords.map((r) => r.height),
        color: (opacity = 1) => `rgba(74, 144, 226, ${opacity})`,
        strokeWidth: 2,
      },
    ],
  };

  return (
   <SafeAreaView style={{flex:1, backgroundColor: '#fff'}}>
    <ScrollView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.greeting}>Good morning, Parent</Text>
        <View style={styles.headerIcons}>
          <TouchableOpacity onPress={() => alert('Notifications coming soon')}>
            <Ionicons name="notifications-outline" size={24} color="#2a5ca4" />
          </TouchableOpacity>
          <TouchableOpacity
            style={{ marginLeft: 16 }}
            onPress={() => {
              setLoggedIn(false);
            }}
          >
            <Ionicons name="log-out-outline" size={24} color="#2a5ca4" />
          </TouchableOpacity>
        </View>
      </View>

      {/* Profile Card */}
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
          <Text style={styles.profileAge}>Age: {getAgeString(selectedChild)}</Text>
          <Text style={styles.profileDob}>
            DOB: {new Date(selectedChild.date_of_birth).toLocaleDateString()}
          </Text>
        </View>
        <TouchableOpacity
          style={styles.switchChildButton}
          onPress={() =>
            setSelectedChildIdx((selectedChildIdx + 1) % mockChildren.length)
          }
        >
          <Ionicons name="swap-horizontal-outline" size={18} color="#2a5ca4" />
          <Text style={styles.switchChildText}>Switch</Text>
        </TouchableOpacity>
      </View>

      {/* Growth Chart */}
      <View style={styles.sectionCard}>
        <Text style={styles.sectionTitle}>Height Growth Chart</Text>
        <LineChart
          data={chartData}
          width={screenWidth - 48}
          height={180}
          chartConfig={{
            backgroundColor: '#fff',
            backgroundGradientFrom: '#fff',
            backgroundGradientTo: '#fff',
            decimalPlaces: 0,
            color: (opacity = 1) => `rgba(74, 144, 226, ${opacity})`,
            labelColor: (opacity = 1) => `rgba(80, 80, 80, ${opacity})`,
            propsForDots: {
              r: '5',
              strokeWidth: '2',
              stroke: '#4A90E2',
            },
          }}
          bezier
          style={styles.chart}
        />
      </View>

      {/* Upcoming Vaccines */}
      <View style={styles.sectionCard}>
        <Text style={styles.sectionTitle}>Upcoming Vaccines</Text>
        {upcomingVaccines.map((vaccine, idx) => (
          <View key={idx} style={styles.upcomingVaccineRow}>
            <View style={{ flex: 1 }}>
              <Text style={styles.vaccineName}>{vaccine.name} Vaccine</Text>
              <Text style={styles.vaccineDesc}>{vaccine.description}</Text>
            </View>
            <View style={{ alignItems: 'flex-end' }}>
              <Text style={styles.vaccineDueDate}>
                {new Date(vaccine.dueDate).toLocaleDateString()}
              </Text>
              <Text style={styles.vaccineDueIn}>Due in {vaccine.daysLeft} days</Text>
            </View>
          </View>
        ))}
      </View>

      {/* Health Notes */}
      <View style={styles.sectionCard}>
        <Text style={styles.sectionTitle}>Health Notes</Text>
        {healthNotes.map((note, idx) => (
          <View key={idx} style={styles.healthNoteRow}>
            <Text style={styles.healthNoteText}>{note.note}</Text>
            <Text style={styles.healthNoteDate}>
              {note.type === 'last' ? 'Last updated' : 'Added'}: {note.date}
            </Text>
          </View>
        ))}
      </View>

      {/* Vaccine Records (REVISED) */}
      <View style={styles.sectionCard}>
        <Text style={styles.sectionTitle}>Vaccine Records</Text>
        {mockVaccinationRecords.map((record) => (
          <View key={record.recordID} style={styles.vaccineRecordSimpleRow}>
            <View style={{ flex: 1 }}>
              <Text style={styles.vaccineName}>{record.vaccine_name}</Text>
              <Text style={styles.vaccineDesc}>
                {record.doseNumber
                  ? `Dose ${record.doseNumber}`
                  : 'Single dose'}
              </Text>
            </View>
            <View style={{ alignItems: 'flex-end' }}>
              <Text style={styles.vaccineDueDate}>
                {new Date(record.administrationDate).toLocaleDateString()}
              </Text>
              <Text style={styles.vaccineStatus}>Completed</Text>
            </View>
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
    backgroundColor: '#f5f5f5',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#fff',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 2,
  },
  greeting: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2a5ca4',
  },
  headerIcons: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  profileName: {
  fontWeight: 'bold',
  fontSize: 16,
  color: '#1a1a1a',
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
    color: '#4A90E2',
    fontWeight: 'bold',
    fontSize: 20,
  },
  profileInfo: {
    flex: 1,
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
    fontSize: 15,
    marginBottom: 10,
    color: '#222',
  },
  chart: {
    marginVertical: 8,
    borderRadius: 12,
  },
  upcomingVaccineRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
    paddingVertical: 4,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  vaccineName: {
    fontWeight: 'bold',
    fontSize: 14,
    color: '#222',
  },
  vaccineDesc: {
    fontSize: 13,
    color: '#888',
    marginTop: 2,
  },
  vaccineDueDate: {
    fontSize: 13,
    color: '#4A90E2',
    fontWeight: 'bold',
  },
  vaccineDueIn: {
    fontSize: 12,
    color: '#888',
  },
  healthNoteRow: {
    backgroundColor: '#fafbfc',
    borderRadius: 8,
    padding: 10,
    marginBottom: 8,
  },
  healthNoteText: {
    fontSize: 14,
    color: '#222',
  },
  healthNoteDate: {
    fontSize: 12,
    color: '#888',
    marginTop: 2,
  },
  vaccineRecordSimpleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  vaccineStatus: {
    fontSize: 13,
    color: '#27AE60',
    fontWeight: 'bold',
  },
});
