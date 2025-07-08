import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { AuthProvider, useAuth } from '../../../myVaccine/guardian-app/app/AuthContext';
import LoginScreen from '../../../myVaccine/guardian-app/app/login';
import HomeTab from '../../../myVaccine/guardian-app/app/(tabs)/index';
import GrowthTab from '../../../myVaccine/guardian-app/app/(tabs)/growth';
import SettingsTab from '../../../myVaccine/guardian-app/app/(tabs)/settings';
import { ActivityIndicator, View } from 'react-native';

const Tab = createBottomTabNavigator();

function MainTabs() {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Home" component={HomeTab} />
      <Tab.Screen name="Growth" component={GrowthTab} />
      <Tab.Screen name="Settings" component={SettingsTab} />
    </Tab.Navigator>
  );
}

function RootNavigator() {
  const { isAuthenticated, loading } = useAuth();
  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" />
      </View>
    );
  }
  return isAuthenticated ? <MainTabs /> : <LoginScreen />;
}

export default function App() {
  return (
    <AuthProvider>
      <NavigationContainer>
        <RootNavigator />
      </NavigationContainer>
    </AuthProvider>
  );
} 