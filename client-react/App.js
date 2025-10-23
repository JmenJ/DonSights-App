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