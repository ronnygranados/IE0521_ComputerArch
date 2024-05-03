class pshared:
    def __init__(self, bits_to_index, local_history_size):
        # Acá defino los tamaños de la tabla PC y LH
        self.bits_to_index = bits_to_index
        self.size_of_PC_table = 2**bits_to_index # n
        
        self.local_history_size = local_history_size
        self.size_LH_table = 2**local_history_size # m
        
        # Creo las respectivas tablas de PC y de Historia Global
        self.LH_table = [0 for i in range(self.size_LH_table)]
        self.PC_table = [] # Tabla vacía para llenarla con los registros locales
        
        self.local_history_reg = ""
        for i in range(local_history_size):
            self.local_history_reg += "0"
        
        self.PC_table = [self.local_history_reg for i in range(self.size_of_PC_table)]

        #Escriba aquí el init de la clase
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0

    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\t\tP-Shared")
        print("\tEntradas en el Predictor:\t\t\t"+str(2**self.bits_to_index))
        print("\tTamaño de los registros de historia global:\t"+str(self.local_history_size))

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
        pc_index = int(PC) % self.size_of_PC_table
        LH_index = int(self.PC_table[pc_index], 2)
        LH_table_entry = self.LH_table[LH_index] # Aquí accedo a la predicción [0,1,2,3]

        if LH_table_entry in [0, 1]:
            return "N"
        else:
            return "T"

    def update(self, PC, result, prediction):
        pc_index = int(PC) % self.size_of_PC_table
        HL_index = int(self.PC_table[pc_index], 2)

        LH_table_entry = self.LH_table[HL_index] # Aquí accedo a la predicción [0,1,2,3]

        # Actualizo la tabla de HL
        #   Llego hasta 3 porque son solamente 2 bits de predicción
        if LH_table_entry == 0 and result == "N":
            updated_LH_table_entry = LH_table_entry
        elif LH_table_entry != 0 and result == "N":
            updated_LH_table_entry = LH_table_entry - 1
        elif LH_table_entry == 3 and result == "T":
            updated_LH_table_entry = LH_table_entry
        else:
            updated_LH_table_entry = LH_table_entry + 1
        
        self.LH_table[HL_index] = updated_LH_table_entry
        
        # Actualizar tabla de PC
        if (result == "T"):
            entry_reg = self.PC_table[pc_index]
            entry_reg = entry_reg[-self.local_history_size+1:] + "1"
            self.PC_table[pc_index] = entry_reg
            
        else:
            entry_reg = self.PC_table[pc_index]
            entry_reg = entry_reg[-self.local_history_size+1:] + "0"
            self.PC_table[pc_index] = entry_reg
        
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