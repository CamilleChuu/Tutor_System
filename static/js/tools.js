function openPopupCalculator() {
    var top = screen.height;
    var left = (screen.width/2) - (window.innerWidth/2);
    var features = 'left=' + left + ',top=' + top + ',width=750,height=400'; 
    return new Promise((resolve, reject) => {
      const CalculatorWindow = window.open(calculatorUrl, 'CalculatorWindow', features);
      const checkWindowClosed = setInterval(() => {
        if (CalculatorWindow.closed) {
            clearInterval(checkWindowClosed);
            resolve(); // Resolve the promise when the window is closed
        }
    }, 100);
    });
  }
  
function openPopupDragboard() {
    var left = (screen.width/2)-500;
    var top = (screen.height/2);
    var features = 'left=' + left + ',top=' + top + ',width=750,height=500'; 
    return new Promise((resolve, reject) => {
      const DragboardWindow = window.open(dragboardUrl, 'DragboardWindow', features );
      const checkWindowClosed = setInterval(() => {
        if (DragboardWindow.closed) {
            clearInterval(checkWindowClosed);
            resolve(); 
        }
    }, 100);
    });
  }
  
function openPopupWhiteboard(){
    var left = (screen.width/2)-500;
    var top = (screen.height/2);
    var features = 'left=' + left + ',top=' + top + ',width=750,height=500'; 
    return new Promise((resolve, reject) => {
      const DragboardWindow = window.open(whiteboardUrl, 'WhiteboardWindow', features );
      const checkWindowClosed = setInterval(() => {
        if (DragboardWindow.closed) {
            clearInterval(checkWindowClosed);
            resolve(); 
        }
    }, 100);
    });
  }

function updateImage(InputQuestion) {
    var imgElement = document.querySelector('.figure-section img');
    if (imgElement) {
        imgElement.src = imageMap[InputQuestion];
        imgElement.alt = 'Figure';
        imgElement.id = 'figure';
    } else {
        console.error('Image element not found.');
    }
}

function updateImage2(ImageDir) {
  var imgElement = document.querySelector('.figure-section img');
  if (imgElement) {
      imgElement.src = ImageDir;
      imgElement.alt = 'Figure';
      imgElement.id = 'figure';
  } else {
      console.error('Image element not found.');
  }
}

function openNewImage(ImageDir) {
    var imgElement = document.querySelector('.figure-section img');
    if (imgElement) {
        imgElement.src = ImageDir;
        imgElement.alt = 'Figure';
        imgElement.id = 'figure';
    } else {
        console.error('Image element not found.');
    }
  }

function resizeImageToFit(container, img) {
  var widthRatio = container.offsetWidth / img.naturalWidth;
  var heightRatio = container.offsetHeight / img.naturalHeight;

  var styleString = '';
  if (widthRatio < heightRatio) {
      styleString = 'width: 100%; height: auto;';
  } else {
      styleString = 'width: auto; height: 100%;';
  }
  return styleString;
}

function openVideoPopup(videoName) {
  var left = (screen.width / 2) - 500; 
  var top = (screen.height / 2) - 300; 
  var width = 750;
  var height = 500; 
  var features = `left=${left},top=${top},width=${width},height=${height}`;

  var videoPlayerUrl =  videoName;

  return new Promise((resolve, reject) => {
      const videoWindow = window.open(videoPlayerUrl, 'VideoPlayerWindow', features);
      if (!videoWindow) {
          reject(new Error('Failed to open video window'));
          return;
      }
      videoWindow.focus();
      const checkWindowClosed = setInterval(() => {
          if (videoWindow.closed) {
              clearInterval(checkWindowClosed);
              resolve();
          }
      }, 100);
  });
}