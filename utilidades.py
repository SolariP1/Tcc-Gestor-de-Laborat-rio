def contar_letras(string):
    string = string.replace(" ", "")
    return len(string)

def contar_espacos(string):
    return string.count(" ")


def bubble_sort(vetor):
    n = len(vetor)
    # Percorre todos os elementos do vetor
    for i in range(n):
        # Últimos i elementos já estão no lugar certo
        for j in range(0, n-i-1):
            # Troca se o elemento atual for maior que o próximo
            if vetor[j] > vetor[j+1]:
                vetor[j], vetor[j+1] = vetor[j+1], vetor[j]

