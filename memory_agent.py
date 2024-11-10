import logging
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

class MemoryAgent:
    def __init__(self):
        # Retrieve Neo4j connection details from environment variables
        uri = os.getenv('NEO4J_URI')
        user = os.getenv('NEO4J_USERNAME')
        password = os.getenv('NEO4J_PASSWORD')

        # Log URI and username (not password for security reasons)
        logging.info(f"Connecting to Neo4j with URI: {uri} and User: {user}")

        # Validate that credentials are not None
        if not uri or not user or not password:
            logging.error("One or more environment variables are missing. Please check NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD.")
            raise ValueError("Missing required environment variables for Neo4j connection.")

        # Attempt to connect and verify authentication
        try:
            # Use (user, password) tuple for Neo4j connection
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            # Test the connection with a simple query to ensure credentials are valid
            with self.driver.session() as session:
                session.run("RETURN 1")
                logging.info("Connected to Neo4j and authenticated successfully.")
        except Exception as e:
            logging.error(f"Failed to connect to Neo4j: {e}")
            raise e

    def close(self):
        if self.driver is not None:
            self.driver.close()
            logging.info("Closed Neo4j connection")

    def add_memory(self, user_id, memory):
        logging.info(f"Adding memory for user_id: {user_id}")
        with self.driver.session() as session:
            try:
                session.write_transaction(self._create_and_return_memory, user_id, memory)
                logging.info(f"Memory added successfully for user_id: {user_id}")
            except Exception as e:
                logging.error(f"Failed to add memory for user_id {user_id}: {e}")

    @staticmethod
    def _create_and_return_memory(tx, user_id, memory):
        query = (
            "MERGE (u:User {id: $user_id}) "
            "CREATE (u)-[:HAS_MEMORY]->(m:Memory {content: $memory, timestamp: datetime()}) "
            "RETURN m"
        )
        result = tx.run(query, user_id=user_id, memory=memory)
        return result.single()

    def retrieve_memories(self, user_id):
        logging.info(f"Retrieving memories for user_id: {user_id}")
        with self.driver.session() as session:
            try:
                result = session.read_transaction(self._get_memories, user_id)
                memories = [record["memory_content"] for record in result]
                logging.info(f"Retrieved {len(memories)} memories for user_id: {user_id}")
                return memories
            except Exception as e:
                logging.error(f"Failed to retrieve memories for user_id {user_id}: {e}")
                return []

    @staticmethod
    def _get_memories(tx, user_id):
        query = (
            "MATCH (u:User {id: $user_id})-[:HAS_MEMORY]->(m:Memory) "
            "RETURN m.content AS memory_content ORDER BY m.timestamp DESC"
        )
        return tx.run(query, user_id=user_id)

    def add_user_preference(self, user_id, preference):
        logging.info(f"Adding preference for user_id: {user_id}")
        with self.driver.session() as session:
            try:
                session.write_transaction(self._create_and_return_preference, user_id, preference)
                logging.info(f"Preference added successfully for user_id: {user_id}")
            except Exception as e:
                logging.error(f"Failed to add preference for user_id {user_id}: {e}")

    @staticmethod
    def _create_and_return_preference(tx, user_id, preference):
        query = (
            "MERGE (u:User {id: $user_id}) "
            "MERGE (p:Preference {name: $preference}) "
            "MERGE (u)-[:HAS_PREFERENCE]->(p) "
            "RETURN p"
        )
        tx.run(query, user_id=user_id, preference=preference)

    def get_user_preferences(self, user_id):
        logging.info(f"Retrieving preferences for user_id: {user_id}")
        with self.driver.session() as session:
            try:
                result = session.read_transaction(self._get_preferences, user_id)
                preferences = [record["preference_name"] for record in result]
                logging.info(f"Retrieved {len(preferences)} preferences for user_id: {user_id}")
                return preferences
            except Exception as e:
                logging.error(f"Failed to retrieve preferences for user_id {user_id}: {e}")
                return []

    @staticmethod
    def _get_preferences(tx, user_id):
        query = (
            "MATCH (u:User {id: $user_id})-[:HAS_PREFERENCE]->(p:Preference) "
            "RETURN p.name AS preference_name"
        )
        return tx.run(query, user_id=user_id)