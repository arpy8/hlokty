const axios = require('axios');
const express = require('express');

const app = express();
const PORT = process.env.PORT || 3000;

const TOKEN = process.env.IPG_BOT_TOKEN;
const CHANNEL_ID = process.env.IPG_CHANNEL_ID;

const url = `https://discord.com/api/v10/channels/${CHANNEL_ID}/messages`;

app.get("/", (req, res) => {
  res.json({ "NOTE": "Do not use this library. It is for experimental purposes only." });
});

app.post("/data", async (req, res) => {
  try {
    const { data } = req.body;

    if (!data) {
      return res.status(400).json({ error: "Data not provided" });
    }

    await sendMessage(data);
    res.json("sent successfully");
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal server error" });
  }
});

async function sendMessage(message) {
  if (message.length <= 2000) {
    const data = {
      content: message,
    };

    try {
      const response = await axios.post(url, data, {
        headers: {
          'Authorization': `Bot ${TOKEN}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.status !== 200) {
        console.error(`Failed to send message. Status code: ${response.status}, Response: ${response.data}`);
      }
    } catch (error) {
      console.error("Error sending message:", error.message);
    }
  } else {
    await sendMessage(message.slice(0, 2000));
    await sendMessage(message.slice(2000));
  }
}

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});