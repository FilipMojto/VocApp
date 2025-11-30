import axios from 'axios';

const API_URL = "http://localhost:8000"; // backend base url

export const USER_PREFIX = "/users"
export const WORD_PREFIX = "/words"
export const USER_WORD_PREFIX = "/userwords"
export const WORD_RELATION_PREFIX = "/wordrelations"

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
  try {
    const response = await api.post("/users/", { username, password });
    return response.data; // return the created user or relevant data
  } catch (err: any) {
    if (err.response) {
      // Server responded with an error status
      throw new Error(err.response.data?.message || "Registration failed");
    } else if (err.request) {
      // No response received
      throw new Error("Unable to connect with server");
    } else {
      // Something else happened
      throw new Error("An unexpected error occurred");
    }
  }
}

export async function loginUser(username: string, password: string) {
  try {
    const response = await api.post(
      "/users/auth/login",
      new URLSearchParams({ username, password })
    );
    const data = response.data as { access_token: string };
    localStorage.setItem("token", data.access_token);
    return data;
  } catch (err: any) {
    // Axios distinguishes network errors (no response) from HTTP errors
    if (err.response) {
      // Server responded with a status code (e.g., 401, 500)
      throw new Error("Invalid username or password");
    } else if (err.request) {
      // Request was made but no response received (network error)
      throw new Error("Unable to connect with server");
    } else {
      // Something else went wrong
      throw new Error("An unexpected error occurred");
    }
  }
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