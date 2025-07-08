import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { FontAwesome5 } from '@expo/vector-icons';

interface StatsCardProps {
  title: string;
  count: number;
  icon: string;
  color: string;
}

const StatsCard: React.FC<StatsCardProps> = ({ title, count, icon, color }) => {
  return (
    <View style={[styles.card, { borderColor: color }]}> 
      <FontAwesome5 name={icon} size={28} color={color} style={styles.icon} />
      <Text style={styles.count}>{count}</Text>
      <Text style={styles.title}>{title}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    margin: 8,
    borderWidth: 2,
    elevation: 2,
    minWidth: 100,
    minHeight: 120,
  },
  icon: {
    marginBottom: 8,
  },
  count: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#222',
  },
  title: {
    fontSize: 16,
    color: '#666',
    marginTop: 4,
  },
});

export default StatsCard; 