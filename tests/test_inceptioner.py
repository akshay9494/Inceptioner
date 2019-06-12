from core.inceptioner import Inceptioner
import pytest


def test_inceptioner():
    sut = Inceptioner()
    res = sut.predict(img_path='dog.jpg')
    assert res['prediction'] == 'golden_retriever'
    assert res['confidence'] == pytest.approx(0.65, 0.1)