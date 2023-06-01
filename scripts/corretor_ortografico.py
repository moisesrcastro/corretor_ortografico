import nltk
import string

nltk.download('punkt')

class CorretorOrtografico():

  alfabeto = string.ascii_lowercase + "áàâãéèêíïóôõúü" + string.ascii_uppercase

  def __init__(self, vocabulario, frequencia):
    self.vocabulario = vocabulario
    self.frequencia = frequencia

  def __OmissaoLetra(self, palavra):

      palavras_geradas = list()

      for i in range(len(palavra)):

          if i == 0:
              for letra_alfabeto in self.alfabeto:
                  nova_palavra = letra_alfabeto + palavra
                  palavras_geradas.append(nova_palavra)

          elif i < len(palavra)-1:
              for letra_alfabeto in self.alfabeto:
                  nova_palavra = palavra[0:i] + letra_alfabeto + palavra[i:]
                  palavras_geradas.append(nova_palavra)

          else:
              
              for letra_alfabeto in self.alfabeto:
                  nova_palavra = palavra + letra_alfabeto
                  palavras_geradas.append(nova_palavra)

      return palavras_geradas
  
  def __AdicaoLetra(self, palavra):

      palavras_geradas = list()

      for i in range(len(palavra)):

          if i == 0:
              for letra_alfabeto in self.alfabeto:
                  nova_palavra = letra_alfabeto + palavra[2:]
                  palavras_geradas.append(nova_palavra)

          else :
              for letra_alfabeto in self.alfabeto:
                  nova_palavra = palavra[0:i] + letra_alfabeto + palavra[i+2:]
                  palavras_geradas.append(nova_palavra)

      return palavras_geradas

  def __SubstituicaoLetra(self, palavra):

      palavras_geradas = list()

      for i in range(len(palavra)):

          if i == 0:
              for letra_alfabeto in self.alfabeto:
                  nova_palavra = letra_alfabeto + palavra[1:]
                  palavras_geradas.append(nova_palavra)

          elif i < len(palavra)-1:
              for letra_alfabeto in self.alfabeto:
                  nova_palavra = palavra[:i] + letra_alfabeto + palavra[i+1:]
                  palavras_geradas.append(nova_palavra)

          else:
              pass

      return palavras_geradas

  def __TransposicaoLetra(self, palavra):

      palavras_geradas = list()

      for i in range(len(palavra)):

          if i == 0:
              for letra_alfabeto in self.alfabeto:
                  nova_palavra = palavra[1]+ letra_alfabeto + palavra[2:]
                  palavras_geradas.append(nova_palavra)

          elif i < len(palavra)-2:
              for letra_alfabeto in self.alfabeto:
                  nova_palavra = palavra[:i] + palavra[i+1] +  letra_alfabeto + palavra[i+2:]
                  palavras_geradas.append(nova_palavra)

          elif i < len(palavra)-1:
              for letra_alfabeto in self.alfabeto:
                  nova_palavra = palavra[:i] + palavra[i+1] +  letra_alfabeto
                  palavras_geradas.append(nova_palavra)            

          else:
              pass

      return palavras_geradas

  def __GeraPalavras(self, palavra):
      lista_palavras = list()
      geradores = [self.__OmissaoLetra, self.__AdicaoLetra, self.__SubstituicaoLetra, self.__TransposicaoLetra]

      for i in geradores:
          lista_palavras += i(palavra)
          
      return lista_palavras

  def __CalculaProbabilidade(self, palavra):
      return self.frequencia[palavra]/ len(self.vocabulario)

  def Corretor(self, palavra):
      lista_palavras_geradas = self.__GeraPalavras(palavra)
      candidatos = [palavra]

      for p in lista_palavras_geradas:
          if p in self.vocabulario:
              candidatos.append(p)
      palavra_correta = max(candidatos, key=self.__CalculaProbabilidade)

      return palavra_correta
  
if __name__ == "__main__":

    with open(r'artigos.txt', 'r', encoding='utf-8') as file:
        artigos = file.read()

    tokens = list()
    palavras_separadas = nltk.tokenize.word_tokenize(artigos)

    for palavra in palavras_separadas:
        if palavra.isalpha():
        tokens.append(palavra.lower())
    else:
        pass

    frequencia = nltk.FreqDist(tokens)
    vocabulario = set(tokens)

    with open(r'/palavras.txt', 'r', encoding='utf-8') as file:
        palavras = file.readlines()
  
    for i in range(len(palavras)):
      palavras[i] = palavras[i].replace('\n', '')

    acertou = 0
    desconhecidas = 0

    for i in range(len(palavras)):
        correta, errada = palavras[i].split(' ')

      #desconhecidas += correta not in vocabulario
        desconhecidas += correta not in vocabulario
        if CorretorOrtografico(vocabulario, frequencia).Corretor(errada) == correta:
            acertou +=1

    print(f'{round(acertou/len(palavras)*100,2)}% e {desconhecidas} palavras desconhecidas')
