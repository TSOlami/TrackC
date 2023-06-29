// This file can contain functions to make API requests to your Flask backend

import axios from 'axios';

const httpClient = axios.create({
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
});

export default httpClient;
