import logging
import random
import time
from enum import Enum
from typing import List, Dict, Optional, Any

# Configure logging for the Two-Phase Commit module
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

class ParticipantState(Enum):
    """
    Represents the various states a Participant can be in during a distributed transaction.
    """
    INIT = "INIT"
    READY = "READY"
    ABORTED = "ABORTED"
    COMMITTED = "COMMITTED"

class OperationStatus(Enum):
    """
    Represents the status of a local operation for a participant.
    """
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"

class TransactionMessage:
    """
    Represents a message exchanged between the Coordinator and the Participants.
    """
    def __init__(self, tx_id: str, sender_id: str, action: str, payload: Optional[Any] = None):
        """
        Initializes a transaction message.
        
        :param tx_id: The transaction identifier.
        :param sender_id: The ID of the sender.
        :param action: The action or message type (e.g., PREPARE, VOTE_COMMIT, VOTE_ABORT, GLOBAL_COMMIT, GLOBAL_ABORT).
        :param payload: Any operational data related to the message.
        """
        self.tx_id = tx_id
        self.sender_id = sender_id
        self.action = action
        self.payload = payload

    def __str__(self):
        return f"Message(tx={self.tx_id}, sender={self.sender_id}, action={self.action})"

class Participant:
    """
    Represents a resource manager or node participating in the distributed transaction.
    """
    def __init__(self, participant_id: str, simulate_failure_rate: float = 0.0):
        """
        Initializes the participant.
        
        :param participant_id: Unique identifier for the participant.
        :param simulate_failure_rate: Probability (0.0 to 1.0) that the participant simulates a failure during the prepare phase.
        """
        self.participant_id = participant_id
        self.state = ParticipantState.INIT
        self.simulate_failure_rate = simulate_failure_rate
        self.logger = logging.getLogger(f"Participant-{self.participant_id}")
        self.current_tx_id = None

    def receive_prepare(self, message: TransactionMessage) -> TransactionMessage:
        """
        Phase 1: Receive a PREPARE message from the coordinator.
        The participant evaluates if it can commit the transaction.
        """
        self.logger.info(f"Received {message.action} for TX: {message.tx_id}")
        self.current_tx_id = message.tx_id
        
        # Simulate local evaluation of the transaction
        time.sleep(random.uniform(0.1, 0.3))
        
        # Decide whether to vote commit or abort based on failure rate
        if random.random() < self.simulate_failure_rate:
            self.logger.warning(f"Simulating local failure during prepare phase for TX: {self.current_tx_id}")
            self.state = ParticipantState.ABORTED
            return TransactionMessage(self.current_tx_id, self.participant_id, "VOTE_ABORT")
        else:
            self.logger.info(f"Local operations successful. Voting COMMIT for TX: {self.current_tx_id}")
            self.state = ParticipantState.READY
            return TransactionMessage(self.current_tx_id, self.participant_id, "VOTE_COMMIT")

    def receive_decision(self, message: TransactionMessage):
        """
        Phase 2: Receive the final global decision (COMMIT or ABORT) from the coordinator.
        """
        self.logger.info(f"Received global decision {message.action} for TX: {message.tx_id}")
        if self.current_tx_id != message.tx_id:
            self.logger.error("Decision received for unknown or mismatched transaction.")
            return

        if message.action == "GLOBAL_COMMIT":
            if self.state == ParticipantState.READY:
                self.logger.info(f"Committing transaction {self.current_tx_id} locally.")
                self.state = ParticipantState.COMMITTED
            else:
                self.logger.error(f"Cannot commit. Current state is {self.state}")
        elif message.action == "GLOBAL_ABORT":
            self.logger.info(f"Aborting transaction {self.current_tx_id} locally.")
            self.state = ParticipantState.ABORTED
        else:
            self.logger.warning(f"Unknown decision action received: {message.action}")

        # Reset current tx id after resolution (in a real system, we'd persist state before this)
        self.current_tx_id = None

