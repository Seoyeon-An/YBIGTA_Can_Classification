import React from 'react';
import { StyleSheet, View, Image, Text, Pressable } from 'react-native';

export default function App() {
  return (
    <View style={styles.container}>
      <Image source={require('./assets/logo.png')} style={styles.logo} />
      <Text style={styles.text}>iCANsee</Text>
      <View style={styles.buttonContainer}>
        <Pressable style={[styles.button, styles.buttonVisualImpairment]}>
          <Text style={styles.buttonText}>시각장애인</Text>
        </Pressable>
        <Pressable style={[styles.button, styles.buttonNonVisualImpairment]}>
          <Text style={styles.buttonText}>비시각장애인</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'black',
    alignItems: 'center',
    justifyContent: 'center',
  },
  logo: {
    width: 100,
    height: 100,
    resizeMode: 'contain',
  },
  text: {
    marginTop: 20,
    color: 'white',
    fontSize: 24,
  },
  buttonContainer: {
    marginTop: 30,
    flexDirection: 'row',
  },
  button: {
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 10,
    marginRight: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
  buttonText: {
    color: 'black',
    fontSize: 16,
  },
  buttonVisualImpairment: {
    backgroundColor: 'yellow',
  },
  buttonNonVisualImpairment: {
    backgroundColor: 'white',
  },
});
