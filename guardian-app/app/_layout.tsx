import { ThemeProvider, DarkTheme, DefaultTheme } from '@react-navigation/native';
import { useFonts } from 'expo-font';
import { Slot, useRouter, useSegments, useRootNavigationState } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import React, { useEffect, useState } from 'react';
import { useColorScheme } from '@/hooks/useColorScheme';
import { AuthContext } from './AuthContext';

export default function RootLayout() {
  const colorScheme = useColorScheme();
  const [loaded] = useFonts({
    SpaceMono: require('../assets/fonts/SpaceMono-Regular.ttf'),
  });

  const [loggedIn, setLoggedIn] = useState(false); // You can wire up proper auth later
  const router = useRouter();
  const segments = useSegments();
  const navigationState = useRootNavigationState();

  useEffect(() => {
    if (!navigationState?.key) return;
    const timeout = setTimeout(() => {
      if (!loggedIn && segments[0] !== 'login') {
        router.replace('/login');
      }
      if (loggedIn && segments[0] === 'login') {
        router.replace('/(tabs)');
      }
    }, 0);
    return () => clearTimeout(timeout);
  }, [loggedIn, segments, navigationState]);

  if (!loaded) {
    return null; // show a splash maybe
  }

  return (
    <AuthContext.Provider value={{ loggedIn, setLoggedIn }}>
      <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
        <Slot />
        <StatusBar style="dark" backgroundColor="#fff" translucent={false} />
      </ThemeProvider>
    </AuthContext.Provider>
  );
}
