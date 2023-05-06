'use strict';
const line = require('@line/bot-sdk'),
      express = require('express'),
      configGet = require('config');
const { TextAnalyticsClient, AzureKeyCredential } = require("@azure/ai-text-analytics");

// Line config
const configLine = {
  channelAccessToken: configGet.get("CHANNEL_ACCESS_TOKEN"),
  channelSecret: configGet.get("CHANNEL_SECRET")
};

// Azure Text Sentiment
const endpoint = configGet.get("ENDPOINT");
const apiKey = configGet.get("TEXT_ANALYTICS_API_KEY");

const client = new line.Client(configLine);
const app = express();

const port = process.env.PORT || process.env.port || 3001; // NGROK http 3001

app.listen(port, () => {
  console.log(`listening on ${port}`);
});

async function analyzeTextSentiment(text) {
  console.log("[analyzeTextSentiment] in");
  const analyticsClient = new TextAnalyticsClient(endpoint, new AzureKeyCredential(apiKey));
  const results = await analyticsClient.analyzeSentiment([text], "zh-Hant", {
    includeOpinionMining: true
  });

  console.log("[results] ", JSON.stringify(results));

  const sentiment = results[0].sentiment;
  const confidenceScores = results[0].confidenceScores;

  return {
    sentiment: sentiment,
    confidenceScores: confidenceScores
  };
}

app.post('/callback', line.middleware(configLine), (req, res) => {
  Promise
    .all(req.body.events.map(handleEvent))
    .then((result) => res.json(result))
    .catch((err) => {
      console.error(err);
      res.status(500).end();
    });
});

function handleEvent(event) {
  if (event.type !== 'message' || event.message.type !== 'text') {
    return Promise.resolve(null);
  }

  const text = event.message.text;

  return analyzeTextSentiment(text)
    .then((result) => {
      const { sentiment, confidenceScores } = result;
      const confidence = Math.round(confidenceScores[sentiment] * 100);

      const replyText = `該文本的情感分析結果為 ${sentiment}，信心指數為 ${confidence}%。`;

      const echo = {
        type: 'text',
        text: replyText
      };

      return client.replyMessage(event.replyToken, echo);
    })
    .catch((err) => {
      console.error("Error:", err);
    });
}