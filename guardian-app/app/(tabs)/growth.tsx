import React, { useEffect, useState } from 'react';
import { View, Text, ActivityIndicator, Button, FlatList, RefreshControl } from 'react-native';
import guardianService from '../../services/guardianService';
import { useAuth } from '../AuthContext';

const GrowthTab = () => {
  const { user } = useAuth();
  const [children, setChildren] = useState<any[]>([]);
  const [selectedChild, setSelectedChild] = useState<any>(null);
  const [growthRecords, setGrowthRecords] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState('');

  const fetchChildrenAndGrowth = async () => {
    setLoading(true);
    setError('');
    try {
      const childrenData = await guardianService.getChildren();
      setChildren(childrenData);
      if (childrenData.length > 0) {
        setSelectedChild(childrenData[0]);
        await fetchGrowth(childrenData[0].child_id);
      } else {
        setSelectedChild(null);
        setGrowthRecords([]);
      }
    } catch (err: any) {
      setError(err.detail || 'Failed to load data');
    }
    setLoading(false);
  };

  const fetchGrowth = async (childId: string) => {
    try {
      const growth = await guardianService.getChildGrowthRecords(childId);
      setGrowthRecords(growth);
    } catch (err: any) {
      setError(err.detail || 'Failed to load growth records');
    }
  };

  useEffect(() => {
    fetchChildrenAndGrowth();
  }, []);

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchChildrenAndGrowth();
    setRefreshing(false);
  };

  const handleChildSwitch = async (child: any) => {
    setSelectedChild(child);
    await fetchGrowth(child.child_id);
  };

  if (loading) {
    return <ActivityIndicator style={{ flex: 1 }} />;
  }

  if (error) {
    return <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}><Text>{error}</Text></View>;
  }

  return (
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
              <Text>{item.date_recorded}: {item.height}cm, {item.weight}kg (BMI: {item.bmi ?? 'N/A'})</Text>
            )}
            ListEmptyComponent={<Text>No growth records found.</Text>}
          />
        </View>
      ) : (
        <Text>No children found.</Text>
      )}
      <Button title="Refresh" onPress={onRefresh} />
    </View>
  );
};

export default GrowthTab; 