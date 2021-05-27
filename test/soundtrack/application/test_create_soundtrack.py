
class TestCreateSoundtrack():

    def test_new_soundtrack_is_created(self):
        user_dto: UserDTO = UserBuilder().with_user_id(
            user_id).with_email(user_email).build_dto()

        use_case.run(user_dto)

        found_user = user_repository.find(user_id)
        assert found_user != None
        assert found_user.user_id.value == user_id.value
        assert found_user.email == user_email

    def test_already_existing_soundtrack_throws_an_error(self):
        user_dto: UserDTO = UserBuilder().with_user_id(
            user_id).with_email(user_email).build_dto()

        with pytest.raises(AlreadyExistingUserError):
            use_case.run(user_dto)
