import unittest
import sys
import os
import logging
from unittest.mock import patch, MagicMock

# Adjust sys.path to allow importing from the core package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.two_phase_commit import (
    Coordinator,
    Participant,
    ParticipantState,
    TransactionMessage
)

# Disable logging output during tests to keep console clean, unless needed for debugging
logging.getLogger().setLevel(logging.CRITICAL)

class TestTwoPhaseCommit(unittest.TestCase):
    """
    Unit test suite for the Two-Phase Commit (2PC) implementation.
    Tests cover happy paths (all commit), failure paths (a node aborts), 
    and verifies state transitions of participants.
    """

    def setUp(self):
        """
        Set up a fresh coordinator and a set of clean participants for each test.
        """
        self.coordinator = Coordinator("Test-Coordinator-1")
        self.tx_id = "TX-Test-01"
        self.payload = {"action": "test_update", "value": 42}

    def test_participant_initial_state(self):
        """
        Verify that a participant initializes correctly.
        """
        p = Participant("Node-A")
        self.assertEqual(p.participant_id, "Node-A")
        self.assertEqual(p.state, ParticipantState.INIT)
        self.assertIsNone(p.current_tx_id)
        self.assertEqual(p.simulate_failure_rate, 0.0)

    def test_participant_receive_prepare_success(self):
        """
        Verify that a reliable participant correctly votes VOTE_COMMIT upon receiving PREPARE.
        """
        p = Participant("Node-A", simulate_failure_rate=0.0)
        msg = TransactionMessage(self.tx_id, self.coordinator.coordinator_id, "PREPARE", self.payload)
        
        reply = p.receive_prepare(msg)
        
        self.assertEqual(reply.action, "VOTE_COMMIT")
        self.assertEqual(reply.sender_id, "Node-A")
        self.assertEqual(reply.tx_id, self.tx_id)
        self.assertEqual(p.state, ParticipantState.READY)
        self.assertEqual(p.current_tx_id, self.tx_id)

    def test_participant_receive_prepare_failure(self):
        """
        Verify that a failing participant correctly votes VOTE_ABORT upon receiving PREPARE.
        """
        p = Participant("Node-A", simulate_failure_rate=1.0) # 100% failure rate
        msg = TransactionMessage(self.tx_id, self.coordinator.coordinator_id, "PREPARE", self.payload)
        
        reply = p.receive_prepare(msg)
        
        self.assertEqual(reply.action, "VOTE_ABORT")
        self.assertEqual(reply.sender_id, "Node-A")
        self.assertEqual(reply.tx_id, self.tx_id)
        self.assertEqual(p.state, ParticipantState.ABORTED)
        self.assertEqual(p.current_tx_id, self.tx_id)

    def test_participant_receive_global_commit(self):
        """
        Verify that a participant in READY state commits upon receiving GLOBAL_COMMIT.
        """
        p = Participant("Node-A")
        p.state = ParticipantState.READY
        p.current_tx_id = self.tx_id

        msg = TransactionMessage(self.tx_id, self.coordinator.coordinator_id, "GLOBAL_COMMIT")
        p.receive_decision(msg)

        self.assertEqual(p.state, ParticipantState.COMMITTED)
        self.assertIsNone(p.current_tx_id)

    def test_participant_receive_global_abort(self):
        """
        Verify that a participant aborts upon receiving GLOBAL_ABORT.
        """
        p = Participant("Node-A")
        p.state = ParticipantState.READY
        p.current_tx_id = self.tx_id

        msg = TransactionMessage(self.tx_id, self.coordinator.coordinator_id, "GLOBAL_ABORT")
        p.receive_decision(msg)

        self.assertEqual(p.state, ParticipantState.ABORTED)
        self.assertIsNone(p.current_tx_id)

    def test_coordinator_no_participants(self):
        """
        Verify that the coordinator rejects a transaction if there are no participants.
        """
        result = self.coordinator.execute_transaction(self.tx_id, self.payload)
        self.assertFalse(result)

    def test_global_commit_all_reliable_participants(self):
        """
        Integration test: Verify that if all participants are reliable (0% failure rate), 
        the global transaction successfully commits.
        """
        p1 = Participant("DB-1", simulate_failure_rate=0.0)
        p2 = Participant("DB-2", simulate_failure_rate=0.0)
        p3 = Participant("DB-3", simulate_failure_rate=0.0)

        self.coordinator.register_participant(p1)
        self.coordinator.register_participant(p2)
        self.coordinator.register_participant(p3)

        result = self.coordinator.execute_transaction(self.tx_id, self.payload)

        self.assertTrue(result)
        self.assertEqual(p1.state, ParticipantState.COMMITTED)
        self.assertEqual(p2.state, ParticipantState.COMMITTED)
        self.assertEqual(p3.state, ParticipantState.COMMITTED)

    def test_global_abort_one_failing_participant(self):
        """
        Integration test: Verify that if at least one participant fails (votes abort), 
        the global transaction aborts for EVERYONE.
        """
        p1 = Participant("DB-1", simulate_failure_rate=0.0)
        p2 = Participant("DB-2", simulate_failure_rate=1.0) # This one will definitely fail Phase 1
        p3 = Participant("DB-3", simulate_failure_rate=0.0)

        self.coordinator.register_participant(p1)
        self.coordinator.register_participant(p2)
        self.coordinator.register_participant(p3)

        result = self.coordinator.execute_transaction(self.tx_id, self.payload)

        self.assertFalse(result)
        # All participants should end up in the ABORTED state, even if they initially voted COMMIT
        self.assertEqual(p1.state, ParticipantState.ABORTED)
        self.assertEqual(p2.state, ParticipantState.ABORTED)
        self.assertEqual(p3.state, ParticipantState.ABORTED)

    def test_coordinator_handles_participant_exception_in_prepare(self):
        """
        Verify that if a participant throws an unhandled exception during Phase 1, 
        the coordinator catches it and safely aborts the global transaction.
        """
        p1 = Participant("DB-1", simulate_failure_rate=0.0)
        p2 = Participant("DB-2", simulate_failure_rate=0.0)
        
        # Mock instance method for p1 to throw exception
        p1.receive_prepare = MagicMock(side_effect=Exception("Network timeout"))

        self.coordinator.register_participant(p1)
        self.coordinator.register_participant(p2)

        result = self.coordinator.execute_transaction(self.tx_id, self.payload)

        self.assertFalse(result)
        # DB-2 dynamically voted commit in reality, but then received GLOBAL_ABORT because DB-1 threw exception
        self.assertEqual(p2.state, ParticipantState.ABORTED)

    @patch('core.two_phase_commit.Participant.receive_decision')
    def test_coordinator_handles_participant_exception_in_decision(self, mock_receive_decision):
        """
        Verify that if a participant throws an exception during Phase 2 (receiving the decision),
        it doesn't crash the coordinator, though other nodes still commit.
        """
        p1 = Participant("DB-1", simulate_failure_rate=0.0)
        p2 = Participant("DB-2", simulate_failure_rate=0.0)
        
        self.coordinator.register_participant(p1)
        self.coordinator.register_participant(p2)

        # Make the mock throw an exception during receive_decision to simulate a crash/timeout
        # Note: In a real system the DB-1 state might be unknown, but the Coordinator method should return True
        mock_receive_decision.side_effect = Exception("Failed to receive commit message")

        result = self.coordinator.execute_transaction(self.tx_id, self.payload)

        # The global transaction decision was COMMIT. 
        # Even if nodes threw exceptions receiving the decision, the coordinator executed Phase 2.
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
