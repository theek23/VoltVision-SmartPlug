import React from 'react';
import { View, Text, Button } from 'react-native';

const App = () => {
  const handlePress = async () => {
    try {
      const response = await fetch('http://192.168.8.100/off');
      const data = await response.json();
      console.log('Response:', data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>VOLTVISION</Text>
      <Button title="On/Off" onPress={handlePress} />
    </View>
  );
};

export default App;