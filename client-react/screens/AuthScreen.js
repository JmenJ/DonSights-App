import React, { useState } from 'react';
import { View, Text, TextInput, StyleSheet, TouchableOpacity, Alert, Button, ScrollView } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import api from '../api/client';

/**
 * Authentication screen that provides both login and registration
 * capabilities. The user can switch between modes by tapping a link.
 * Upon successful login or registration the JWT token and user
 * information are stored in AsyncStorage and the navigation resets to
 * the main map screen.
 */
export default function AuthScreen({ navigation }) {
    const [isRegister, setIsRegister] = useState(false);
    // Common fields
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    // Business owner specific fields
    const [isBusinessOwner, setIsBusinessOwner] = useState(false);
    const [companyName, setCompanyName] = useState('');
    const [inn, setInn] = useState('');
    const [phone, setPhone] = useState('');

    const resetFields = () => {
        setName('');
        setEmail('');
        setPassword('');
        setCompanyName('');
        setInn('');
        setPhone('');
        setIsBusinessOwner(false);
    };

    const handleSubmit = async () => {
        if (!email || !password || (isRegister && !name)) {
            Alert.alert('Ошибка', 'Пожалуйста, заполните обязательные поля');
            return;
        }
        try {
            if (isRegister) {
                // Build payload for registration
                const payload = {
                    name,
                    email,
                    password,
                };
                if (isBusinessOwner) {
                    payload.type = 'businessOwner';
                    payload.company_name = companyName || undefined;
                    payload.inn = inn || undefined;
                    payload.phone = phone || undefined;
                }
                const response = await api.post('/auth/register', payload);
                const { token, user } = response.data;
                await AsyncStorage.setItem('token', token);
                await AsyncStorage.setItem('user', JSON.stringify(user));
                await AsyncStorage.setItem('userRole', user.role);
                resetFields();
                navigation.reset({ index: 0, routes: [{ name: 'Map' }] });
            } else {
                const response = await api.post('/auth/login', { email, password });
                const { token, user } = response.data;
                await AsyncStorage.setItem('token', token);
                await AsyncStorage.setItem('user', JSON.stringify(user));
                await AsyncStorage.setItem('userRole', user.role);
                resetFields();
                navigation.reset({ index: 0, routes: [{ name: 'Map' }] });
            }
        } catch (error) {
            console.warn('Auth error', error);
            const message = error.response?.data?.error || 'Произошла ошибка';
            Alert.alert('Ошибка', message);
        }
    };

    return (value = { name }
     onChangeText = { setName }
        />
     )
}
     <TextInput
     style={styles.input}
     placeholder="Email"
     value={email}
     onChangeText={setEmail}
     keyboardType="email-address"
     autoCapitalize="none"
     />
     <TextInput
     style={styles.input}
     placeholder="Пароль"
     value={password}
     onChangeText={setPassword}
     secureTextEntry
     />
{
    isRegister && (
        <>
            <TouchableOpacity
                onPress={() => setIsBusinessOwner(!isBusinessOwner)}
                style={styles.checkboxContainer}
            >
                <View style={[styles.checkbox, isBusinessOwner && styles.checkboxChecked]} />
                <Text style={styles.checkboxLabel}>Зарегистрироваться как владелец бизнеса</Text>
            </TouchableOpacity>
            {isBusinessOwner && (
                <>
                    <TextInput
                        style={styles.input}
                        placeholder="Название компании"
                        value={companyName}
                        onChangeText={setCompanyName}
                    />
                    <TextInput
                        style={styles.input}
                        placeholder="ИНН"
                        value={inn}
                        onChangeText={setInn}
                    />
                    <TextInput
                        style={styles.input}
                        placeholder="Телефон"
                        value={phone}
                        onChangeText={setPhone}
                        keyboardType="phone-pad"
                    />
                </>
            )}
        </>
    )
}
     <Button
     title={isRegister ? 'Зарегистрироваться' : 'Войти'}
     onPress={handleSubmit}
     />
     <TouchableOpacity onPress={() => { setIsRegister(!isRegister); resetFields(); }}>
     <Text style={styles.switchText}>
     {isRegister ? 'Уже есть аккаунт? Войти' : 'Нет аккаунта? Регистрация'}
     </Text>
     </TouchableOpacity>
     </View >
     </ScrollView >
     );
    }