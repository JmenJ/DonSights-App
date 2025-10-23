import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

/**
 * Create a configured axios instance for communicating with the backend API.
 * Adjust the baseURL to match your development environment. When
 * running on an Android emulator, `10.0.2.2` points back to your
 * host machine. On a physical device you will need to use the
 * machine's IP address.
 */
const api = axios.create({
    baseURL: 'https://10.0.2.2:4443',
    timeout: 1000,
});

// Attach the JWT token to every request if present. AsyncStorage is
// asynchronous, so we use an interceptor to await the token.
api.interceptors.request.use(async (config) => {
    const token = await AsyncStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default api;