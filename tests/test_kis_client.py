import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from unittest.mock import patch, Mock
import os

import importlib
import backend.kis_client as kis


def test_get_access_token():
    mock_response = Mock()
    mock_response.json.return_value = {"access_token": "TOKEN"}
    mock_response.raise_for_status = lambda: None
    with patch.dict(os.environ, {"KIS_APP_KEY": "k", "KIS_APP_SECRET": "s"}):
        importlib.reload(kis)
        with patch('requests.post', return_value=mock_response) as p:
            token = kis.get_access_token()
            assert token == "TOKEN"
            p.assert_called_once()
