// App.js + AuthScreen.js + MapScreen.js (оставляем как есть)

// screens/PlaceDetails.js
import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TextInput, Button, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import api from '../api/client';

export default function PlaceDetails({ route }) {
  const { placeId } = route.params;
  const [place, setPlace] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [comment, setComment] = useState('');
  const [userRole, setUserRole] = useState(null);

  useEffect(() => {
    load();
    AsyncStorage.getItem('userRole').then(setUserRole);
  }, []);

  const load = async () => {
    try {
      const res1 = await api.get(`/places/${placeId}`);
      setPlace(res1.data);
      const res2 = await api.get(`/reviews/${placeId}`);
      setReviews(res2.data);
    } catch (err) {
      Alert.alert('Ошибка загрузки');
    }
  };

  const submitReview = async () => {
    try {
      await api.post('/reviews', { place_id: placeId, text: comment });
      setComment('');
      load();
    } catch (err) {
      Alert.alert('Ошибка отзыва');
    }
  };

  const toggleFavorite = async () => {
    try {
      await api.post('/favorites', { place_id: placeId });
      Alert.alert('Добавлено в избранное');
    } catch {
      Alert.alert('Ошибка');
    }
  };

  if (!place) return <Text>Загрузка...</Text>;

  return (
    <ScrollView style={{ padding: 20 }}>
      <Text style={styles.title}>{place.name}</Text>
      <Text style={styles.desc}>{place.description}</Text>
      <Text style={styles.hours}>⏰ {place.opening_hours || 'Время работы не указано'}</Text>

      {userRole && (
        <>
          <Button title="Добавить в избранное" onPress={toggleFavorite} />
          <Text style={{ marginTop: 16, fontWeight: 'bold' }}>Оставить отзыв:</Text>
          <TextInput value={comment} onChangeText={setComment} placeholder="Ваш отзыв..." style={styles.input} />
          <Button title="Отправить" onPress={submitReview} />
        </>
      )}

      <Text style={{ marginTop: 20, fontWeight: 'bold' }}>Отзывы:</Text>
      {reviews.map((r, idx) => (
        <View key={idx} style={styles.review}>
          <Text>{r.text}</Text>
          <Text style={styles.byline}>— {r.user_id}</Text>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 8 },
  desc: { fontSize: 16, marginBottom: 8 },
  hours: { fontSize: 14, color: 'gray', marginBottom: 16 },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 8,
    marginVertical: 8,
    borderRadius: 6
  },
  review: {
    marginVertical: 6,
    padding: 8,
    backgroundColor: '#f2f2f2',
    borderRadius: 6
  },
  byline: {
    fontSize: 12,
    color: '#666',
    marginTop: 4
  }
});