import math
import numpy as np

class perceptron:
    def __init__(self, bits_to_PC, bits_global_history):
        self.perceptron_steps = 0
        self.bits_to_PC = bits_to_PC
        self.bits_to_GH = bits_global_history
        
        self.PC_table_size = bits_to_PC ** 2
        
        self.PC_table = []
        
        # Inicializo la matriz
        for _ in range(bits_to_PC**2):
            self.PC_table.append([0] * bits_global_history)
        
        for i in range(bits_to_PC ** 2):
            for j in range(bits_global_history):
                self.PC_table[i][j] = 0
        
        self.global_history_reg = ""
        for i in range(bits_global_history):
            self.global_history_reg += "0"
        
        self.umbral = math.floor(1.93*bits_global_history + 14)
        
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

    # def predict(self, PC):
    #     perceptron_index = int(PC) % self.PC_table_size
    #     prediction = 0
        
    #     prediction += self.PC_table[perceptron_index][0] # Con esto obtengo w0
        
    #     for i in range(self.bits_to_GH):
    #         prediction += int(self.global_history_reg[-i]) * self.PC_table[perceptron_index][i]
            
    #     if prediction > 0:
    #         return "T"
    #     else:
    #         return "N"

    def predict(self, PC):
        perceptron_index = int(PC) % self.PC_table_size
        pred = 0
        
        pred += self.PC_table[perceptron_index][0] # Con esto obtengo w0
        
        for i in range(self.bits_to_GH):
            if self.global_history_reg[i-1] == 1:
                pred += self.PC_table[perceptron_index][i] * int(self.global_history_reg[-i])
            else:
                pred -= self.PC_table[perceptron_index][i] * int(self.global_history_reg[-i])
        
        self.perceptron_steps = abs(pred)
            
        if pred > 0:
            return "T"
        else:
            return "N"

    def update(self, PC, result, prediction):
        perceptron_index = int(PC) % self.PC_table_size
        # Aquí está lo que viene en el repo de GitHub: https://github.com/taraeicher/PerceptronBranchPredictor/blob/master/perceptron.cc
        
        # if (result != prediction) or (self.perceptron_steps <= self.umbral):
            
        #     if (result == "T"):
        #         new_val = self.PC_table[perceptron_index][0] + 1
        #         if (new_val > 128):
        #             self.PC_table[perceptron_index][0] = 128
        #         else:
        #             self.PC_table[perceptron_index][0] += 1
        #     else:
        #         new_val = self.PC_table[perceptron_index][0] - 1
        #         if (new_val < -128):
        #             self.PC_table[perceptron_index][0] = -128
        #         else:
        #             self.PC_table[perceptron_index][0] -= 1
            
            
        #     for i in range(self.bits_to_GH):
        #         # Actualizo pesos
        #         if (result == "T" and self.global_history_reg[-i] == 1) or (result == "N" and self.global_history_reg[-i] == 0):
        #             new_val = self.PC_table[perceptron_index][i] + 1
        #             if (new_val > self.umbral):
        #                 self.PC_table[perceptron_index][i] = self.umbral
        #             else:
        #                 self.PC_table[perceptron_index][i] += 1
        #         else:
        #             new_val = self.PC_table[perceptron_index][i] - 1
        #             if (new_val < self.umbral * (-1)):
        #                 self.PC_table[perceptron_index][i] = self.umbral * (-1)
        #             else:
        #                 self.PC_table[perceptron_index][i] -= 1
        # #Update GHR
        # if result == "T":
        #     self.global_history_reg = self.global_history_reg[-self.bits_to_GH+1:] + "1"
        # else:
        #     self.global_history_reg = self.global_history_reg[-self.bits_to_GH+1:] + "0"
        
        
        # De aquí para abajo está lo que yo implementé 
        
        # Calculo de nuevo la predicción para poder actualizar mis pesos
        pred = 0
        pred += self.PC_table[perceptron_index][0] # Con esto obtengo w0
        # pred = 0
        
        # pred += self.PC_table[perceptron_index][0] # Con esto obtengo w0
        
        for i in range(self.bits_to_GH):
            pred += int(self.global_history_reg[i]) * self.PC_table[perceptron_index][i]

        # Para poder implementar el pseudo código del paper
        if result == "T":
            t = 1
        else:
            t = -1
        
        if np.sign(pred) != t or abs(pred) <= self.umbral:
            for i in range(self.bits_to_GH):
                self.PC_table[perceptron_index][i] += self.PC_table[perceptron_index][i] + t*int(self.global_history_reg[-i])

        # #Update GHR
        if result == "T":
            self.global_history_reg = self.global_history_reg[-self.bits_to_GH+1:] + "1"
        else:
            self.global_history_reg = self.global_history_reg[-self.bits_to_GH+1:] + "0"
        
        #Update stats
        if result == "T" and result == prediction:
            self.total_taken_pred_taken += 1
        elif result == "T" and result != prediction:
            self.total_taken_pred_not_taken += 1
        elif result == "N" and result == prediction:
            self.total_not_taken_pred_not_taken += 1
        else:
            self.total_not_taken_pred_taken += 1
            
        self.total_predictions += 1
        #Escriba aquí el código para actualizar
        #La siguiente línea es solo para que funcione la prueba
        #Quítela para implementar su código
