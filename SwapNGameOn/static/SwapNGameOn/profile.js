document.addEventListener('DOMContentLoaded', function () {
  const deleteBtns = document.querySelectorAll('.redBtn');
  deleteBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      deleteGame(btn);
    });
  });

  const submitRatingBtn = document.querySelector('#submit-rating');
  submitRatingBtn.addEventListener('click', () => {
    submitRating(submitRatingBtn);
  });
});

function deleteGame(target) {
  var gameId = target.value;
  var gameDiv = document.querySelector(`#game-${gameId}`);

  fetch('/deleteGame', {
    method: 'POST',
    body: JSON.stringify({
      gameId: gameId
    })
  })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      gameDiv.remove();
    });
}

function submitRating(target) {
  var user = target.value;
  var radioStarBtns = document.querySelectorAll('.form-check-input');
  var ratingScore = null;

  for (btn of radioStarBtns) {
    if (btn.checked) {
      ratingScore = btn.value;
      break;
    }
  }

  fetch('/addRating', {
    method: 'POST',
    body: JSON.stringify({
      user: user,
      rating: ratingScore
    })
  })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      location.reload();
    });
}
