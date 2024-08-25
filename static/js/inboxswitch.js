function createEndBox() {
    const endingboxElement = document.createElement('div');
    const textNode = document.createTextNode('Activity Ends; Please Select Other Questions on the Top Bar.');
    endingboxElement.id = 'endboxbutton';
    endingboxElement.style.backgroundColor = '#f0f8ff'; 
    endingboxElement.style.color = 'black';              
    endingboxElement.style.width = '100%';             
    endingboxElement.style.padding = '10px';           
    endingboxElement.style.border = '1px solid #ddd';   
    endingboxElement.appendChild(textNode);
    return endingboxElement;
}

function createBeginBox() {
    const outerDiv = document.createElement('div');
    outerDiv.className = 'row';
    outerDiv.id = 'inputboxbutton';
    outerDiv.style.width = '100%';
    const colDiv = document.createElement('div');
    colDiv.className = 'col-sm-10';
    colDiv.style.width = '100%';
    const inputElement = document.createElement('input');
    inputElement.type = 'text';
    inputElement.id = 'userInput';
    inputElement.placeholder = 'Type your message here...';
    inputElement.autofocus = true;
    inputElement.style.width = '100%';
    colDiv.appendChild(inputElement);
    const buttonColDiv = document.createElement('div');
    buttonColDiv.className = 'col-sm-2';
    const button = document.createElement('button');
    button.id = 'submitBtn';
    button.type = 'button';
    button.className = 'btn btn-outline-dark';
    button.style.borderRadius = '50%';
    const icon = document.createElement('i');
    icon.className = 'fa fa-location-arrow';
    button.appendChild(icon);
    buttonColDiv.appendChild(button);
    outerDiv.appendChild(colDiv);
    outerDiv.appendChild(buttonColDiv);
    return outerDiv;
// const originalInputId = 'inputboxbutton';
// const originalInputElement = document.getElementById(originalInputId);
}

function toggleInputEndingBox() {
    const inputBoxElement = document.getElementById('inputboxbutton');
    const endBoxElement = document.getElementById('endboxbutton');
    if (inputBoxElement) {
        const newEndBoxElement = createEndingBox();
        inputBoxElement.parentNode.replaceChild(newEndBoxElement, inputBoxElement);
    } else if (endBoxElement) {
        const newInputBoxElement = createInputBox();
        endBoxElement.parentNode.replaceChild(newInputBoxElement, endBoxElement);
    }
}


export { toggleInputEndingBox };
export { createBeginBox };
export { createEndBox };