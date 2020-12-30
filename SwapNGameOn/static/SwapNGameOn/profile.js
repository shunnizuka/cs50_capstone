document.addEventListener('DOMContentLoaded', function () {
  const deleteBtns = document.querySelectorAll('.redBtn');
  deleteBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      deleteGame(btn);
    });
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
