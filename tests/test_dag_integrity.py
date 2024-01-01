tfrom unittest.mock import patch, MagicMock
from airflow.models import DagBag
from dags.firstdag import capture_api_response


def test_dag_bag():
    dag_bag = DagBag(include_examples=False)
    assert not dag_bag.import_errors


@patch('dags.firstdag.requests')
def test_capture_api_response(mock_requests):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'description': 'test response'}

    mock_requests.get.return_value = mock_response

    assert capture_api_response() is 'test response'
