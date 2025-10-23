import React, { useState, useRef } from 'react';
import { View, Text, ScrollView, Dimensions, StyleSheet, Button } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function Onboarding({ navigation }) {
    const slides = [
        {
            title: 'Добро пожаловать!',
            description: 'Исследуйте карту достопримечательностей Донецка и находите интересные места.',
        },
        {
            title: 'Отзывы и избранное',
            description: 'Оставляйте отзывы о местах и добавляйте их в избранное, чтобы не забыть.',
        },
        {
            title: 'Для владельцев бизнеса',
            description: 'Добавляйте свои заведения на карту и управляйте информацией о них.',
        },
    ];
    const scrollRef = useRef(null);
    const [index, setIndex] = useState(0);

    const handleNext = async () => {
        if (index < slides.length - 1) {
            const nextIndex = index + 1;
            setIndex(nextIndex);
            scrollRef.current?.scrollTo({ x: nextIndex * width, animated: true });
        } else {
            // Mark onboarding as viewed and navigate to auth
            await AsyncStorage.setItem('viewedOnboarding', 'true');
            navigation.reset({ index: 0, routes: [{ name: 'Auth' }] });
        }
    };

    return (
        <View style={styles.container}>
            <ScrollView
                horizontal
                pagingEnabled
                showsHorizontalScrollIndicator={false}
                ref={scrollRef}
                scrollEnabled={false}
                style={styles.scrollView}
            >
                {slides.map((slide, i) => (
                    <View key={i} style={[styles.slide, { width }]}>
                        <Text style={styles.title}>{slide.title}</Text>
                        <Text style={styles.text}>{slide.description}</Text>
                    </View>
                ))}
            </ScrollView>
            <View style={styles.buttonContainer}>
                <Button
                    title={index === slides.length - 1 ? 'Начать' : 'Далее'}
                    onPress={handleNext}
                />
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center',
    },
    scrollView: {
        flexGrow: 0,
    },
    slide: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        paddingHorizontal: 20,
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 10,
        textAlign: 'center',
    },
    text: {
        fontSize: 16,
        textAlign: 'center',
    },
    buttonContainer: {
        position: 'absolute',
        bottom: 40,
        left: 0,
        right: 0,
        paddingHorizontal: 40,
    },
});