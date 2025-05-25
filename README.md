# Ludo Game 🎲

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern implementation of the classic Ludo board game, built with Python Flask. Challenge your friends in this exciting multiplayer game of strategy and luck!

## ✨ Features

- **Multiplayer Gameplay**: Play with up to 4 players in real-time
- **Lobby System**: Create and join game lobbies with unique codes
- **Interactive UI**: Beautiful and responsive game interface
- **Cross-Platform**: Play on any device with a web browser
- **Persistent Sessions**: Rejoin your games with cookies-based authentication

## 🚀 Getting Started

### Prerequisites

- Python 3.6+
- Flask 3.1.0
- Web browser

## 🎮 How to Play

1. Create a new game lobby or join an existing one with a code
2. Wait for all players to join (2-4 players)
3. Roll the dice and move your pawns according to the rules
4. The first player to get all pawns to the center wins!

## 🏗️ Project Structure

```
├── api/                # Backend Flask application
│   ├── app.py          # Main application entry point
│   ├── lobby_handler.py # Game logic and lobby management
│   └── requirements.txt # Python dependencies
├── client/             # Frontend assets
│   ├── static/         # CSS and JavaScript files
│   └── templates/      # HTML templates
└── docs/               # Documentation
    └── html/           # Doxygen generated documentation
```

## 📚 Documentation

Detailed API documentation is available in the [docs/html](docs/html/index.html) directory. Open `index.html` in your browser to view the complete Doxygen documentation.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [Doxygen](https://www.doxygen.nl/) - Used to generate API documentation