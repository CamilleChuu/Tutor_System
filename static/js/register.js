// const apiBaseUrl = 'https://tutor-system-app.herokuapp.com'; 

function Register() {
    var left = (screen.width/2)-500;
    var top = (screen.height/2);
    var features = 'left=' + left + ',top=' + top + ',width=750,height=500'; 
    var registerUrl = "static/popups/register.html";

    // var data = {
    //     username: username,
    //     password: password,
    //     nickname: nickname
    // };
    return new Promise((resolve, reject) => {
        const RegisterWindow = window.open(registerUrl, 'RegisterWindow', features );
        const checkWindowClosed = setInterval(() => {
          if (RegisterWindow.closed) {
              clearInterval(checkWindowClosed);
              resolve(); 
          }
      }, 100);
      });
}

function submitRegister(username, password, nickname) {
    $.ajax({
        // url: 'https://192.168.1.24:5001/register',
        url: 'https://tutor-system-app-7c5441f65344.herokuapp.com/register',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ "username": username, 'password': password, "nickname": nickname}),
        success: async function(response){
            window.alert(response.content);
        },
        error: function(xhr, status, error) {
            console.error("Error: " + status + " " + error);
        }
    });
}

function Login(username, password) {
    $.ajax({
        // url: 'https://192.168.1.24:5001/login',
        url: 'https://tutor-system-app-7c5441f65344.herokuapp.com/login',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ "username": username, 'password': password}),
        success: async function(response){
            if (response.success === 1) {
                localStorage.setItem('user', username);
                alert('Hello, '+response.content);
                window.location.href = '/welcomepage';
            } else{
                alert('Login Failed:'+username+'; '+password);
            }
        },
        error: function(xhr, status, error) {
            console.error("Error: " + status + " " + error);
        }
    });
}

function Logout() {
    localStorage.removeItem('user');
    window.location.href = '/';
}