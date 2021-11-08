import pytest
import pixel_worker


@pytest.fixture(scope="session")
def generic_file(tmp_path_factory):
    file_name = tmp_path_factory.mktemp("data") / "dummyfile"
    return file_name

@pytest.fixture()
def pattern_instance(generic_file):
    pattern = pixel_worker.Pattern(pru=generic_file)
    return pattern

def test_pattern_write(generic_file, pattern_instance):
    # pattern = pixel_worker.Pattern(pru=generic_file)
    # pattern = pattern_instance()
    pattern_instance.write(pixel_location=0, color=(0, 0, 0))
    f = open(generic_file, "r")
    lines = f.readlines()
    assert lines == ['0 0 0 0\n']

def test_pattern_commit(generic_file, pattern_instance):
    # pattern = pixel_worker.Pattern(pru=generic_file)
    pattern_instance.commit()
    f = open(generic_file, "r")
    lines = f.readlines()
    assert lines == ['-1 0 0 0\n']
