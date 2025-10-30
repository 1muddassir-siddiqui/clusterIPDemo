const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();
const BACKEND_URL = 'http://backend-service:5000';

app.use(express.static('public'));

app.get('/api/employees', async (req, res) => {
    try {
        const response = await axios.get(`${BACKEND_URL}/employees`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Backend connection failed' });
    }
});

app.get('/api/message', async (req, res) => {
    try {
        const response = await axios.get(`${BACKEND_URL}/message`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Backend connection failed' });
    }
});

app.listen(3000, '0.0.0.0', () => {
    console.log('Frontend server running on port 3000');
});
