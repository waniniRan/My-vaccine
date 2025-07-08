import React, { useEffect, useState } from 'react';
import { View, Text, TextInput, Button, ActivityIndicator, StyleSheet, Alert } from 'react-native';
import { useAuth } from '../AuthContext';
import guardianService from '../../services/guardianService';

const SettingsTab = () => {
  const { user, logout, refreshProfile } = useAuth();
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [changing, setChanging] = useState(false);
  const [success, setSuccess] = useState('');

  useEffect(() => {
    const fetchProfile = async () => {
      setLoading(true);
      setError('');
      try {
        const data = await guardianService.getProfile();
        setProfile(data);
      } catch (err: any) {
        setError(err.detail || 'Failed to load profile');
      }
      setLoading(false);
    };
    fetchProfile();
  }, [refreshProfile]);

  const handleChangePassword = async () => {
    setSuccess('');
    setError('');
    if (!oldPassword || !newPassword || !confirmPassword) {
      setError('Please fill all password fields.');
      return;
    }
    if (newPassword !== confirmPassword) {
      setError('New passwords do not match.');
      return;
    }
    setChanging(true);
    try {
      await guardianService.changePassword({ old_password: oldPassword, new_password: newPassword });
      setSuccess('Password changed successfully.');
      setOldPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (err: any) {
      setError(err.detail || 'Password change failed');
    }
    setChanging(false);
  };

  if (loading) {
    return <ActivityIndicator style={{ flex: 1 }} />;
  }

  if (error) {
    return <View style={styles.center}><Text style={styles.error}>{error}</Text></View>;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Profile</Text>
      {profile && (
        <View style={styles.profileBox}>
          <Text>Full Name: {profile.full_name}</Text>
          <Text>Email: {profile.email}</Text>
          <Text>Phone: {profile.phone_number}</Text>
          <Text>National ID: {profile.national_id}</Text>
        </View>
      )}
      <Text style={styles.title}>Change Password</Text>
      <TextInput
        style={styles.input}
        placeholder="Current Password"
        value={oldPassword}
        onChangeText={setOldPassword}
        secureTextEntry
      />
      <TextInput
        style={styles.input}
        placeholder="New Password"
        value={newPassword}
        onChangeText={setNewPassword}
        secureTextEntry
      />
      <TextInput
        style={styles.input}
        placeholder="Confirm New Password"
        value={confirmPassword}
        onChangeText={setConfirmPassword}
        secureTextEntry
      />
      {changing ? <ActivityIndicator /> : <Button title="Change Password" onPress={handleChangePassword} />}
      {success ? <Text style={styles.success}>{success}</Text> : null}
      <Button title="Logout" color="red" onPress={logout} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 20, fontWeight: 'bold', marginVertical: 10 },
  input: { borderWidth: 1, borderColor: '#ccc', borderRadius: 5, padding: 10, marginBottom: 10 },
  error: { color: 'red', marginBottom: 10, textAlign: 'center' },
  success: { color: 'green', marginBottom: 10, textAlign: 'center' },
  profileBox: { marginBottom: 20, padding: 10, backgroundColor: '#f5f5f5', borderRadius: 5 },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
});

export default SettingsTab; 