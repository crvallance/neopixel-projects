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
    pattern_instance.write(pixel_location=0, color=(0, 0, 0))
    f = open(generic_file, "r")
    lines = f.readlines()
    assert lines == ['0 0 0 0\n']


def test_pattern_commit(generic_file, pattern_instance):
    pattern_instance.commit()
    f = open(generic_file, "r")
    lines = f.readlines()
    assert lines == ['-1 0 0 0\n']


@pytest.mark.parametrize(
    'push_param',
    (True, False)
)
def test_pattern_paint_all_windows(generic_file, push_param):
    pattern = pixel_worker.Pattern(pru=generic_file, pixel_count=2, push=push_param)
    pattern.paint_all_windows(color=(0, 0, 0))
    f = open(generic_file, "r")
    lines = f.readlines()
    if push_param:
        assert lines == ['0 0 0 0\n', '-1 0 0 0\n', '1 0 0 0\n', '-1 0 0 0\n', '-1 0 0 0\n']
    else:
        assert lines == ['0 0 0 0\n', '1 0 0 0\n', '-1 0 0 0\n']


def test_strobe(generic_file):
    # mypattern = pixel_worker.Pattern()
    strobe = pixel_worker.Strobe().with_pru(generic_file)
    strobe.run(color=(0, 0, 0))
    f = open(generic_file, "r")
    lines = f.readlines()

# class Strobe(Pattern):
#     def __init__(self, color: tuple = (255, 255, 255)):
#         self.__color = color
#         super().__init__()

#     def run(self, color):
#         self.paint_all_windows(Colors.off)
#         self.paint_all_windows(self.__color)
#         self.paint_all_windows(Colors.off)
#         self.paint_all_windows(self.__color)
#         self.paint_all_windows(Colors.off)

#     def loop(self, color: tuple = (255, 255, 255), loop_count: int = 20, wait: int = 0):
#         for loop in range(0, loop_count):
#             self.run(color)
#             time.sleep(wait)
