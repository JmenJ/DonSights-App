import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Modal, TextInput, Button, Alert } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import AsyncStorage from '@react-native-async-storage/async-storage';
import api from '../api/client';

export default function MapScreen({ navigation }) {
  const [places, setPlaces] = useState([]);
  const [userRole, setUserRole] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);
  const [newPlace, setNewPlace] = useState({ name: '', description: '', lat: 0, lng: 0 });

  useEffect(() => {
    loadPlaces();
    AsyncStorage.getItem('userRole').then(setUserRole);
  }, []);

  const loadPlaces = async () => {
    try {
      const res = await api.get('/places');
      setPlaces(res.data);
    } catch (err) {
      Alert.alert('Ошибка загрузки мест');
    }
  };

  const handleAddPlace = async () => {
    try {
      await api.post('/places', {
        name: newPlace.name,
        description: newPlace.description,
        latitude: newPlace.lat,
        longitude: newPlace.lng
      });
      setModalVisible(false);
      setNewPlace({ name: '', description: '', lat: 0, lng: 0 });
      loadPlaces();
    } catch (err) {
      Alert.alert('Ошибка добавления');
    }
  };

  const handleLongPress = (event) => {
    if (userRole !== 'BusinessOwner' && userRole !== 'Moderator' && userRole !== 'Admin') return;
    const { latitude, longitude } = event.nativeEvent.coordinate;
    setNewPlace({ ...newPlace, lat: latitude, lng: longitude });
    setModalVisible(true);
  };

  const logout = async () => {
    await AsyncStorage.multiRemove(['token', 'userRole']);
    navigation.replace('Auth');
  };

  return (
    <View style={{ flex: 1 }}>
      <MapView style={{ flex: 1 }} onLongPress={handleLongPress}>
        {places.map(place => (
          <Marker
            key={place.id}
            coordinate={{ latitude: place.latitude, longitude: place.longitude }}
            title={place.name}
            description={place.description}
            onCalloutPress={() => navigation.navigate('PlaceDetails', { placeId: place.id })}
          />
        ))}
      </MapView>
      <TouchableOpacity style={styles.logoutBtn} onPress={logout}>
        <Text style={{ color: 'white' }}>Выход</Text>
      </TouchableOpacity>
      <Modal visible={modalVisible} animationType="slide">
        <View style={styles.modalContent}>
          <TextInput placeholder="Название" value={newPlace.name} onChangeText={text => setNewPlace(p => ({ ...p, name: text }))} style={styles.input} />
          <TextInput placeholder="Описание" value={newPlace.description} onChangeText={text => setNewPlace(p => ({ ...p, description: text }))} style={styles.input} />
          <Button title="Добавить" onPress={handleAddPlace} />
          <Button title="Отмена" color="gray" onPress={() => setModalVisible(false)} />
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  logoutBtn: {
    position: 'absolute',
    top: 40,
    right: 20,
    backgroundColor: '#000',
    padding: 10,
    borderRadius: 10
  },
  modalContent: {
    marginTop: 100,
    padding: 20
  },
  input: {
    borderWidth: 1,
    borderColor: '#aaa',
    padding: 10,
    marginBottom: 12,
    borderRadius: 8
  }
});
