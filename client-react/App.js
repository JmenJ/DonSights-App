import React, { useEffect, useState } from 'react';
import { ActivityIndicator, View } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

// Import screens
import Onboarding from './screens/Onboarding';
import AuthScreen from './screens/AuthScreen';
import MapScreen from './screens/MapScreen';
import PlaceDetails from './screens/PlaceDetails';

const Stack = createStackNavigator();

/**
 * Root component. Determines whether to show the onboarding flow on
 * first launch, the authentication screen when not logged in, or the
 * main application when a token is present. Uses AsyncStorage to
 * persist authentication and onboarding state.
 */
export default function App() {
    const [isLoading, setIsLoading] = useState(true);
    const [showOnboarding, setShowOnboarding] = useState(false);
    const [userToken, setUserToken] = useState(null);

    useEffect(() => {
        const bootstrap = async () => {
            try {
                const viewed = await AsyncStorage.getItem('viewedOnboarding');
                setShowOnboarding(!viewed);
                const token = await AsyncStorage.getItem('token');
                setUserToken(token);
            } catch (err) {
                console.warn('Error loading persisted state', err);
            } finally {
                setIsLoading(false);
            }
        };
        bootstrap();
    }, []);

    if (isLoading) {
        return (
            <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
                <ActivityIndicator size="large" />
            </View>
        );
    }

    return (
        <NavigationContainer>
            <Stack.Navigator screenOptions={{ headerShown: false }}>
                {showOnboarding ? (
                    // Onboarding flow shown only once
                    <Stack.Screen name="Onboarding" component={Onboarding} />
                ) : userToken ? (
                    // Main app for authenticated users
                    <>
                        <Stack.Screen name="Map" component={MapScreen} />
                        <Stack.Screen name="PlaceDetails" component={PlaceDetails} />
                    </>
                ) : (
                    // Authentication screen for guests
                    <Stack.Screen name="Auth" component={AuthScreen} />
                )}
            </Stack.Navigator>
        </NavigationContainer>
    );
}