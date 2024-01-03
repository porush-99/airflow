import unittest
from unittest.mock import patch, MagicMock
from airflow.models import DagBag
from dags.firstdag import capture_api_response


class TestAirflowDag(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dag_bag = DagBag(include_examples=False)

    def test_dag_bag(self):
        # dag_bag = DagBag(include_examples=False)
        dag = self.dag_bag.get_dag(dag_id='first_dag')
        assert self.dag_bag.import_errors == {}
        assert dag is not None

    @staticmethod
    def AssertDagDictEqual(source, dag):
        print('source keys')
        print(source)
        print(list(dag.task_dict.keys()))
        assert list(dag.task_dict.keys()) == source

    def test_dag(self):
        self.AssertDagDictEqual([
            "start",
            "capture_response",
            "end"
        ], self.dag_bag.get_dag(dag_id='first_dag'))

    @patch('dags.firstdag.requests')
    def test_capture_api_response(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'description': 'test response'}

        mock_requests.get.return_value = mock_response

        self.assertEqual(capture_api_response(), 'test response')

        mock_response.status_code = 404
        mock_requests.get.return_value = mock_response

        self.assertEqual(capture_api_response(), 'no response')
