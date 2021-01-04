document.addEventListener('DOMContentLoaded', function () {
  const receivedTab = document.querySelector('#receivedTab');
  receivedTab.addEventListener('click', () => {
    displayReceived();
  });

  const sentTab = document.querySelector('#sentTab');
  sentTab.addEventListener('click', () => {
    displaySent();
  });
});

function displayReceived() {
  var receivedPanel = document.querySelector('#received');
  var receivedTab = document.querySelector('#receivedTab');
  receivedPanel.style.display = 'block';
  receivedTab.className = 'innerNavActive';

  var sentPanel = document.querySelector('#sent');
  var sentTab = document.querySelector('#sentTab');
  sentPanel.style.display = 'none';
  sentTab.className = 'innerNav';
}

function displaySent() {
  var receivedPanel = document.querySelector('#received');
  var receivedTab = document.querySelector('#receivedTab');
  receivedPanel.style.display = 'none';
  receivedTab.className = 'innerNav';

  var sentPanel = document.querySelector('#sent');
  var sentTab = document.querySelector('#sentTab');
  sentPanel.style.display = 'block';
  sentTab.className = 'innerNavActive';
}

function declineRequest(target) {
  var requestId = target.value;

  fetch('/declineRequest', {
    method: 'POST',
    body: JSON.stringify({
      requestId: requestId
    })
  })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      var requestDiv = document.querySelector(`#request-${requestId}`);
      requestDiv.remove();
    });
}

function acceptRequest(target) {
  var requestId = target.value;

  fetch('/acceptRequest', {
    method: 'POST',
    body: JSON.stringify({
      requestId: requestId
    })
  })
    .then(response => response.json())
    .then(result => {
      console.log(result);

      if (result.error) {
        alert(result.error);
      } else {
        var modalTitle = document.querySelector('#modalTitle');
        modalTitle.innerHTML = `Accepted ${result.requester}'s request`;

        var contactNumber = document.querySelector('#contactNumber');
        contactNumber.innerHTML = `<b>Contact Number: ${result.contactNumber}</b>`;

        var acceptedAlertModal = document.querySelector('#requestAccepted');
        acceptedAlertModal.className = 'modal fade show';
        acceptedAlertModal.style = 'display: block;';
        acceptedAlertModal.setAttribute('aria-hidden', 'false');
      }

      var requestDiv = document.querySelector(`#request-${requestId}`);
      requestDiv.remove();
    });
}

function closeAcceptModal() {
  var acceptedAlertModal = document.querySelector('#requestAccepted');
  acceptedAlertModal.className = 'modal fade';
  acceptedAlertModal.style = 'display: none;';
  acceptedAlertModal.setAttribute('aria-hidden', 'true');
}

function cancelRequest(target) {

    var requestId = target.value;
    
    fetch('/cancelRequest', {
        method: 'POST',
        body: JSON.stringify({
            requestId: requestId
        })
    }).then(response => response.json()).then(result =>{
        console.log(result);
        var requestDiv = document.querySelector(`#sent-request-${requestId}`);
        requestDiv.remove();
    })
}
