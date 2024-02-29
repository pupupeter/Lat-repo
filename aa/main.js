//大部分的CODE我沒有改變，我延續作業4的信心指數內容，可以讓網頁分析圖片時，也讓人知道AI準確性高不高

$(document).ready(function(){
  //do something
  $("#thisButton").click(function(){
      processImage();
  });
});

function processImage() {
  
  //確認區域與所選擇的相同或使用客製化端點網址
  var url = "https://eastus.api.cognitive.microsoft.com/";
  var uriBase = url + "vision/v2.1/analyze";
  
  var params = {
      "visualFeatures": "Faces,Adult,Brands,Categories,Description,",
      "details": "",
      "language": "zh",
  };
  //顯示分析的圖片
  var sourceImageUrl = document.getElementById("inputImage").value;
  document.querySelector("#sourceImage").src = sourceImageUrl;
  //送出分析
  $.ajax({
      url: uriBase + "?" + $.param(params),
      // Request header
      beforeSend: function(xhrObj){
          xhrObj.setRequestHeader("Content-Type","application/json");
          xhrObj.setRequestHeader("Ocp-Apim-Subscription-Key", subscriptionKey);
      },
      type: "POST",
      // Request body
      data: '{"url": ' + '"' + sourceImageUrl + '"}',
  })
  .done(function(data) {
    //顯示JSON內容
    $("#responseTextArea").val(JSON.stringify(data, null, 2));
    $("#picDescription").empty();

    var captions = data.description.captions;
    for (var i = 0; i < captions.length; i++) {
        $("#picDescription").append(captions[i].text + "<br>");
        $("#picDescription").append("信心指數: " + captions[i].confidence.toFixed(2) + "<br>");
    }

    $("#picDescription").append("這裡有" + data.categories.length + "個物件");
    $("#picDescription").append("這裡有" + data.faces.length + "個人");
    $("#picDescription").append("這裡針對人、物件(種類)、信心指數作分析");
})
  .fail(function(jqXHR, textStatus, errorThrown) {
      //丟出錯誤訊息
      var errorString = (errorThrown === "") ? "Error. " : errorThrown + " (" + jqXHR.status + "): ";
      errorString += (jqXHR.responseText === "") ? "" : jQuery.parseJSON(jqXHR.responseText).message;
      alert(errorString);
  });
};
