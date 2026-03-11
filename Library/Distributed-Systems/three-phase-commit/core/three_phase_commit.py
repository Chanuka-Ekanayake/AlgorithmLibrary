import logging
import random
import time
from enum import Enum
from typing import List, Optional, Any

# Configure logging for the Three-Phase Commit module
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

class ParticipantState(Enum):
    """
    Represents the various states a Participant can be in during a Three-Phase Commit transaction.
    """
    INIT = "INIT"             # Initial state
    WAIT_VOTE = "WAIT_VOTE"   # Waiting to send vote
    READY = "READY"           # Voted YES, waiting for PRE_COMMIT
    PRECOMMIT = "PRECOMMIT"   # Received PRE_COMMIT, meaning coordinator intends to commit
    ABORTED = "ABORTED"       # Final State: changes rolled back
    COMMITTED = "COMMITTED"   # Final State: changes applied

class MessageType(Enum):
    """
    Message types exchanged between Coordinator and Participants.
    """
    CAN_COMMIT = "CAN_COMMIT"         # Coordinator asks if participants can commit (Phase 1)
    VOTE_YES = "VOTE_YES"             # Participant votes YES
    VOTE_NO = "VOTE_NO"               # Participant votes NO
    PRE_COMMIT = "PRE_COMMIT"         # Coordinator tells participants it intends to commit (Phase 2)
    ACK = "ACK"                       # Participant acknowledges PRE_COMMIT or DO_COMMIT
    DO_COMMIT = "DO_COMMIT"           # Coordinator commands to commit (Phase 3)
    ABORT = "ABORT"                   # Coordinator commands to abort

class TransactionMessage:
    """
    Represents a payload exchanged in the 3PC protocol.
    """
    def __init__(self, tx_id: str, sender_id: str, msg_type: MessageType, payload: Optional[Any] = None):
        self.tx_id = tx_id
        self.sender_id = sender_id
        self.msg_type = msg_type
        self.payload = payload

    def __str__(self):
        return f"Message(tx={self.tx_id}, sender={self.sender_id}, type={self.msg_type.value})"

class Participant:
    """
    A resource manager participating in the distributed transaction.
    """
    def __init__(self, participant_id: str, failure_rate_p1: float = 0.0, failure_rate_p2: float = 0.0):
        """
        :param participant_id: ID for the Node
        :param failure_rate_p1: Probability to fail (vote NO) during Phase 1
        :param failure_rate_p2: Probability to timeout/fail during Phase 2
        """
        self.participant_id = participant_id
        self.state = ParticipantState.INIT
        self.failure_rate_p1 = failure_rate_p1
        self.failure_rate_p2 = failure_rate_p2
        self.logger = logging.getLogger(f"Participant-{self.participant_id}")
        self.current_tx_id = None

    def receive_can_commit(self, message: TransactionMessage) -> TransactionMessage:
        """
        Phase 1: Voting Phase. Evaluates if the local transaction is possible.
        """
        self.logger.info(f"Received {message.msg_type.value} for TX: {message.tx_id}")
        self.current_tx_id = message.tx_id
        self.state = ParticipantState.WAIT_VOTE

        time.sleep(random.uniform(0.05, 0.15))

        if random.random() < self.failure_rate_p1:
            self.logger.warning(f"Local condition failed. Voting NO for TX: {self.current_tx_id}")
            self.state = ParticipantState.ABORTED
            return TransactionMessage(self.current_tx_id, self.participant_id, MessageType.VOTE_NO)
        else:
            self.logger.info(f"Local checks passed. Voting YES for TX: {self.current_tx_id}")
            self.state = ParticipantState.READY
            return TransactionMessage(self.current_tx_id, self.participant_id, MessageType.VOTE_YES)

    def receive_pre_commit(self, message: TransactionMessage) -> TransactionMessage:
        """
        Phase 2: Preparation Phase. The participant prepares to commit.
        """
        self.logger.info(f"Received {message.msg_type.value} for TX: {message.tx_id}")
        if self.state != ParticipantState.READY:
            self.logger.error(f"Cannot process PRE_COMMIT. Current state is {self.state.value}")
            raise RuntimeError(f"Participant {self.participant_id} in invalid state {self.state.value}")

        if random.random() < self.failure_rate_p2:
            self.logger.error(f"Node crashed simulating network timeout before sending ACK for PRE_COMMIT")
            raise ConnectionError("Network Timeout")

        self.state = ParticipantState.PRECOMMIT
        self.logger.info(f"Entered PRECOMMIT state. Sending ACK.")
        return TransactionMessage(self.current_tx_id, self.participant_id, MessageType.ACK)

    def receive_decision(self, message: TransactionMessage):
        """
        Phase 3: Execution Phase. Final decision to either commit or abort.
        """
        self.logger.info(f"Received decision {message.msg_type.value} for TX: {message.tx_id}")

        if message.msg_type == MessageType.DO_COMMIT:
            if self.state == ParticipantState.PRECOMMIT:
                self.logger.info(f"Executing DO_COMMIT locally. Applying changes.")
                self.state = ParticipantState.COMMITTED
            else:
                self.logger.error(f"Cannot DO_COMMIT from state {self.state.value}")
        elif message.msg_type == MessageType.ABORT:
            self.logger.info(f"Executing ABORT locally. Rolling back changes.")
            self.state = ParticipantState.ABORTED

        self.current_tx_id = None

