import React from 'react';
import { StyleSheet, View, SafeAreaView, StatusBar, Text } from 'react-native';
import MobileWorkspace from './components/MobileWorkspace';

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      <View style={styles.header}>
        <Text style={styles.title}>HumanText <Text style={styles.highlight}>AI</Text></Text>
        <Text style={styles.subtitle}>Mobile Agentic Engine</Text>
      </View>
      <MobileWorkspace />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#09090b', // Obsidian Glass dark background
  },
  header: {
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255,255,255,0.1)',
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#f8f8f2',
  },
  highlight: {
    color: '#3b82f6', // Accent blue
  },
  subtitle: {
    fontSize: 12,
    color: '#10b981', // Success green indicator
    marginTop: 4,
  }
});
