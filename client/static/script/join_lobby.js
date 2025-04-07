document.addEventListener('DOMContentLoaded', function () {
    const joinForm = document.querySelector('form');
    if (joinForm) {
        joinForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const lobbyIdInput = document.querySelector('input[name="lobby_id"]');
            const lobbyId = lobbyIdInput.value.trim();

            if (lobbyId) {
                sessionStorage.setItem('joinedLobbyId', lobbyId);

                window.location.href = `/game?room_id=${lobbyId}`;
            }
        });
    }
});