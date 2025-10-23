import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, Dimensions, Button } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const slides = [
  { title: 'Добро пожаловать!', text: 'Это интерактивная карта Донецка. Исследуй город!' },
  { title: 'Отзывы и избранное', text: 'Оставляй отзывы и добавляй любимые места в избранное.' },
  { title: 'Для бизнеса', text: 'Владельцы могут добавлять свои заведения прямо на карту!' }
];

const width = Dimensions.get('window').width;

export default function Onboarding({ navigation }) {
  const [index, setIndex] = useState(0);

  const handleNext = async () => {
    if (index === slides.length - 1) {
      await AsyncStorage.setItem('seenOnboarding', 'true');
      navigation.replace('Auth');
    } else {
      setIndex(index + 1);
    }
  };

  return (
    <ScrollView horizontal pagingEnabled style={{ flex: 1 }} scrollEnabled={false}>
      {slides.map((slide, i) => (
        <View key={i} style={[styles.slide, { width }]}> 
          <Text style={styles.title}>{slide.title}</Text>
          <Text style={styles.text}>{slide.text}</Text>
          {i === index && <Button title={i === slides.length - 1 ? 'Начать' : 'Далее'} onPress={handleNext} />}
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  slide: {
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24
  },
  title: {
    fontSize: 26,
    fontWeight: 'bold',
    marginBottom: 16
  },
  text: {
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 24
  }
});