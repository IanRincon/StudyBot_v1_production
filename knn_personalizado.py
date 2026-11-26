import numpy as np

# Definición del algoritmo propio de KNN

class KNN_Classifier:
    def __init__(self, k):
        self.k = k
        self.xInstancias = None
        self.yInstancias = None

    def distanciaEuclidiana(self, vector1, vector2):
        return np.sqrt(np.sum((vector1 - vector2)**2))

    def crearInstancia(self,xInstancias,yInstancias):
        self.xInstancias = xInstancias
        self.yInstancias = yInstancias

    def predicir(self,ds_x):
      x = np.array(ds_x)
      y_pred = [self.predecirFeature(i) for i in x]
      return np.array(y_pred)

    def predecirFeature(self,x):
      distancia = [self.distanciaEuclidiana(x, i) for i in self.xInstancias]
      topKVecinos = np.argsort(distancia)[:self.k]

      return np.bincount(self.yInstancias[topKVecinos]).argmax()