class Coordinator:
    """
    Represents the Transaction Coordinator responsible for driving the 2PC protocol.
    """
    def __init__(self, coordinator_id: str):
        """
        Initializes the coordinator node.
        
        :param coordinator_id: Unique identifier for the coordinator.
        """
        self.coordinator_id = coordinator_id
        self.participants: List[Participant] = []
        self.logger = logging.getLogger(f"Coordinator-{self.coordinator_id}")

    def register_participant(self, participant: Participant):
        """
        Registers a participant node for distributed transactions.
        """
        self.participants.append(participant)
        self.logger.info(f"Registered Participant: {participant.participant_id}")

    def execute_transaction(self, tx_id: str, payload: Any) -> bool:
        """
        Executes a distributed transaction across all registered participants using 2PC.
        
        :param tx_id: Unique transaction identifier.
        :param payload: Transaction payload/data.
        :return: True if the transaction successfully committed globally, False otherwise.
        """
        if not self.participants:
            self.logger.error("No participants registered. Cannot execute transaction.")
            return False

        self.logger.info(f"--- Starting Transaction {tx_id} ---")
        
        # === PHASE 1: PREPARE ===
        self.logger.info("--- PHASE 1: PREPARE ---")
        prepare_msg = TransactionMessage(tx_id, self.coordinator_id, "PREPARE", payload)
        
        votes = []
        all_ready = True
        
        for participant in self.participants:
            # In a real distributed system, this would be an async network call
            try:
                reply = participant.receive_prepare(prepare_msg)
                self.logger.info(f"Received {reply.action} from {reply.sender_id}")
                votes.append(reply)
                if reply.action != "VOTE_COMMIT":
                    all_ready = False
            except Exception as e:
                self.logger.error(f"Communication error with {participant.participant_id}: {e}")
                all_ready = False

        # === PHASE 2: COMMIT / ABORT ===
        self.logger.info("--- PHASE 2: RESOLUTION ---")
        if all_ready:
            self.logger.info(f"All participants voted COMMIT. Proceeding with GLOBAL_COMMIT for TX: {tx_id}")
            decision_msg = TransactionMessage(tx_id, self.coordinator_id, "GLOBAL_COMMIT")
            final_status = True
        else:
            self.logger.warning(f"One or more participants failed/aborted. Proceeding with GLOBAL_ABORT for TX: {tx_id}")
            decision_msg = TransactionMessage(tx_id, self.coordinator_id, "GLOBAL_ABORT")
            final_status = False

        # Broadcast decision to all participants
        for participant in self.participants:
            # In an actual system, we must ensure delivery of this message, even if retries are required
            try:
                participant.receive_decision(decision_msg)
            except Exception as e:
                self.logger.error(f"Failed to send decision to {participant.participant_id}: {e}")

        self.logger.info(f"--- Transaction {tx_id} Complete. Status: {'COMMITTED' if final_status else 'ABORTED'} ---")
        return final_status

if __name__ == "__main__":
    # Example usage of the Two-Phase Commit algorithm
    coordinator = Coordinator("Coord-1")
    
    # Adding participants. One of them is a reliable node, the other has a 20% chance to fail local eval.
    p1 = Participant("Database-Node-A", simulate_failure_rate=0.0)
    p2 = Participant("Database-Node-B", simulate_failure_rate=0.2)
    p3 = Participant("Message-Queue-Node", simulate_failure_rate=0.0)

    coordinator.register_participant(p1)
    coordinator.register_participant(p2)
    coordinator.register_participant(p3)

    # Execute a transaction
    tx1_success = coordinator.execute_transaction("TX-1001", {"action": "deduct_balance", "amount": 50})
    print(f"Transaction 1001 success: {tx1_success}\n")

    # Execute another transaction
    tx2_success = coordinator.execute_transaction("TX-1002", {"action": "add_inventory", "item": "widget", "qty": 10})
    print(f"Transaction 1002 success: {tx2_success}")
