import React, { useState } from 'react';
import { View, Text, TextInput, Button, ActivityIndicator, StyleSheet } from 'react-native';
import { useAuth } from './AuthContext';
import guardianService from '../services/guardianService';
import AsyncStorage from '@react-native-async-storage/async-storage';

type GuardianLoginResponse = {
  access: string;
  refresh: string;
  password_change_required?: boolean;
};

const LoginScreen = ({ navigation }: any) => {
  const { login } = useAuth();
  const [nationalId, setNationalId] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [showChangePassword, setShowChangePassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await guardianService.login({ national_id: nationalId, password }) as GuardianLoginResponse;
      const { access, refresh, password_change_required } = response;
      await AsyncStorage.setItem('accessToken', access);
      await AsyncStorage.setItem('refreshToken', refresh);
      if (password_change_required) {
        setShowChangePassword(true);
      } else {
        login({ access, refresh });
      }
    } catch (err: any) {
      setError('Login failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Guardian Login</Text>
      <TextInput
        style={styles.input}
        placeholder="National ID"
        value={nationalId}
        onChangeText={setNationalId}
        autoCapitalize="none"
      />
      <TextInput
        style={styles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      {error ? <Text style={styles.error}>{error}</Text> : null}
      {loading ? (
        <ActivityIndicator />
      ) : (
        <Button title="Login" onPress={handleLogin} />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, textAlign: 'center' },
  input: { borderWidth: 1, borderColor: '#ccc', borderRadius: 5, padding: 10, marginBottom: 10 },
  error: { color: 'red', marginBottom: 10, textAlign: 'center' },
});

export default LoginScreen; 