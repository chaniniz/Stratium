import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from unittest.mock import patch, Mock

import backend.openai_client as oc


def test_generate_weekly_report():
    mock_resp = Mock()
    mock_resp.choices = [Mock(message={"content": "보고서"})]
    with patch('openai.ChatCompletion.create', return_value=mock_resp) as p, \
         patch('openai.api_key', 'key'):
        text = oc.generate_weekly_report('TEST', {'trade_count': 1})
        assert text == '보고서'
        p.assert_called_once()
