// import { createEndBox } from './toggleInputEndingBox.js';

var question = null;
var session_id = null;
var user = user;

$(function(){
    // $(".chat").niceScroll();
    
    var chatmessages = [{
        username : 'bot',
        name: 'TutorSys',
        avatar: './image/avatar/chat1.png',
        text: 'Text 1',
        ago: '5 min ago' 
        
    },
    {
        username : 'user',
        name: 'TutorUser',
        avatar: './image/avatar/chat2.png',
        text: 'Text 2',
        ago: '2 min ago' 
        
    }];
    
    let htmldiv = ``;
    jQuery.each( chatmessages, function( i, item ) {

        let position = item.username=='bot'? 'left': 'right';
        let ago = item.ago;
        htmldiv += `<div class="answer ${position}">
                <div class="avatar">
                  <img src="${item.avatar}" alt="${item.name}">
                  <div class="status offline"></div>
                </div>
                <div class="name">${item.name}</div>
                <div class="text">
                  ${item.text}
                </div>
                <div class="time">${ago}</div>
              </div>`;
    });
    
    $("div#chat-messages" ).html(htmldiv);

}) 


function receiveSize(width, height) {
  document.getElementById('size').textContent = `Size: ${width}x${height}`;
  }

  $(document).ready(function() {
    $("#submitBtn").click(function() {
      var userInput = $('#userInput').val();
      $('#userInput').val(''); // Clear input field after sending
      publishUserInput(userInput);
      sendUserInput(userInput);
    });
    $('#userInput').keypress(function(e) {
        if (e.which === 13) { // Enter key pressed
          var userInput = $('#userInput').val();
          $('#userInput').val(''); // Clear input field after sending
          publishUserInput(userInput);
          sendUserInput(userInput);
        }
    });
    });

function publishUserInput(userInput) {
  if (userInput.trim() !== '') {
    $('#dialogueSection').append('<div class="answer right"> <div class="avatar"> <img src="./static/images/avatar/user.png" alt="User name"> <div class="status offline"></div> </div><div class="name">User</div> <div class="text">' +  userInput + ' </div>  </div>');
    // Append the element for the animation of three dots
    // Append the userInput with waiting animation
    $('#dialogueSection').append('<div class="answer left"> <div class="avatar"> <img src="./static/images/avatar/gpt.png" alt="User name"> <div class="status offline"></div> </div><div class="name">User</div> <div class="waiting-animation">...</div> </div>')
    scrollToBottom();
    } 
  }

function OpeningOutput(userInput) {
    var session_id = localStorage.getItem('session_id');
    var question = localStorage.getItem('question');
    document.getElementById('end_box').style.visibility = 'hidden';
    document.getElementById('inputboxbutton').style.visibility = 'visible';
    $('#dialogueSection').empty();
    $.ajax({
      url: 'http://149.28.76.168:5001/dialogue_open', // Make sure this matches the Flask app's URL and port
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ "question": question, "sessionID": session_id }),
      success: async function(response) {
        $('#openingText').empty();
        updateImage2('./static/images/blank.jpg');
        for (const step of response) {
          if (step.type === 'text') {
            $('#openingText').append("<p>" + step.content + "</p>");
            } else  if (step.type === 'action' && step.content.startsWith("openNewImage")) {
              const functionNameMatch = step.content.match(/\((.*?)\)/);
              const imagepath = functionNameMatch[1];
              updateImage2(imagepath);
              // let regex = /\((.*?)\)/;
              // let img_path = regex.exec(step.content)[1];
              }
          }

        for (const step of response) {
          if (step.type === 'text') {
            $('#dialogueSection').append('<div class="answer left"> <div class="avatar"> <img src="./static/images/avatar/gpt.png" alt="System name"> <div class="status offline"></div> </div> <div class="name">System</div> <div class="text">' + step.content + ' </div> </div>');
            scrollToBottom();
            await new Promise(resolve => setTimeout(resolve, 1500));
          } 
          }
        },
      error: function(xhr, status, error) {
          console.error("Error: " + status + " " + error);
      }
    });
  }

function scrollToBottom() {
  var element = document.querySelector('.chat-body');
  element.scrollTop = element.scrollHeight;
}

function sendUserInput(userInput) {
  var session_id = localStorage.getItem('session_id');
  var question = localStorage.getItem('question');
  if (userInput.trim() !== '') {
    $.ajax({
      url: 'http://149.28.76.168:5001/dialogue_new', // Make sure this matches the Flask app's URL and port
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
          }
        };
        if (is_end === true) {
          $('#dialogueSection').append('<div class="answer left"> <div class="avatar"> <img src="./static/images/avatar/gpt.png" alt="System name"> <div class="status offline"></div> </div> <div class="name">System</div> <div class="text">' + "This is the end of this activity."+ ' </div> </div>');
          scrollToBottom();
          document.getElementById('end_box').style.visibility = 'visible';
          document.getElementById('inputboxbutton').style.visibility = 'hidden';
      };
      }
    });
  };
};