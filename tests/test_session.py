import pytest
from WordStream import WordStream

from core.BaseClient import BaseClient


@pytest.fixture(name='stream')
def stream_fixture():
    return WordStream(['test 123'])


def test_session(stream):
    stt_client = BaseClient()
    stt_client.set_status('Ready')
    assert stt_client.session.status == 'Ready'

    for transcript in stream.generator():
        print(type(transcript))
        stt_client.update(transcript)

    assert stt_client.session.paragraphs == [['test 123']]