class Coordinator:
    """
    The Transaction Coordinator orchestrating the Three-Phase Commit protocol.
    """
    def __init__(self, coordinator_id: str):
        self.coordinator_id = coordinator_id
        self.participants: List[Participant] = []
        self.logger = logging.getLogger(f"Coordinator-{self.coordinator_id}")

    def register_participant(self, participant: Participant):
        self.participants.append(participant)
        self.logger.info(f"Registered Participant: {participant.participant_id}")

    def execute_transaction(self, tx_id: str, payload: Any) -> bool:
        """
        Execute 3PC protocol: CanCommit -> PreCommit -> DoCommit.
        """
        if not self.participants:
            self.logger.error("No participants available to conduct transaction.")
            return False

        self.logger.info(f"=== Starting 3PC Transaction {tx_id} ===")

        # === PHASE 1: CAN COMMIT (VOTING) ===
        self.logger.info(">>> PHASE 1: CAN COMMIT")
        can_commit_msg = TransactionMessage(tx_id, self.coordinator_id, MessageType.CAN_COMMIT, payload)
        
        all_voted_yes = True
        for p in self.participants:
            try:
                reply = p.receive_can_commit(can_commit_msg)
                if reply.msg_type != MessageType.VOTE_YES:
                    all_voted_yes = False
            except Exception as e:
                self.logger.error(f"Communication issue with {p.participant_id} during Voting: {e}")
                all_voted_yes = False

        if not all_voted_yes:
            self.logger.warning(f"Aborting at Phase 1. Broadcasting ABORT for TX: {tx_id}")
            self._broadcast_decision(tx_id, MessageType.ABORT)
            return False

        # === PHASE 2: PRE COMMIT ===
        self.logger.info(">>> PHASE 2: PRE COMMIT")
        pre_commit_msg = TransactionMessage(tx_id, self.coordinator_id, MessageType.PRE_COMMIT)
        
        all_acked = True
        for p in self.participants:
            try:
                reply = p.receive_pre_commit(pre_commit_msg)
                if reply.msg_type != MessageType.ACK:
                    all_acked = False
            except Exception as e:
                self.logger.error(f"Timeout/Error communicating with {p.participant_id} during Pre-Commit: {e}")
                all_acked = False

        if not all_acked:
            # Under 3PC rules, if PreCommit fails/times out, we still abort
            self.logger.warning(f"Timeout during Pre-Commit. Broadcasting ABORT for TX: {tx_id}")
            self._broadcast_decision(tx_id, MessageType.ABORT)
            return False

        # === PHASE 3: DO COMMIT ===
        self.logger.info(">>> PHASE 3: DO COMMIT")
        self._broadcast_decision(tx_id, MessageType.DO_COMMIT)
        self.logger.info(f"=== Transaction {tx_id} Completed Successfully ===")
        return True

    def _broadcast_decision(self, tx_id: str, decision: MessageType):
        """
        Helper method to broadcast the coordinator's final decision (COMMIT or ABORT)
        to all participants, regardless of which phase determined that outcome.
        """
        decision_msg = TransactionMessage(tx_id, self.coordinator_id, decision)
        for p in self.participants:
            try:
                p.receive_decision(decision_msg)
            except Exception as e:
                self.logger.error(f"Failed to deliver decision to {p.participant_id}: {e}")

if __name__ == "__main__":
    print("\n--- TEST: Happy Path ---")
    # Using independent instances just for the demo
    clean_p1 = Participant("Node-A")
    clean_p2 = Participant("Node-B")
    clean_coord = Coordinator("Coord-1")
    clean_coord.register_participant(clean_p1)
    clean_coord.register_participant(clean_p2)
    clean_coord.execute_transaction("TX-100", {"data": "commit me"})

    print("\n--- TEST: Phase 1 Failure ---")
    fail_p1 = Participant("Node-Fail-P1", failure_rate_p1=1.0)
    clean_coord.register_participant(fail_p1)
    clean_coord.execute_transaction("TX-101", {"data": "will fail"})
