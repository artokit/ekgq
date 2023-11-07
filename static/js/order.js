const socket = new WebSocket('ws://127.0.0.1:8000/ws');

socket.onopen = function(e) {
  socket.send(JSON.stringify({
    message: window.location.href.split('/').at(-2)
  }));
};

socket.onmessage = function(event) {
    addNewElement(JSON.parse(event.data));
};


let table = document.querySelector('.TableViewReports table');


let addNewElement = (obj) => {
    let tr = document.createElement('tr');
    
    let number_td = document.createElement('td');
    number_td.textContent = obj.number;
    tr.appendChild(number_td);
    
    let device_td = document.createElement('td');
    device_td.textContent = obj.device;
    tr.appendChild(device_td);
    
    let email_td = document.createElement('td');
    email_td.textContent = obj.email;
    tr.appendChild(email_td);
    
    let text_td = document.createElement('td');
    text = '';
    for (let i of obj.text.split('\n')) {
        text += `<p>${i}</p>`
    }
    text_td.innerHTML = text;
    text_td.className = 'notCenterTd';
    tr.appendChild(text_td);

    table.appendChild(tr);
    tr.className = 'animateTr';
}
