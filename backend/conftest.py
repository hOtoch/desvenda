"""Configuração comum a todos os testes do backend."""

import socket

import pytest
from pytest_socket import SocketConnectBlockedError

_getaddrinfo_original = socket.getaddrinfo


@pytest.fixture(autouse=True)
def bloqueia_consulta_de_nome_externo(request, monkeypatch):
    """Recusa a consulta de nomes fora da lista do `--allow-hosts`.

    O pytest-socket bloqueia o `connect`, mas não o `getaddrinfo` que vem antes dele: sem esta
    guarda, um teste ainda consultaria o DNS de verdade antes de ser barrado.
    """
    permitidos = request.config.getoption("--allow-hosts").split(",")

    def getaddrinfo_so_local(host, *args, **kwargs):
        if host is not None and host not in permitidos:
            raise SocketConnectBlockedError(permitidos, host)
        return _getaddrinfo_original(host, *args, **kwargs)

    monkeypatch.setattr(socket, "getaddrinfo", getaddrinfo_so_local)
