import unittest
import sys
import os
import logging
from unittest.mock import MagicMock

# Adjust sys.path to allow importing from the core package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.three_phase_commit import (
    Coordinator,
    Participant,
    ParticipantState,
    MessageType,
    TransactionMessage
)

# Disable logging output during tests to keep console clean, unless needed for debugging
logging.getLogger().setLevel(logging.CRITICAL)

class TestThreePhaseCommit(unittest.TestCase):
    """
    Unit test suite for the Three-Phase Commit (3PC) implementation.
    """

    def setUp(self):
        """
        Set up a fresh coordinator and a set of clean participants for each test.
        """
        self.coordinator = Coordinator("Test-Coord-1")
        self.tx_id = "TX-Test"
        self.payload = {"operation": "insert", "key": "k1", "value": "v1"}

    def test_participant_initial_state(self):
        """
        Verify participant initializes correctly.
        """
        p = Participant("Node-A")
        self.assertEqual(p.participant_id, "Node-A")
        self.assertEqual(p.state, ParticipantState.INIT)
        self.assertIsNone(p.current_tx_id)

    def test_participant_receive_can_commit_success(self):
        """
        Verify participant correctly votes VOTE_YES upon receiving CAN_COMMIT.
        """
        p = Participant("Node-A", failure_rate_p1=0.0)
        msg = TransactionMessage(self.tx_id, self.coordinator.coordinator_id, MessageType.CAN_COMMIT, self.payload)
        
        reply = p.receive_can_commit(msg)
        
        self.assertEqual(reply.msg_type, MessageType.VOTE_YES)
        self.assertEqual(p.state, ParticipantState.READY)
        self.assertEqual(p.current_tx_id, self.tx_id)

    def test_participant_receive_can_commit_failure(self):
        """
        Verify failing participant votes VOTE_NO.
        """
        p = Participant("Node-A", failure_rate_p1=1.0)
        msg = TransactionMessage(self.tx_id, self.coordinator.coordinator_id, MessageType.CAN_COMMIT, self.payload)
        
        reply = p.receive_can_commit(msg)
        
        self.assertEqual(reply.msg_type, MessageType.VOTE_NO)
        self.assertEqual(p.state, ParticipantState.ABORTED)

    def test_participant_receive_pre_commit(self):
        """
        Verify participant transitions to PRECOMMIT and ACKs.
        """
        p = Participant("Node-A")
        p.state = ParticipantState.READY
        p.current_tx_id = self.tx_id

        msg = TransactionMessage(self.tx_id, self.coordinator.coordinator_id, MessageType.PRE_COMMIT)
        reply = p.receive_pre_commit(msg)

        self.assertEqual(reply.msg_type, MessageType.ACK)
        self.assertEqual(p.state, ParticipantState.PRECOMMIT)

    def test_participant_invalid_pre_commit_state(self):
        """
        Verify participant rejects PRE_COMMIT if not in READY state.
        """
        p = Participant("Node-A")
        p.state = ParticipantState.INIT
        p.current_tx_id = self.tx_id

        msg = TransactionMessage(self.tx_id, self.coordinator.coordinator_id, MessageType.PRE_COMMIT)
        
        with self.assertRaises(RuntimeError):
            p.receive_pre_commit(msg)

    def test_participant_receive_do_commit(self):
        """
        Verify participant transitions from PRECOMMIT to COMMITTED.
        """
        p = Participant("Node-A")
        p.state = ParticipantState.PRECOMMIT
        p.current_tx_id = self.tx_id

        msg = TransactionMessage(self.tx_id, self.coordinator.coordinator_id, MessageType.DO_COMMIT)
        p.receive_decision(msg)

        self.assertEqual(p.state, ParticipantState.COMMITTED)
        self.assertIsNone(p.current_tx_id)

    def test_global_commit_all_reliable_participants(self):
        """
        Integration test: Verify healthy 3PC transaction.
        """
        p1 = Participant("DB-1", failure_rate_p1=0.0, failure_rate_p2=0.0)
        p2 = Participant("DB-2", failure_rate_p1=0.0, failure_rate_p2=0.0)

        self.coordinator.register_participant(p1)
        self.coordinator.register_participant(p2)

        result = self.coordinator.execute_transaction(self.tx_id, self.payload)

        self.assertTrue(result)
        self.assertEqual(p1.state, ParticipantState.COMMITTED)
        self.assertEqual(p2.state, ParticipantState.COMMITTED)

    def test_global_abort_phase1_failure(self):
        """
        Integration test: Verify abort if a participant votes NO.
        """
        p1 = Participant("DB-1", failure_rate_p1=0.0)
        p2 = Participant("DB-2", failure_rate_p1=1.0) # Always votes NO

        self.coordinator.register_participant(p1)
        self.coordinator.register_participant(p2)

        result = self.coordinator.execute_transaction(self.tx_id, self.payload)

        self.assertFalse(result)
        # Even though p1 voted YES (and entered READY), it should receive the ABORT broadcast
        self.assertEqual(p1.state, ParticipantState.ABORTED)
        self.assertEqual(p2.state, ParticipantState.ABORTED)

    def test_global_abort_phase2_timeout(self):
        """
        Integration test: Verify abort if a participant times out during Phase 2 (PRE_COMMIT).
        """
        p1 = Participant("DB-1", failure_rate_p1=0.0, failure_rate_p2=0.0)
        p2 = Participant("DB-2", failure_rate_p1=0.0, failure_rate_p2=1.0) # Fails Phase 2 (Timeout)

        self.coordinator.register_participant(p1)
        self.coordinator.register_participant(p2)

        result = self.coordinator.execute_transaction(self.tx_id, self.payload)

        self.assertFalse(result)
        # p1 entered PRECOMMIT, p2 crashed/timed out. Coordinator decides ABORT.
        # Both p1 and p2 receive ABORT and roll back.
        self.assertEqual(p1.state, ParticipantState.ABORTED)
        self.assertEqual(p2.state, ParticipantState.ABORTED)

    def test_coordinator_handles_participant_exception_in_phase1(self):
        """
        Verify exception handling during CAN_COMMIT phase.
        """
        p1 = Participant("DB-1")
        p2 = Participant("DB-2")
        
        # Mock instance method to simulate network error
        p1.receive_can_commit = MagicMock(side_effect=Exception("Network partition"))

        self.coordinator.register_participant(p1)
        self.coordinator.register_participant(p2)

        result = self.coordinator.execute_transaction(self.tx_id, self.payload)

        self.assertFalse(result)
        # p2 voted YES dynamically, but received ABORT because p1 failed
        self.assertEqual(p2.state, ParticipantState.ABORTED)

    def test_coordinator_handles_participant_exception_in_phase3(self):
        """
        Verify that exception during DO_COMMIT doesn't immediately crash coordinator,
        though final transaction state is considered TRUE because decision was written.
        """
        p1 = Participant("DB-1")
        
        # Mock instance method for phase 3
        p1.receive_decision = MagicMock(side_effect=Exception("Disk full on commit"))

        self.coordinator.register_participant(p1)
        result = self.coordinator.execute_transaction(self.tx_id, self.payload)

        # Coordinator decided global COMMIT. Node failing to apply is a node-level recovery issue.
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
