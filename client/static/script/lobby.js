document.addEventListener('DOMContentLoaded', function () {
    const getIdButton = document.querySelector('.button:not([type="submit"])');
    const uniqueIdDiv = document.getElementById('uniqueId');
    const startGameButton = document.querySelector('button[type="submit"]');

    function generateLobbyId() {
        return Math.floor(1000 + Math.random() * 9000).toString();
    }

    function storeLobbyId(id) {
        sessionStorage.setItem('lobbyId', id);
    }

    function displayLobbyId() {
        const lobbyId = generateLobbyId();
        uniqueIdDiv.textContent = `Lobby ID: ${lobbyId}`;
        uniqueIdDiv.style.fontSize = '24px';
        uniqueIdDiv.style.fontWeight = 'bold';
        uniqueIdDiv.style.margin = '20px 0';

        storeLobbyId(lobbyId);

        const form = document.querySelector('form');
        form.action = `/game?room_id=${lobbyId}`;
    }

    if (getIdButton) {
        getIdButton.addEventListener('click', displayLobbyId);
    }
});