function sendUserInput(userInput) {
    var session_id = localStorage.getItem('session_id');
    var question = localStorage.getItem('question');
    if (userInput.trim() !== '') {
      $.ajax({
        url: 'https://tutor-system-app-7c5441f65344.herokuapp.com/dialogue_new',
        // url: 'http://149.28.76.168:5001/dialogue_new', // Make sure this matches the Flask app's URL and port
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ "userInput": userInput, 'question': question, "sessionID": session_id}),
        success: async function(response) {
            $('#dialogueSection .answer.left:last').remove();
            let is_end = false;
            let is_begin = false;
            for (const step of response) {
              if (step.end === 1){
                var session_id = null; // the last step of each dialogue: initialze the session id;
                is_end = true;
              };
              if (step.end === -1){
                if (is_begin === false) {
                  $('#openingText').empty();
                  updateImage2('./static/images/blank.jpg');
                };
                is_begin = true;
              };
              
              if (step.type === 'text') {
                $('#dialogueSection').append('<div class="answer left"> <div class="avatar"> <img src="./static/images/avatar/gpt.png" alt="System name"> <div class="status offline"></div> </div> <div class="name">System</div> <div class="text">' + step.content + ' </div> </div>');
                scrollToBottom();
                if (is_begin === true) {
                    $('#openingText').append("<p>" + step.content + "</p>");
                };
                await new Promise(resolve => setTimeout(resolve, 1500));
              } else if (step.type === 'action') {
                if (is_begin === true && step.content.startsWith("openNewImage") ) {
                  const functionNameMatch = step.content.match(/\((.*?)\)/);
                  const imagepath = functionNameMatch[1];
                  updateImage2(imagepath);
                };
                if (step.content.slice(-2) === "()") {
                  const functionName = step.content.replace(/\(\)$/, ""); 
                if (window[functionName] && typeof window[functionName] === "function") {await window[functionName](); } 
                } else if (step.content.includes("openNewImage(")){
                  const functionNameMatch = step.content.match(/\((.*?)\)/);
                  const imagepath = functionNameMatch[1];
                  openNewImage(imagepath);
                } else if (step.content.includes("openNewVideo(")){
                  const functionNameMatch = step.content.match(/\((.*?)\)/);
                  const imagepath = functionNameMatch[1];
                  await openVideoPopup(imagepath);
                }
              };
            };
              if (is_end === true) {
                $('#dialogueSection').append('<div class="answer left"> <div class="avatar"> <img src="./static/images/avatar/gpt.png" alt="System name"> <div class="status offline"></div> </div> <div class="name">System</div> <div class="text">' + "This is the end of this activity."+ ' </div> </div>');
                scrollToBottom();
                document.getElementById('end_box').style.visibility = 'visible';
                document.getElementById('inputboxbutton').style.visibility = 'hidden';
            };
        },
        error: function(xhr, status, error) {
            console.error("Error: " + status + " " + error);
        
        }
    });
    }
  }