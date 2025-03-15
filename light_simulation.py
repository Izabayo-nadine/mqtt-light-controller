import paho.mqtt.client as mqtt
import time
import sys
import signal
import logging
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# MQTT Configuration
MQTT_BROKER = "broker.emqx.io"  # Changed to EMQX's public broker
MQTT_PORT = 1883
MQTT_TOPIC = "/student_group/light_control"
MQTT_CLIENT_ID = f"light_simulator_{int(time.time())}"
MQTT_KEEPALIVE = 60
MAX_RECONNECT_ATTEMPTS = 5
reconnect_count = 0

# Global variables
client = None
light_state = "OFF"
is_connected = False

def publish_state():
    """Publish current light state."""
    if client and is_connected:
        client.publish(MQTT_TOPIC, light_state, qos=1, retain=True)
        logger.info(f"📤 Published state: {light_state}")

def on_connect(client, userdata, flags, rc):
    """Callback for when the client connects to the broker."""
    global is_connected, reconnect_count
    connection_codes = {
        0: "Connected successfully",
        1: "Incorrect protocol version",
        2: "Invalid client identifier",
        3: "Server unavailable",
        4: "Bad username or password",
        5: "Not authorized"
    }
    
    if rc == 0:
        is_connected = True
        reconnect_count = 0  # Reset reconnect counter on successful connection
        logger.info("✅ Connected to MQTT broker successfully")
        # Subscribe to the main topic and request topic
        client.subscribe([(MQTT_TOPIC, 1), (MQTT_TOPIC + "/request", 1)])
        logger.info(f"📡 Subscribed to topics: {MQTT_TOPIC}, {MQTT_TOPIC}/request")
        # Publish initial state
        publish_state()
    else:
        is_connected = False
        logger.error(f"❌ Connection failed with code {rc}: {connection_codes.get(rc, 'Unknown error')}")
        if reconnect_count >= MAX_RECONNECT_ATTEMPTS:
            logger.error("Maximum reconnection attempts reached. Exiting...")
            cleanup(None, None)

def on_disconnect(client, userdata, rc):
    """Callback for when the client disconnects from the broker."""
    global is_connected, reconnect_count
    is_connected = False
    if rc != 0:
        reconnect_count += 1
        logger.warning(f"❌ Unexpected disconnection ({reconnect_count}/{MAX_RECONNECT_ATTEMPTS}). Attempting to reconnect...")
        if reconnect_count >= MAX_RECONNECT_ATTEMPTS:
            logger.error("Maximum reconnection attempts reached. Exiting...")
            cleanup(None, None)
    else:
        logger.info("Disconnected successfully")

def on_message(client, userdata, msg):
    """Callback for when a message is received from the broker."""
    global light_state
    try:
        payload = msg.payload.decode().strip()
        topic = msg.topic

        if topic == MQTT_TOPIC + "/request" and payload == "STATUS":
            # Respond to status request
            publish_state()
            return

        if topic == MQTT_TOPIC:
            if payload in ["ON", "OFF"]:
                if payload != light_state:
                    light_state = payload
                    logger.info(f"💡 Light is TURNED {light_state}")
                    # Republish state to confirm change
                    publish_state()
            else:
                logger.warning(f"⚠️ Invalid command received: {payload}")
    except Exception as e:
        logger.error(f"❌ Error processing message: {e}")

def on_subscribe(client, userdata, mid, granted_qos):
    """Callback for when the client subscribes to a topic."""
    logger.info("✅ Subscription confirmed")

def cleanup(signum, frame):
    """Cleanup function to disconnect client properly."""
    logger.info("🛑 Shutting down...")
    if client and is_connected:
        # Publish offline status
        client.publish(MQTT_TOPIC, "Light simulator disconnected", qos=1, retain=True)
        client.disconnect()
    sys.exit(0)

def main():
    global client
    
    # Setup signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    # Create MQTT client instance with protocol v311
    client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=True, protocol=mqtt.MQTTv311)

    # Set callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe

    # Set last will message
    client.will_set(MQTT_TOPIC, 
                   payload="Light simulator disconnected unexpectedly", 
                   qos=1, 
                   retain=True)

    logger.info("🚀 Starting MQTT Light Simulator...")
    logger.info(f"📡 Broker: {MQTT_BROKER}")
    logger.info(f"📡 Port: {MQTT_PORT}")
    logger.info(f"📡 Topic: {MQTT_TOPIC}")

    try:
        # Connect to MQTT broker
        client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
        
        # Start network loop
        client.loop_forever()
    except KeyboardInterrupt:
        cleanup(None, None)
    except Exception as e:
        logger.error(f"❌ Failed to connect to broker: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 