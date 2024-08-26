function GetSessionID(userInput, username) {
  return new Promise((resolve, reject) => {
    $.ajax({
      url: 'https://tutor-system-app-7c5441f65344.herokuapp.com/get_sessionid',
      // url: 'http://149.28.76.168:5001/get_sessionid', 
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({"question": userInput, "user": username}),
      success: function(response) {
          localStorage.setItem('session_id', response);
          localStorage.setItem('user', username);
          localStorage.setItem('question', userInput);
          resolve(response); 
        //   session_id = response;
          },
      error: function(xhr, status, error) {
          console.error("Error: " + status + " " + error);
          reject(error);
          }
      });
    });
  }

async function navigateToPage() {
  var selectedOption = document.getElementById("pageSelect").value;
  var user = localStorage.getItem('user');
  if (selectedOption) {
    try {
      await GetSessionID(selectedOption, user);
      OpeningOutput(selectedOption);
    } catch (error) {
        console.error('An error occurred:', error);
    }
  }
}

async function navigateFromProgress(selectedOption) {
  localStorage.setItem('question2', -1);
  var user = localStorage.getItem('user');
  if (selectedOption) {
    try {
      await GetSessionID(selectedOption, user);
      OpeningOutput(selectedOption);
    } catch (error) {
        console.error('An error occurred:', error);
    }
  }
}

function updateUsername() {
  var user = localStorage.getItem('user');
  if (user) {
      document.getElementById('user-display').textContent = 'ACCOUNT: ' + user;
  } else {
      window.location.href = '/';
  }
}

function getProgress() {
  var user = localStorage.getItem('user');
    $.ajax({
      url: 'https://tutor-system-app-7c5441f65344.herokuapp.com/get_progress',
        // url: 'http://149.28.76.168:5001/get_progress', 
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({"user": user}), 
        success: function(response) {
            updateUIBasedOnCriteria(response);
        },
        error: function(xhr, status, error) {
            reject(new Error('Error fetching session ID: ' + error));
        }
      });
}

function updateUIBasedOnCriteria(progressData) {
  progressData.forEach(questionName => {
      const item = document.querySelector(`.item[question-name="${questionName}"]`);
      if (item) {
          const dot = item.querySelector('span:nth-child(2)');
          if (!dot.classList.contains('green-dot')) { 
              dot.classList.remove('red-dot'); 
              dot.classList.add('green-dot'); 
          }
      }
  });
}

// async function navigateToPage2() {
//   window.location.href = '/welcomepage';
// }

function setupEventHandlers() {
  const buttons = document.querySelectorAll('.item button');  // Select all buttons within each item
  buttons.forEach(button => {
      button.onclick = function() {
          const questionName = this.parentNode.getAttribute('question-name');  // Get the question-name from the parent div
          navigateToPage2(questionName);
      };
  });
}

function navigateToPage2(selectedOption) {
  var user = localStorage.getItem('user');
  if (selectedOption) {
    try {
        GetSessionID(selectedOption, user).then(() => {
          localStorage.setItem('question2', selectedOption);
          window.location.href = '/welcomepage';
        }).catch((error) => { 
            console.error('An error occurred:', error);
        });
    } catch (error) {
        console.error('An error handling exception:', error);
    }
} else {
    console.error('No question selected');
}
}

function checkAndNavigate() {
  if (localStorage.getItem('question2') !== '-1') {
    let Question = localStorage.getItem('question2');
    localStorage.setItem('question2', -1);
    navigateFromProgress(Question);
  } else {
      console.log("No 'question' item found in localStorage.");
  };
}