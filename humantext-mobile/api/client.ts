// Replace with your computer's local IP address when testing on a physical device.
// e.g., 'http://192.168.1.100:8000/api/v1'
const API_URL = 'http://10.0.2.2:8000/api/v1'; // Default Android Emulator localhost alias

export const humanizeText = async (text: string, strength: string) => {
  try {
    const response = await fetch(`${API_URL}/humanize/advanced`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, strength })
    });
    const data = await response.json();
    return data.job_id;
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};

export const pollJobStatus = async (jobId: string) => {
  try {
    const response = await fetch(`${API_URL}/jobs/${jobId}`);
    return await response.json();
  } catch (error) {
    console.error("Poll Error:", error);
    throw error;
  }
};
