import sys

sys.path.append("D:\MestradoUnifei\desafioXP\Desafio-tecnico-xp")
# ver uma forma melhor de passar o path, talvez rodando do terminal e do Desafio-tecnico-xp

from src.chains.RCIChain import chain_RCI


def test_correction():
    """
    Testa se a correção da resposta está funcionando corretamente.
    """
    initial_response = "O Brasil está na Ásia."
    improved_response = chain_RCI(initial_response)
    print(improved_response)
    try:
        assert "O Brasil está na Ásia." not in improved_response
        print("Teste passou!")
    except AssertionError:
        print("Teste falhou!")


test_correction()
