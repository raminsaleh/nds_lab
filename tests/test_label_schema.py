from nds_core.label_validation import validate_label_row

def _base_row():
    return {"label_id":"LBL_000001","symbol":"US30","timeframe":"M15","timestamp_start":"2026-01-05 09:00","timestamp_end":"2026-01-05 09:00","price_start":"37650","price_end":"37650","label_type":"Z","direction":"1","cycle_id":"CYCLE_0001","parent_label_id":"","child_label_ids":"","confidence":"PROBABLE","source_validation_status":"SOURCE_COMPATIBLE_INTERPRETATION","related_86_context":"POINT_Z","related_point3_status":"NOT_APPLICABLE","notes":"Initial Z candidate"}

def test_valid_label_row_has_no_errors():
    assert validate_label_row(_base_row(), row_number=2) == []

def test_generic_86_is_rejected():
    row=_base_row(); row["related_86_context"]="GENERIC_86"
    assert any(i.field=="related_86_context" for i in validate_label_row(row,2))

def test_invalid_direction_is_rejected():
    row=_base_row(); row["direction"]="2"
    assert any(i.field=="direction" for i in validate_label_row(row,2))

def test_invalid_label_type_is_rejected():
    row=_base_row(); row["label_type"]="SWING_HIGH"
    assert any(i.field=="label_type" for i in validate_label_row(row,2))
