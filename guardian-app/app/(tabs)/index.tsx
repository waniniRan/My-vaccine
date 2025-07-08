import React, { useEffect, useState } from 'react';
import { View, Text, Button, ActivityIndicator, FlatList, RefreshControl } from 'react-native';
import guardianService from '../../services/guardianService';
import { useAuth } from '../AuthContext';
import StatsGrid from '../../components/ui/StatsGrid';

const HomeTab = () => {
  const { user, loading: authLoading } = useAuth();
  const [children, setChildren] = useState<any[]>([]);
  const [selectedChild, setSelectedChild] = useState<any>(null);
  const [growthRecords, setGrowthRecords] = useState<any[]>([]);
  const [vaccines, setVaccines] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState('');
  const [totalChildren, setTotalChildren] = useState(0);
  const [totalVaccinations, setTotalVaccinations] = useState(0);
  const [totalGrowthRecords, setTotalGrowthRecords] = useState(0);

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      const childrenData = await guardianService.getChildren();
      setChildren(childrenData);
      if (childrenData.length > 0) {
        setSelectedChild(childrenData[0]);
        await fetchChildDetails(childrenData[0].child_id);
      } else {
        setSelectedChild(null);
        setGrowthRecords([]);
        setVaccines([]);
      }
    } catch (err: any) {
      setError(err.detail || 'Failed to load data');
    }
    setLoading(false);
  };

  const fetchChildDetails = async (childId: string) => {
    try {
      const growth = await guardianService.getChildGrowthRecords(childId);
      setGrowthRecords(growth);
      const vaccinesData = await guardianService.getChildVaccinationRecords(childId);
      setVaccines(vaccinesData);
    } catch (err: any) {
      setError(err.detail || 'Failed to load child details');
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    setTotalChildren(children.length);
    setTotalVaccinations(vaccines.length);
    setTotalGrowthRecords(growthRecords.length);
  }, [children, vaccines, growthRecords]);

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchData();
    setRefreshing(false);
  };

  const handleChildSwitch = async (child: any) => {
    setSelectedChild(child);
    await fetchChildDetails(child.child_id);
  };

  if (authLoading || loading) {
    return <ActivityIndicator style={{ flex: 1 }} />;
  }

  if (error) {
    return <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}><Text>{error}</Text></View>;
  }

  return (
    <View style={{ flex: 1 }}>
      <StatsGrid
        stats={[
          { title: 'Children', count: totalChildren, icon: 'child', color: '#4F8EF7' },
          { title: 'Vaccinations', count: totalVaccinations, icon: 'syringe', color: '#34C759' },
          { title: 'Growth Records', count: totalGrowthRecords, icon: 'chart-line', color: '#FF9500' },
        ]}
      />
      <View style={{ flex: 1, padding: 16 }}>
        {children.length > 1 && (
          <FlatList
            data={children}
            horizontal
            keyExtractor={item => item.child_id}
            renderItem={({ item }) => (
              <Button
                title={item.full_name}
                onPress={() => handleChildSwitch(item)}
                color={selectedChild?.child_id === item.child_id ? 'blue' : 'gray'}
              />
            )}
          />
        )}
        {selectedChild ? (
          <View>
            <Text style={{ fontSize: 20, fontWeight: 'bold', marginVertical: 10 }}>{selectedChild.full_name}</Text>
            <Text>Date of Birth: {selectedChild.date_of_birth}</Text>
            <Text>Gender: {selectedChild.gender}</Text>
            <Text>Age: {selectedChild.age}</Text>
            <Text style={{ marginTop: 10, fontWeight: 'bold' }}>Growth Records:</Text>
            <FlatList
              data={growthRecords}
              keyExtractor={item => item.id.toString()}
              renderItem={({ item }) => (
                <Text>{item.date_recorded}: {item.height}cm, {item.weight}kg</Text>
              )}
              ListEmptyComponent={<Text>No growth records found.</Text>}
            />
            <Text style={{ marginTop: 10, fontWeight: 'bold' }}>Vaccination Records:</Text>
            <FlatList
              data={vaccines}
              keyExtractor={item => item.recordID}
              renderItem={({ item }) => (
                <Text>{item.administration_date}: {item.vaccine_name} (Dose {item.dose_number})</Text>
              )}
              ListEmptyComponent={<Text>No vaccination records found.</Text>}
            />
          </View>
        ) : (
          <Text>No children found.</Text>
        )}
        <Button title="Refresh" onPress={onRefresh} />
      </View>
    </View>
  );
};

export default HomeTab; 