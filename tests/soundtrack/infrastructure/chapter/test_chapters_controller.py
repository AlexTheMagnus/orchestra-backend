import json
import uuid
from faker import Faker

from orchestra import app
from ...builder.soundtrack_builder import SoundtrackBuilder
from src.soundtrack.infrastructure.soundtrack_mysql_repository import SoundtrackMysqlRepository
from src.soundtrack.infrastructure.chapter.chapter_mysql_repository import ChapterMysqlRepository
from src.soundtrack.domain.chapter.chapter_id import ChapterId
from ...builder.chapter_builder import ChapterBuilder

fake = Faker()
chapter_repository = ChapterMysqlRepository()
soundtrack_repository = SoundtrackMysqlRepository()

def teardown_module():
    ChapterMysqlRepository().clean()

class TestChaptersPostController():
    def test_should_add_a_new_chapter_with_the_passed_parameters(self):
        soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)

        chapter_id = ChapterId.from_string(str(uuid.uuid4()))
        chapters_post_request_params = get_chapters_post_request_params_with_ids(
            chapter_id.value, soundtrack.soundtrack_id.value)

        response = app.test_client().post(
            '/chapters',
            data=json.dumps(chapters_post_request_params),
            content_type='application/json'
        )
        
        saved_chapter = chapter_repository.find(chapter_id)
        assert response.status_code == 200
        assert saved_chapter != None
        assert saved_chapter.chapter_id.value == chapters_post_request_params["chapter_id"]
        assert saved_chapter.soundtrack_id.value == chapters_post_request_params["soundtrack_id"]
        assert saved_chapter.chapter_number.value == chapters_post_request_params["chapter_number"]
        assert saved_chapter.theme.value == chapters_post_request_params["theme"]
        assert saved_chapter.chapter_title.value == chapters_post_request_params["chapter_title"]

    def test_should_return_409_when_adding_a_chapter_with_an_already_registered_chapter_id(self):
        soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)
        chapter = ChapterBuilder().with_soundtrack_id(soundtrack.soundtrack_id).build()
        chapter_repository.save(chapter)

        chapters_post_request_params = get_chapters_post_request_params_with_ids(
            chapter.chapter_id.value, chapter.soundtrack_id.value)

        response = app.test_client().post(
            '/chapters',
            data=json.dumps(chapters_post_request_params),
            content_type='application/json'
        )
        
        assert response.status_code == 409

    def test_should_return_404_when_adding_a_chapter_to_an_unexisting_soundtrack(self):
        chapter = ChapterBuilder().build()

        chapters_post_request_params = get_chapters_post_request_params_with_ids(
            chapter.chapter_id.value, chapter.soundtrack_id.value)

        response = app.test_client().post(
            '/chapters',
            data=json.dumps(chapters_post_request_params),
            content_type='application/json'
        )
        
        assert response.status_code == 404

def get_chapters_post_request_params_with_ids(chapter_id: str, soundtrack_id: str):
    return {
        "chapter_id": chapter_id,
        "soundtrack_id": soundtrack_id,
        "chapter_number": 2,
        "theme": fake.pystr(),
        "chapter_title": fake.pystr()
    }


class TestChaptersGetController():
    def test_should_return_the_soundtrack_chapters(self):
        soundtrack: Soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)

        for x in range(2):
            chapter: Chapter = ChapterBuilder().with_soundtrack_id(soundtrack.soundtrack_id).build()
            chapter_repository.save(chapter)

        response = app.test_client().get(
            '/chapters/soundtrack/{0}'.format(soundtrack.soundtrack_id.value),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert len(data["chapters_list"]) == 2