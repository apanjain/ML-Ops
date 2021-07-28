function checkLogs(user, train_filelocation) {
  var updateLoop = null;
  updateLiveData = function () {
    var now = new Date();
    var url = `/logs/${user}/?&train_filelocation=${train_filelocation}&${now}`;
    console.log("updating...");
    fetch(url)
      .then((res) => {
        res.text().then(function (text) {
          dataDiv = document.getElementById("liveData");
          dataDiv.innerHTML = text;
          // Checkpoint for terminating updates
          if (
            text.length > 13 &&
            text.substring(text.length - 13) === "!!</p><p></p>"
          ) {
            console.log("terminating...");
            clearInterval(updateLoop);
          }
          window.scrollTo(0, document.body.scrollHeight);
        });
      })
      .catch((err) => {
        console.log("terminating...");
        clearInterval(updateLoop);
        console.log(err);
      });
  };
  updateLiveData();
  updateLoop = setInterval(updateLiveData, 1000);
}
