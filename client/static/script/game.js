let roomId = document.getElementById('room-id').textContent;
let playerId = document.getElementById('player-id').textContent;
let isYourTurn = false;
let gameInterval = null;


const rollDiceBtn = document.getElementById('roll-dice-btn');
const diceResult = document.getElementById('dice-result');
const turnMessage = document.getElementById('turn-message');
const playersConnected = document.getElementById('players-connected');
const currentPlayer = document.getElementById('current-player');
const lastRoll = document.getElementById('last-roll');

function initGame() {

    rollDiceBtn.addEventListener('click', rollDice);

    updateGameStatus();
    gameInterval = setInterval(updateGameStatus, 2000); // Update every 2 seconds
}

async function updateGameStatus() {
    try {
        const response = await fetch(`/get_room_status?room_id=${roomId}`);
        if (!response.ok) {
            throw new Error('Failed to get room status');
        }

        const data = await response.json();

        playersConnected.textContent = data.players_connected;

        if (data.current_player && data.players[data.current_player]) {
            currentPlayer.textContent = data.players[data.current_player].name;
        } else {
            currentPlayer.textContent = 'Waiting...';
        }

        if (data.last_roll) {
            lastRoll.textContent = data.last_roll;
        } else {
            lastRoll.textContent = 'None';
        }

        isYourTurn = data.is_your_turn;

        if (data.players_connected < 2) {
            turnMessage.textContent = 'Waiting for more players to join...';
            rollDiceBtn.disabled = true;
        } else if (isYourTurn) {
            turnMessage.textContent = 'It\'s your turn! Roll the dice.';
            rollDiceBtn.disabled = false;
        } else {
            turnMessage.textContent = `Waiting for ${data.players[data.current_player].name} to roll...`;
            rollDiceBtn.disabled = true;
        }

    } catch (error) {
        console.error('Error updating game status:', error);
    }
}

async function rollDice() {
    if (!isYourTurn) {
        return;
    }

    rollDiceBtn.disabled = true;

    try {
        const response = await fetch(`/dice_roll?room_id=${roomId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to roll dice');
        }

        const data = await response.json();

        animateDiceRoll(data.dice_value);

        turnMessage.textContent = `You rolled a ${data.dice_value}. Now it's ${data.next_player}'s turn.`;

        setTimeout(updateGameStatus, 1000);

    } catch (error) {
        console.error('Error rolling dice:', error);
        rollDiceBtn.disabled = false;
    }
}

function animateDiceRoll(finalValue) {
    let count = 0;
    const animationInterval = setInterval(() => {
        const randomValue = Math.floor(Math.random() * 6) + 1;
        diceResult.textContent = `🎲 ${randomValue}`;

        count++;
        if (count > 10) {
            clearInterval(animationInterval);
            diceResult.textContent = `🎲 ${finalValue}`;
        }
    }, 100);
}

initGame();