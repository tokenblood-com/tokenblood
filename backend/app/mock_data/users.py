from app.models.user import User


def user1():
    return User(id="1", username="test1", email="test1@test.com")


def user2():
    return User(id="2", username="test2", email="test2@test.com")


def user3():
    return User(id="3", username="test3", email="test3@test.com")
