"""Os testes não acessam a rede externa (Princípio III), mas acessam a própria máquina.

Se algum destes testes falhar, o bloqueio de rede foi desligado ou mudou.
"""

import socket
import threading
import time

import pytest

# 192.0.2.0/24 (TEST-NET-1) é reservada para documentação: nunca leva a um servidor de verdade.
ENDERECO_EXTERNO = ("192.0.2.1", 80)
NOME_EXTERNO = "example.com"


def _confere_bloqueio(erro: pytest.ExceptionInfo[BaseException]) -> None:
    # Compara pelo nome para o teste falhar com uma mensagem clara mesmo sem o plugin instalado.
    assert type(erro.value).__name__ == "SocketConnectBlockedError", repr(erro.value)


def test_conexao_por_endereco_externo_e_bloqueada_na_hora():
    inicio = time.monotonic()
    with pytest.raises(Exception) as erro, socket.socket() as conexao:
        conexao.settimeout(2)
        conexao.connect(ENDERECO_EXTERNO)
    _confere_bloqueio(erro)
    assert time.monotonic() - inicio < 1


def test_conexao_por_nome_externo_e_bloqueada():
    with pytest.raises(Exception) as erro:
        socket.create_connection((NOME_EXTERNO, 80), timeout=2).close()
    _confere_bloqueio(erro)


def test_consulta_de_nome_externo_e_bloqueada():
    with pytest.raises(Exception) as erro:
        socket.getaddrinfo(NOME_EXTERNO, 80)
    _confere_bloqueio(erro)


def test_conexao_com_a_propria_maquina_e_permitida():
    with socket.create_server(("127.0.0.1", 0)) as servidor:
        porta = servidor.getsockname()[1]
        aceite = threading.Thread(target=lambda: servidor.accept()[0].close())
        aceite.start()
        with socket.create_connection(("127.0.0.1", porta), timeout=2):
            pass
        aceite.join(timeout=2)
