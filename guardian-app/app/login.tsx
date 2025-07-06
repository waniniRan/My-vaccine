import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import { useAuth } from './AuthContext';
import { mockGuardian } from '@/services/mockData';
import { Ionicons } from '@expo/vector-icons';

export default function LoginScreen() {
  const [national_id, setNationalId] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const router = useRouter();
  const { setLoggedIn } = useAuth();

  const handleLogin = () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      if (
        national_id.trim() === mockGuardian.national_id &&
        password === 'password123' // change for production
      ) {
        setLoggedIn(true);
      } else {
        Alert.alert('Login Failed', 'Invalid ID or password.');
      }
    }, 800);
  };

  return (
    <View style={styles.container}>
      <View style={styles.card}>
        <View style={styles.inputWrapper}>
          <Ionicons name="person-circle-outline" size={24} color="#555" style={styles.inputIcon} />
          <TextInput
            style={styles.input}
            placeholder="Enter your National ID"
            keyboardType="number-pad"
            value={national_id}
            onChangeText={setNationalId}
          />
        </View>
        <View style={styles.inputWrapper}>
          <Ionicons name="lock-closed-outline" size={24} color="#555" style={styles.inputIcon} />
          <TextInput
            style={styles.input}
            placeholder="Enter your password"
            secureTextEntry={!showPassword}
            value={password}
            onChangeText={setPassword}
          />
          <TouchableOpacity onPress={() => setShowPassword(!showPassword)} style={styles.eyeIcon}>
            <Ionicons
              name={showPassword ? 'eye-off-outline' : 'eye-outline'}
              size={22}
              color="#555"
            />
          </TouchableOpacity>
        </View>
        <TouchableOpacity style={styles.forgotButton} onPress={() => Alert.alert('Redirect to forgot password flow')}>
          <Text style={styles.forgotText}>Forgot password?</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.button, loading && { opacity: 0.7 }]}
          onPress={handleLogin}
          disabled={loading}
        >
          <Text style={styles.buttonText}>{loading ? 'Signing in...' : 'Sign In'}</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#e6f0fb', // lighter blue background
  },
  card: {
    width: '90%',
    maxWidth: 400,
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#c2d4ee',
    borderRadius: 8,
    paddingHorizontal: 10,
    backgroundColor: '#f9fbff',
    marginTop: 16,
  },
  inputIcon: {
    marginRight: 8,
  },
  eyeIcon: {
    marginLeft: 8,
  },
  input: {
    flex: 1,
    fontSize: 16,
    paddingVertical: 12,
  },
  forgotButton: {
    alignSelf: 'flex-end',
    marginTop: 10,
  },
  forgotText: {
    color: '#2a5ca4', // darker blue but not navy
    fontSize: 14,
  },
  button: {
    backgroundColor: '#2a5ca4', // dark but vibrant blue
    borderRadius: 8,
    paddingVertical: 14,
    marginTop: 24,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
});
