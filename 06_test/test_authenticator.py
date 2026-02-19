import pytest
from authenticator import Authenticator


@pytest.fixture
def auth():
    """
    テスト用のAuthenticatorインスタンスを作成するフィクスチャ
    """
    return Authenticator()


def test_register_success(auth):
    """
    ユーザー登録が正常に行われることをテストする
    """
    auth.register("testuser", "password123")
    assert "testuser" in auth.users
    assert auth.users["testuser"] == "password123"


def test_register_duplicate_user(auth):
    """
    既に存在するユーザーを登録しようとした場合、
    ValueErrorが発生することをテストする
    """
    auth.register("testuser", "password123")

    with pytest.raises(ValueError) as exc_info:
        auth.register("testuser", "newpassword")

    assert str(exc_info.value) == "エラー: ユーザーは既に存在します。"


def test_login_success(auth):
    """
    正しいユーザー名とパスワードでログインが成功することをテストする
    """
    auth.register("testuser", "password123")
    result = auth.login("testuser", "password123")
    assert result == "ログイン成功"


def test_login_incorrect_password(auth):
    """
    間違ったパスワードでログインしようとした場合、
    ValueErrorが発生することをテストする
    """
    auth.register("testuser", "password123")

    with pytest.raises(ValueError) as exc_info:
        auth.login("testuser", "wrongpassword")

    assert str(exc_info.value) == "エラー: ユーザー名またはパスワードが正しくありません。"
