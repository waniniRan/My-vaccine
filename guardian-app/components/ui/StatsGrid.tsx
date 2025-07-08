import React from 'react';
import { View, StyleSheet, Dimensions } from 'react-native';
import StatsCard from '../StatsCard';

interface Stat {
  title: string;
  count: number;
  icon: string;
  color: string;
}

interface StatsGridProps {
  stats: Stat[];
}

const StatsGrid: React.FC<StatsGridProps> = ({ stats }) => {
  return (
    <View style={styles.grid}>
      {stats.map((stat, idx) => (
        <StatsCard
          key={stat.title}
          title={stat.title}
          count={stat.count}
          icon={stat.icon}
          color={stat.color}
        />
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  grid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'stretch',
    marginHorizontal: 8,
    marginTop: 16,
  },
});

export default StatsGrid; 