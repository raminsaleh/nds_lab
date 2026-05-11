import pytest
from nds_core.enums import SequenceState
from nds_core.sequence_engine import NDSSequenceEngine
from nds_core.sequence_state import NDSSequenceContext

def test_full_canonical_sequence_reaches_cycle_complete():
    context=NDSSequenceContext(cycle_id="CYCLE_0001"); engine=NDSSequenceEngine(context)
    for node in ["Z","N1","S1","N2","S2","N3","S3"]:
        result=engine.submit_node(node); assert result.accepted, result.message
    assert context.current_state == SequenceState.CYCLE_COMPLETE
    assert context.confirmed_nodes == ["Z","N1","S1","N2","S2","N3","S3"]

def test_invalid_sequence_jump_is_rejected():
    context=NDSSequenceContext(cycle_id="CYCLE_0001"); engine=NDSSequenceEngine(context)
    result=engine.submit_node("N1")
    assert not result.accepted
    assert context.current_state == SequenceState.WAIT_Z
    assert context.confirmed_nodes == []

def test_cycle_is_not_complete_at_n3():
    context=NDSSequenceContext(cycle_id="CYCLE_0001"); engine=NDSSequenceEngine(context)
    for node in ["Z","N1","S1","N2","S2","N3"]:
        result=engine.submit_node(node); assert result.accepted, result.message
    assert context.current_state == SequenceState.WAIT_S3
    assert context.current_state != SequenceState.CYCLE_COMPLETE

def test_next_cycle_requires_cycle_complete():
    context=NDSSequenceContext(cycle_id="CYCLE_0001"); engine=NDSSequenceEngine(context)
    with pytest.raises(ValueError): engine.reset_for_next_cycle("CYCLE_0002")
