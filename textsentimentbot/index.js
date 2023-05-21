'use strict';
const line = require('@line/bot-sdk'),
      express = require('express'),
      axios =require('axios'),
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
  //save to json server
  //Save to JSON Server
  let newData = {
    "sentiment": results[0].sentiment,
    "confidenceScore": results[0].confidenceScores[results[0].sentiment],
    "opinionText":""
  };

  if(results[0].sentences[0].opinions.length!=0){
    newData.opinionText = results[0].sentences[0].opinions[0].target.text;
  }

  let axios_add_data = {
    method:"post",
    url:"https://mynameispapupapuhahaha.azurewebsites.net/reviews",
    headers:{
      "content-type":"application/json"
    },
    data:newData
  };

  axios(axios_add_data)
  .then(function(response){
    console.log(JSON.stringify(response.data));
  })
  .catch(function(){
    console.log("Error!!");
  });

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