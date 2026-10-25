from app.curriculum.videos import get_lesson_video


def test_first_mapped_video_is_verified_install_and_setup():
    video = get_lesson_video("py-v2-u1-l02")
    assert video.video_id == "YYXdXT2l-Gg"
    assert "Install and Setup" in video.title
    assert video.instructor == "Corey Schafer"
    assert video.verification_status.startswith("oEmbed verified")


def test_lesson1_mapped_video_is_bro_code():
    video = get_lesson_video("py-v2-u1-l01")
    assert video.video_id == "Sg4GMVMdOPo"
    assert "Start coding with PYTHON" in video.title
    assert video.instructor == "Bro Code"


def test_unmatched_lesson_has_no_fabricated_video():
    assert get_lesson_video("not-a-lesson") is None
