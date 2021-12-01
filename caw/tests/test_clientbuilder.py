import unittest
from unittest.mock import Mock, patch

import typer

from chris.types import CUBEAddress, CUBEToken, CUBEUsername, CUBEPassword
from chris.errors import ChrisIncorrectLoginError
from caw.builder import ClientBuilder
from caw.login.manager import LoginManager


class ClientBuilderTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.lm = Mock(spec=LoginManager)
        self.builder = ClientBuilder(self.lm)

    # @patch('caw.builder.FriendlyClient')
    # def test_using_default_session(self, constructor):
    #     address = CUBEAddress('https://example.com/api/v1/')
    #     token = CUBEToken('my_token_value')
    #     self.lm.get_default_address.return_value = address
    #     self.lm.get.return_value = token
    #
    #     self.builder()
    #     constructor.assert_called_once_with(address, token=token)

    # @patch('caw.builder.FriendlyClient')
    # def test_using_token_and_specific_address(self, constructor):
    #     address = CUBEAddress('https://example.com/api/v1/')
    #     token = CUBEToken('my_token_value')
    #     self.lm.get.return_value = token
    #     self.builder.address = address
    #
    #     self.builder()
    #     constructor.assert_called_once_with(address, token=token)
    #     self.lm.get_default_address.assert_not_called()

    # @patch('caw.builder.FriendlyClient')
    # def test_using_username_password(self, constructor):
    #     self.builder.address = CUBEAddress('https://example.com/api/v1/')
    #     self.builder.username = CUBEUsername('crab')
    #     self.builder.password = CUBEPassword('shrimp')
    #
    #     self.builder()
    #     constructor.assert_called_once_with(self.builder.address,
    #                                         username=self.builder.username,
    #                                         password=self.builder.password)
    #     self.lm.get_default_address.assert_not_called()
    #     self.lm.get.assert_not_called()

    @patch('typer.secho', spec=typer.secho)
    @patch('chris.client.ChrisClient.__init__', side_effect=ChrisIncorrectLoginError)
    def test_logout_after_token_expired(self, _, secho):
        address = CUBEAddress('https://example.com/api/v1/')
        self.lm.get_default_address.return_value = address
        self.lm.get.return_value = CUBEToken('my_token_value')

        with self.assertRaises(typer.Abort):
            self.builder()

        self.lm.get_default_address.assert_called_once()
        self.lm.get.assert_called_once_with(address)
        self.lm.logout.assert_called_once_with(address)
        secho.assert_called_with(
            f'warning: removing saved login for {address}.\n'
            f'To login again, run\n'
            f"\n\tcaw --address '{address}' login",
            err=True
        )


class UserErrorsTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.lm = Mock(spec=LoginManager)
        self.builder = ClientBuilder(self.lm)

    @patch('typer.echo', spec=typer.echo)
    def test_given_username_no_password(self, echo):
        self.builder.username = CUBEUsername('crab')
        with self.assertRaises(typer.Abort):
            self.builder()
        echo.assert_called_with('Given a username but no password. You must supply both.', err=True)

    @patch('typer.echo', spec=typer.echo)
    def test_given_password_no_username(self, echo):
        self.builder.password = CUBEPassword('crab')
        with self.assertRaises(typer.Abort):
            self.builder()
        echo.assert_called_with('Given a password but no username. You must supply both.', err=True)


if __name__ == '__main__':
    unittest.main()
