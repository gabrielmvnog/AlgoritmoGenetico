import random

target = 'Ola Mundo!'
geneSet = ' !QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'
numGenes = len(target)
taxaCrossover = 0.6
taxaMutacao = 0.3
tamPop = 100
maxGeracao = 10000
geracao = 0

class Individuo():
    def __init__ (self, genes, aptidao):
        self.genes = genes
        self.aptidao = aptidao

    def __repr__(self):
        return 'Cromossomo: ' + self.genes + ' | Aptidão: ' + str(self.aptidao) + '\n'

def fitness(cromossomo):
    return sum(1 for s, c in zip(target, cromossomo) if s == c)

def gerarIndividuo():
    cromossomo = ''.join(random.sample(geneSet,numGenes))
    aptidao = fitness(cromossomo)
    individuo = Individuo(cromossomo, aptidao)
    return individuo

#gera a primeira população 
def gerarPopulacao():
    individuos = []
    for x in range(0, tamPop):
        individuos.append(gerarIndividuo())
    return sorted(individuos, key = lambda individuo: individuo.aptidao, reverse = True)

#escolhe 3 individuos e pega os 2 primeiros mais aptos
def selecaoTorneio(populacao):
    aux = []
    aux.append(populacao[random.randint(0,len(populacao)-1)])
    aux.append(populacao[random.randint(0,len(populacao)-1)])
    aux.append(populacao[random.randint(0,len(populacao)-1)])
    return sorted(aux, key = lambda individuo: individuo.aptidao, reverse = True)

def mutacao(gene):

    #Se for preciso mutar, vai trocar o gene daquela posição aleatória
    if random.uniform(0.0,0.1) <= taxaMutacao:
        ind = random.randint(0,numGenes-1)
        gene = gene.replace(gene[ind],random.sample(geneSet,numGenes)[0])
    
    return gene
    
#Ocorre o cruzamento de genes entre os indivíduos pais, gerando novos indivíduos
def crossover(pais):
    filhos = []

    pontoCorte1 = random.randint(1, (numGenes/2 - 1))
    pontoCorte2 = random.randint(numGenes/2, (numGenes - 1))

    geneFilho1 = pais[0].genes[:pontoCorte1] + pais[1].genes[pontoCorte1:pontoCorte2] + pais[0].genes[pontoCorte2:numGenes]
    geneFilho2 = pais[1].genes[:pontoCorte1] + pais[0].genes[pontoCorte1:pontoCorte2] + pais[1].genes[pontoCorte2:numGenes]

    geneFilho1 = mutacao(geneFilho1)
    geneFilho2 = mutacao(geneFilho2)

    aptidao1 = fitness(geneFilho1)
    aptidao2 = fitness(geneFilho2)
    
    filhos.append(Individuo(geneFilho1, aptidao1))
    filhos.append(Individuo(geneFilho2, aptidao2))

    return filhos

#Gera uma nova população com indivíduos mais aptos
def gerarNovaGeracao(populacao):
    novosIndividuos = []
    novosIndividuos.append(populacao[0])

    while len(novosIndividuos) <= len(populacao):

        if(random.uniform(0.0,1.0) <= taxaCrossover):
            filhos = crossover(selecaoTorneio(populacao))
            novosIndividuos.append(filhos[0])
            novosIndividuos.append(filhos[1])
        else:
            novosIndividuos.append(populacao[0])
            novosIndividuos.append(populacao[1])

    return sorted(novosIndividuos, key = lambda individuo: individuo.aptidao, reverse = True)

if __name__ == "__main__":

    #gera minha primeira populacao ordenada
    populacao = gerarPopulacao()

    print 'Iniciando... Aptidão da solucão: ' + str(numGenes)

    while geracao <= maxGeracao:
        geracao += 1

        #cria nova geracao
        populacao = gerarNovaGeracao(populacao)

        print 'Geração: ' + str(geracao) + '\t| Aptidão: ' + str(populacao[0].aptidao) + '\t| Cromossomo: ' + populacao[0].genes

        if populacao[0].aptidao == numGenes:
            break
    
    if geracao == maxGeracao:
        print 'Número máximo de gerações!'
    else:
        print 'Encontrado resultado na geração: ' + str(geracao)



