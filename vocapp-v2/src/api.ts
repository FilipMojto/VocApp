import axios from 'axios';

const API_URL = "http://localhost:8000"; // backend base url

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
});

// Add token automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    if (!config.headers) {
      config.headers = {};
    }
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export async function registerUser(username: string, password: string) {
  return api.post("/users/", { username, password });
}

export async function loginUser(username: string, password: string) {
  const response = await api.post("/users/auth/login", new URLSearchParams({
    username,
    password,
  }));
  const data = response.data as { access_token: string };
  localStorage.setItem("token", data.access_token);
  return data;
}

export default api;
import 'promise.prototype.finally/auto'; // Uncomment if you need to polyfill Promise.finally

axios.get('/api/data')
  .then(response => {
    console.log('Success:', response.data);
  })
  .catch(error => {
    console.error('Error:', error);
  })
  .finally(() => {
    console.log('Cleanup or final actions');
  });