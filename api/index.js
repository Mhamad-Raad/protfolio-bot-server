const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(
  cors({
    origin: '*',
    methods: ['GET', 'POST', 'OPTIONS'],
    allowedHeaders: ['Content-Type'],
  })
);

app.use(express.json());

app.options('*', cors());

app.get('/', (req, res) => res.send('Welcome to the Portfolio Chat Bot API!'));

app.post('/api/chat', async (req, res) => {
  try {
    const { Client } = await import('@gradio/client');
    const { message } = req.body;

    const client = await Client.connect('mhamad69/Portfolio-Chat-Bot');
    const result = await client.predict('/chat', {
      message,
      max_tokens: 300,
      temperature: 0.3,
      top_p: 0.9,
    });

    res.json({ reply: result.data });
  } catch (error) {
    console.error(error);
    res
      .status(500)
      .json({ error: 'Server error while contacting Gradio client' });
  }
});

module.exports = app;
