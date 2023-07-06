"""Test Session object"""
import pytest

from src.core.BaseClient import BaseClient
from tests.WordStream import WordStream


@pytest.fixture(name='stream')
def stream_fixture():
    """Generate a basic stream of words"""
    return WordStream(['test 123'])


def test_session(stream):
    """Tests session object works with stream"""
    stt_client = BaseClient()
    stt_client.set_status('Ready')
    assert stt_client.session.status == 'Ready'

    for transcript in stream.generator():
        print(type(transcript))
        stt_client.update(transcript)

    assert stt_client.session.paragraphs == [['test 123']]
