// App.js
import React, { useEffect, useState } from 'react';
import { ActivityIndicator, View } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

import Onboarding from './screens/Onboarding';
import AuthScreen from './screens/AuthScreen';
import MapScreen from './screens/MapScreen';
import PlaceDetails from './screens/PlaceDetails';

const Stack = createStackNavigator();

export default function App() {
  const [initialScreen, setInitialScreen] = useState(null);

  useEffect(() => {
    const checkFirstLaunch = async () => {
      const seenOnboarding = await AsyncStorage.getItem('seenOnboarding');
      const token = await AsyncStorage.getItem('token');
      if (!seenOnboarding) setInitialScreen('Onboarding');
      else if (token) setInitialScreen('Map');
      else setInitialScreen('Auth');
    };
    checkFirstLaunch();
  }, []);

  if (!initialScreen) {
    return <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}><ActivityIndicator size="large" /></View>;
  }

  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName={initialScreen} screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Onboarding" component={Onboarding} />
        <Stack.Screen name="Auth" component={AuthScreen} />
        <Stack.Screen name="Map" component={MapScreen} />
        <Stack.Screen name="PlaceDetails" component={PlaceDetails} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// screens/AuthScreen.js
import React, { useState } from 'react';
import { View, Text, TextInput, StyleSheet, TouchableOpacity, Alert, Button, ScrollView } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import api from '../api/client';

export default function AuthScreen({ navigation }) {
  const [mode, setMode] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [isBusiness, setIsBusiness] = useState(false);

  const handleSubmit = async () => {
    try {
      if (mode === 'register') {
        const res = await api.post('/auth/register', {
          email,
          password,
          name,
          role: isBusiness ? 'BusinessOwner' : 'User'
        });
        Alert.alert('Успешно', 'Теперь войдите в аккаунт');
        setMode('login');
      } else {
        const res = await api.post('/auth/login', { email, password });
        await AsyncStorage.setItem('token', res.data.token);
        await AsyncStorage.setItem('userRole', res.data.user.role);
        navigation.replace('Map');
      }
    } catch (err) {
      Alert.alert('Ошибка', err.response?.data?.error || 'Что-то пошло не так');
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>{mode === 'login' ? 'Вход' : 'Регистрация'}</Text>
      {mode === 'register' && (
        <TextInput placeholder="Имя" value={name} onChangeText={setName} style={styles.input} />
      )}
      <TextInput placeholder="Email" value={email} onChangeText={setEmail} style={styles.input} />
      <TextInput placeholder="Пароль" value={password} onChangeText={setPassword} secureTextEntry style={styles.input} />
      {mode === 'register' && (
        <TouchableOpacity onPress={() => setIsBusiness(!isBusiness)}>
          <Text style={styles.switch}>{isBusiness ? 'Владелец бизнеса' : 'Обычный пользователь'}</Text>
        </TouchableOpacity>
      )}
      <Button title={mode === 'login' ? 'Войти' : 'Зарегистрироваться'} onPress={handleSubmit} />
      <TouchableOpacity onPress={() => setMode(mode === 'login' ? 'register' : 'login')}>
        <Text style={styles.switch}>{mode === 'login' ? 'Нет аккаунта? Регистрация' : 'Уже есть аккаунт? Войти'}</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: 24,
  },
  title: {
    fontSize: 28,
    marginBottom: 20,
    textAlign: 'center'
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    marginBottom: 12,
    padding: 10,
    borderRadius: 8
  },
  switch: {
    textAlign: 'center',
    marginVertical: 12,
    color: '#007bff'
  }
});
