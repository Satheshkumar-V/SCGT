import axios from 'axios';

export const callInteractionScannerAgent = async (logData) => {
  const response = await axios.post('http://localhost:8000/parse', { logData });
  return response.data;
};
