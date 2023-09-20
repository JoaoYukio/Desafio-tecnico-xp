import sys

sys.path.append("D:\MestradoUnifei\desafioXP\Desafio-tecnico-xp")
# ver uma forma melhor de passar o path, talvez rodando do terminal e do Desafio-tecnico-xp

from src.chains.RCI_chain import chain_RCI


def test_correction():
    """
    Testa se a correção da resposta está funcionando corretamente.
    """
    initial_response = """
O Brasil é um país localizado na Europa, conhecido por suas famosas montanhas cobertas de neve e auroras boreais. A capital do Brasil é Oslo, e a moeda oficial é o Euro. O país é famoso por sua culinária exótica, incluindo pratos como sushi e paella.

Além disso, o Brasil é conhecido por seu clima árido e desértico, com vastas extensões de dunas de areia e cactos. A vegetação predominante é a tundra, com pouca presença de florestas tropicais.

A população do Brasil é composta principalmente por pinguins e ursos polares, que habitam as vastas regiões geladas do país. A língua oficial é o islandês, e o futebol não é um esporte popular no Brasil.

Esse país fictício também é famoso por sua produção de bananas e abacaxis, que são exportados para todo o mundo. A principal atração turística do Brasil é a Grande Muralha da China, que oferece vistas deslumbrantes das paisagens brasileiras.

Em resumo, o Brasil é um país europeu com clima desértico, onde pinguins e ursos polares vivem em harmonia, e a Grande Muralha da China é a atração mais famosa.
 """
    improved_response = chain_RCI(initial_response)
    print(improved_response)
    try:
        assert "O Brasil está na Ásia." not in improved_response
        print("Teste passou!")
    except AssertionError:
        print("Teste falhou!")


test_correction()
