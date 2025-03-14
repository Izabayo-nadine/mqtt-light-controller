# IoT Light Control System

A web-based IoT light control system that demonstrates MQTT communication between a web interface and a simulated IoT device (ESP8266). The system allows users to control a virtual light through a modern web interface while a Python script simulates the IoT device's behavior.

## 🌟 Features

- **Modern Web Interface**

  - Real-time light control
  - Connection status indicator
  - Visual feedback for light state
  - Error handling and notifications
  - Responsive design

- **IoT Device Simulator**
  - Real-time state management
  - Automatic reconnection
  - Detailed logging
  - Graceful error handling
  - Clean shutdown process

## 🛠️ Technologies Used

- **Frontend**

  - HTML5
  - CSS3 (with modern features like glassmorphism)
  - JavaScript
  - MQTT.js for WebSocket communication

- **Backend (Simulator)**

  - Python 3.x
  - paho-mqtt library
  - Logging system

- **Communication**
  - MQTT Protocol
  - EMQX Public Broker
  - WebSocket for web interface
  - Standard MQTT for Python simulator

## 📋 Prerequisites

1. Python 3.x installed
2. Modern web browser (Chrome, Firefox, Safari, Edge)
3. Internet connection for MQTT broker access

## ⚙️ Setup Instructions

1. **Install Python Dependencies**

   ```bash
   pip install paho-mqtt
   ```

2. **Project Structure**
   ```
   mqtt-light-control/
   ├── index.html         # Web interface
   ├── light_simulation.py # IoT device simulator
   └── README.md          # Documentation
   ```

## 🚀 Running the System

1. **Start the IoT Device Simulator**

   ```bash
   python light_simulation.py
   ```

   You should see logs indicating successful connection to the MQTT broker.

2. **Launch the Web Interface**
   - Open `index.html` in a web browser
   - The interface should connect automatically to the MQTT broker
   - Check browser console for connection status

## 💡 Usage

1. **Controlling the Light**

   - Click "TURN ON" to turn the light on
   - Click "TURN OFF" to turn the light off
   - The light bulb icon provides visual feedback
   - Status messages show the current state

2. **Monitoring Connection**
   - Green indicator: Connected
   - Red indicator: Disconnected
   - Status messages show connection state
   - Error messages appear when issues occur

## 🔍 Troubleshooting

1. **Connection Issues**

   - Check internet connection
   - Verify broker status (broker.emqx.io)
   - Check browser console for errors
   - Review Python script logs

2. **Common Error Messages**
   - "Not connected to MQTT broker": Wait for reconnection or restart
   - "Failed to connect": Check network/firewall settings
   - "Maximum reconnection attempts reached": Restart the system

## 🔒 Security Notes

- This demo uses a public MQTT broker (broker.emqx.io)
- No authentication implemented (educational purposes only)
- For production, use:
  - Secure broker with authentication
  - SSL/TLS encryption
  - Access control
  - Environment variables for credentials

## 🤝 Contributing

Feel free to:

- Report bugs
- Suggest improvements
- Submit pull requests

## 📝 License

This project is open-source and available under the MIT License.

## ✨ Acknowledgments

- EMQX for providing the public MQTT broker
- MQTT.js team for the JavaScript client library
- Eclipse Paho for the Python MQTT client
