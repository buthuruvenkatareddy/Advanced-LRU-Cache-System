import axios from 'axios';

// Use environment variable for backend URL or fallback to relative path
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const cacheApi = {
  async getItem(key) {
    const response = await apiClient.get(`/cache/${key}`);
    return response.data;
  },

  async putItem(data) {
    const response = await apiClient.post('/cache', data);
    return response.data;
  },

  async deleteItem(key) {
    const response = await apiClient.delete(`/cache/${key}`);
    return response.data;
  },

  async getAllItems() {
    const response = await apiClient.get('/all');
    return response.data;
  },

  async getStats() {
    const response = await apiClient.get('/stats');
    return response.data;
  },

  async clearCache() {
    const response = await apiClient.post('/clear');
    return response.data;
  },

  async cleanupExpired() {
    const response = await apiClient.post('/cleanup-expired');
    return response.data;
  },

  async updateCapacity(capacity) {
    const response = await apiClient.put('/capacity', { capacity });
    return response.data;
  },

  async getCacheInfo() {
    const response = await apiClient.get('/cache-info');
    return response.data;
  },

  async healthCheck() {
    const response = await apiClient.get('/health');
    return response.data;
  },
};

export default apiClient;
