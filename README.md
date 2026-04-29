# EdTech Honeypot

EdTech Honeypot is a security tool designed to simulate an EdTech student portal login service. It acts as a decoy to detect and log unauthorized access attempts, providing security researchers and administrators with insights into potential attacks.

## Features

- **Decoy Listener (`listener.py`)**: Simulates a fake student portal socket listener. It displays a realistic login banner and logs connection attempts.
- **Attack Logging (`attack_logger.py`)**: Records incoming IP addresses, ports, and connection attempts to a local `logs.json` file.
- **Web Dashboard (`dashboard.py`)**: Provides a visual interface to monitor the honeypot activity and view the logged attack data in real-time.

## Project Structure

```
honeypot_edtech/
├── listener.py        # The main honeypot socket server
├── dashboard.py       # Web application for monitoring
├── attack_logger.py   # Utility to log incoming connections
├── logs.json          # Data storage for logged attacks
├── templates/         # HTML templates for the dashboard
└── static/            # Static assets for the dashboard
```

## Getting Started

### Prerequisites

- Python 3.x

### Running the Honeypot

1. **Start the Listener:**
   Run the listener script to start accepting connections on the configured port (default is `8080`).
   ```bash
   python listener.py
   ```
   *Optional:* You can specify a custom host and port:
   ```bash
   python listener.py --host 0.0.0.0 --port 8080
   ```

2. **Start the Dashboard:**
   In a separate terminal window, start the dashboard application to monitor the logs.
   ```bash
   python dashboard.py
   ```
   The dashboard will be accessible at `http://127.0.0.1:5000`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
