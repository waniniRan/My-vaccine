import React, { useEffect, useState, useCallback } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Calendar, DateData } from 'react-native-calendars';
import { SafeAreaView } from 'react-native-safe-area-context';
import { guardianService } from '../../services/guardianService';
import { useAuth } from '../AuthContext';

export default function CalendarScreen() {
  const { user } = useAuth();
  const [children, setChildren] = useState([]);
  const [selectedChild, setSelectedChild] = useState(null);
  const [markedDates, setMarkedDates] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  const fetchChildren = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await guardianService.getChildren();
      setChildren(data);
      if (data.length > 0) setSelectedChild(data[0]);
    } catch (err) {
      setError('Failed to load children.');
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchVaccinationRecords = useCallback(async (childId) => {
    setLoading(true);
    setError(null);
    try {
      const records = await guardianService.getChildVaccinationRecords(childId);
      const dates = {};
      records.forEach((rec) => {
        if (rec.date_administered) {
          dates[rec.date_administered] = { marked: true, dotColor: '#00C853' };
        }
      });
      setMarkedDates(dates);
    } catch (err) {
      setError('Failed to load vaccination records.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchChildren();
  }, [fetchChildren]);

  useEffect(() => {
    if (selectedChild) {
      fetchVaccinationRecords(selectedChild.id);
    }
  }, [selectedChild, fetchVaccinationRecords]);

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchChildren();
    if (selectedChild) await fetchVaccinationRecords(selectedChild.id);
    setRefreshing(false);
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
