import math
import numpy as np

class perceptron:
    def __init__(self, bits_to_PC, bits_global_history):
        self.bits_to_PC = bits_to_PC
        self.bits_to_GH = bits_global_history
        
        self.PC_table_size = bits_to_PC ** 2
        
        # Inicializo la matriz
        self.PC_table = np.zeros((2**bits_to_PC, bits_global_history+1))
        
        self.global_history_reg = ""
        for i in range(bits_global_history):
            self.global_history_reg += "0"
        
        self.umbral = math.floor(1.93*bits_global_history + 14)
        self.pred = 0
        self.x0 = 1
        
        #Escriba aquí el init de la clase
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0

    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\tPerceptron")
        print("\tEntradas en el Predictor:\t\t\t"+str(2**self.bits_to_PC))
        print("\tTamaño de los registros de historia global:\t"+str(self.bits_to_GH))

    def print_stats(self):
        print("Resultados de la simulación")
        print("\t# branches:\t\t\t\t\t\t"+str(self.total_predictions))
        print("\t# branches tomados predichos correctamente:\t\t"+str(self.total_taken_pred_taken))
        print("\t# branches tomados predichos incorrectamente:\t\t"+str(self.total_taken_pred_not_taken))
        print("\t# branches no tomados predichos correctamente:\t\t"+str(self.total_not_taken_pred_not_taken))
        print("\t# branches no tomados predichos incorrectamente:\t"+str(self.total_not_taken_pred_taken))
        perc_correct = 100*(self.total_taken_pred_taken+self.total_not_taken_pred_not_taken)/self.total_predictions
        formatted_perc = "{:.3f}".format(perc_correct)
        print("\t% predicciones correctas:\t\t\t\t"+str(formatted_perc)+"%")

    def predict(self, PC):
        perceptron_index = int(PC) % self.PC_table_size
        
        self.pred = self.PC_table[perceptron_index][0] * self.x0 # Con esto obtengo w0
        
        for i in range(1, self.bits_to_GH+1): # Estoy iterando desde [1, GH+1]
                                              # Es decir, las filas desde w1-wn
            self.pred += self.PC_table[perceptron_index][i] * self.reg(self.global_history_reg[-i])

        if self.pred >= 0:
            return "T"
        else:
            return "N"

    def update(self, PC, result, prediction):
        perceptron_index = int(PC) % self.PC_table_size

        # Para poder implementar el pseudo código del paper
        if result == "T":
            t = 1
        else:
            t = -1
        
        # Pseudo código del paper para actualizar pesos
        if np.sign(self.pred) != t or abs(self.pred) <= self.umbral:
            # Actualizar por aparte a w0
            self.PC_table[perceptron_index][0] = self.PC_table[perceptron_index][0] + t*self.x0
            
            for i in range(1, self.bits_to_GH+1):
                self.PC_table[perceptron_index][i] += t*self.reg(self.global_history_reg[-i])

        # Update GHR
        if result == "T":
            self.global_history_reg = self.global_history_reg[-self.bits_to_GH+1:] + "1"
        else:
            self.global_history_reg = self.global_history_reg[-self.bits_to_GH+1:] + "0"
        
        # Update stats
        if result == "T" and result == prediction:
            self.total_taken_pred_taken += 1
        elif result == "T" and result != prediction:
            self.total_taken_pred_not_taken += 1
        elif result == "N" and result == prediction:
            self.total_not_taken_pred_not_taken += 1
        else:
            self.total_not_taken_pred_taken += 1
            
        self.total_predictions += 1
        
    def reg(self, bit):
        if bit == "1":
            return 1
        elif bit == "0":
            return -1