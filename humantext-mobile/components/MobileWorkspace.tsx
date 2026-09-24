import React, { useState } from 'react';
import { StyleSheet, View, Text, TextInput, TouchableOpacity, ScrollView, ActivityIndicator } from 'react-native';
import { humanizeText, pollJobStatus } from '../api/client';

export default function MobileWorkspace() {
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [strength, setStrength] = useState('medium');
  const [loading, setLoading] = useState(false);

  const handleHumanize = async () => {
    if (!inputText.trim()) return;
    
    setLoading(true);
    setOutputText('');
    
    try {
      const jobId = await humanizeText(inputText, strength);
      if (jobId) {
        // Poll for result
        const checkStatus = setInterval(async () => {
          const result = await pollJobStatus(jobId);
          if (result.status === 'completed') {
            clearInterval(checkStatus);
            setLoading(false);
            const text = result.result.candidates ? result.result.candidates[0] : result.result.final_output;
            setOutputText(text);
          } else if (result.status === 'failed') {
            clearInterval(checkStatus);
            setLoading(false);
            setOutputText('Error: Backend processing failed.');
          }
        }, 2000);
      }
    } catch (error) {
      setLoading(false);
      setOutputText('Error connecting to backend API.');
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={{ padding: 20 }}>
      
      <Text style={styles.label}>Paste AI Text:</Text>
      <TextInput
        style={styles.input}
        multiline
        placeholder="Text to humanize..."
        placeholderTextColor="#a1a1aa"
        value={inputText}
        onChangeText={setInputText}
      />

      <View style={styles.buttonRow}>
        <TouchableOpacity 
          style={[styles.strengthBtn, strength === 'light' && styles.activeBtn]}
          onPress={() => setStrength('light')}
        >
          <Text style={styles.btnText}>Ninja</Text>
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={[styles.strengthBtn, strength === 'medium' && styles.activeBtn]}
          onPress={() => setStrength('medium')}
        >
          <Text style={styles.btnText}>Balanced</Text>
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={[styles.strengthBtn, strength === 'aggressive' && styles.activeBtn]}
          onPress={() => setStrength('aggressive')}
        >
          <Text style={styles.btnText}>Ghost</Text>
        </TouchableOpacity>
      </View>

      <TouchableOpacity 
        style={styles.submitBtn} 
        onPress={handleHumanize}
        disabled={loading}
      >
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.submitBtnText}>Humanize Now</Text>}
      </TouchableOpacity>

      {outputText ? (
        <View style={styles.outputContainer}>
          <Text style={styles.label}>Result:</Text>
          <Text style={styles.outputText}>{outputText}</Text>
        </View>
      ) : null}
      
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  label: {
    color: '#a1a1aa',
    marginBottom: 8,
    fontWeight: '600',
  },
  input: {
    backgroundColor: 'rgba(24, 24, 27, 0.65)',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.1)',
    borderRadius: 8,
    color: '#f8f8f2',
    padding: 16,
    minHeight: 150,
    textAlignVertical: 'top',
    marginBottom: 20,
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  strengthBtn: {
    flex: 1,
    padding: 12,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.1)',
    borderRadius: 8,
    marginHorizontal: 4,
    alignItems: 'center',
  },
  activeBtn: {
    backgroundColor: 'rgba(59, 130, 246, 0.2)',
    borderColor: '#3b82f6',
  },
  btnText: {
    color: '#f8f8f2',
    fontWeight: 'bold',
  },
  submitBtn: {
    backgroundColor: '#3b82f6',
    padding: 16,
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 20,
  },
  submitBtnText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
  outputContainer: {
    backgroundColor: 'rgba(24, 24, 27, 0.65)',
    padding: 16,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#8b5cf6',
  },
  outputText: {
    color: '#f8f8f2',
    lineHeight: 24,
  }
});
