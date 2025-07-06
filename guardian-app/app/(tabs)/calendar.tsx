import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Calendar, DateData } from 'react-native-calendars';
import { mockVaccinationRecords } from '@/services/mockData';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function CalendarScreen() {
  // get vaccination dates
  const markedDates: Record<string, any> = {};

  mockVaccinationRecords.forEach(record => {
    const date = record.administrationDate.split('T')[0]; // yyyy-mm-dd
    markedDates[date] = {
      marked: true,
      dotColor: '#2a5ca4',
      activeOpacity: 0,
    };
  });

  // hardcode upcoming vaccines too for now
  markedDates['2025-01-15'] = {
    marked: true,
    dotColor: 'orange',
  };
  markedDates['2025-02-20'] = {
    marked: true,
    dotColor: 'orange',
  };

  return (
   <SafeAreaView style={{ flex: 1 , backgroundColor: '#fff' }}> 
    <View style={styles.container}>
      <Text style={styles.title}>Vaccination Calendar</Text>
      <Calendar
        markedDates={markedDates}
        onDayPress={(day: DateData) => {
          console.log('Selected day', day.dateString);
        }}
        theme={{
          selectedDayBackgroundColor: '#2a5ca4',
          todayTextColor: '#2a5ca4',
        }}
      />
    </View>
   </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2a5ca4',
    marginBottom: 12,
  },
});
