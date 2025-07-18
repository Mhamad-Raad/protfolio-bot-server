const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors({ origin: '*' }));
app.use(express.json());

app.get('/', (req, res) => res.send('Welcome to the API!'));

app.post('/api/chat', async (req, res) => {
  const { message } = req.body;

  try {
    const { Client } = await import('@gradio/client');
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
    res.status(500).json({ error: 'Failed to contact chatbot' });
  }
});

app.listen(PORT, () => {
  console.log(`✅ Server running on port ${PORT}`);
});
