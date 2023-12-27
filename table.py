from collections import Counter

import pandas as pd

class Harsh ():
    
    def __init__ (self,X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train
        self.freq_table = self.create_freq_table()
        self.prob_table_1 ,self.prob_table_2 = self.create_prob_table()
        self.ord_mat_1 , self.ord_mat_2 = self.get_order_matrix()
    
    
    # -------------------------- frequency table --------------------------------
    def create_freq_table(self):
        train_set = { x:y  for (x,y) in zip(self.X_train, self.y_train) }
        x = " ".join(train_set.keys()).lower()
        y = " ".join(train_set.values())
        new_train_set = list(zip(x.split(),y.split()))
        
        words = list(Counter(x.split()).keys())
        noun = [int(0)]* len(list(words))
        modal = [int(0)]* len(list(words))
        verb = [int(0)]* len(list(words))
        
        for ele in list(new_train_set):
            idx,pos = ele
            idx = int(list(words).index(idx))
            if pos == 'N':
                noun[idx] +=1
            elif pos == 'M':
                modal[idx] +=1
            else:
                verb[idx] +=1
        
        return  pd.DataFrame({
                "Words":list(words),
                "Noun":noun,
                "Modal":modal,
                "Verb":verb
            })
    
    
    
    # ----------------------- proability table --------------------------------
    def create_prob_table (self):
        df1 = self.freq_table.copy()
        df2 = self.freq_table.copy()
        for column in df1.columns[1:]:
            df1[column] = df1[column].astype(str)
            df2[column] = df2[column].astype(float)
        for column in df1.columns[1:]:
            sum = int(self.freq_table[column].sum())
            for i in range (len(df1[column])):
                if df1[column][i] != "0":
                    df2[column][i] /= sum
                    df1[column][i] += "/" + str(sum)
        
        return df1 , df2
    
    
    
    # ------------------------ sentence ordering ------------------------
    def order_sentence (self, sentence):
            return [ "<s> " + i +" <e>" for i in sentence ]
        
        
    def get_order_matrix (self):
        y_sent = self.order_sentence(self.y_train)
        
        tag_table ={
            "<s>":"Start",
            "N":"Noun",
            "M":"Modal",
            "V":"Verb",
            "<e>":"End"
        }
        rows = ["Start","Noun","Modal","Verb"]
        noun = [0] * len(rows)
        modal = [0] * len(rows)
        verb = [0] * len(rows)
        end = [0] * len(rows)
        
        
        for sentence in y_sent :
            tags = sentence.split()
            for i in range(len(tags)-1):
                current = tags[i]
                next = tags[i+1]
                if next == "N":
                    noun[rows.index(tag_table[current])] += 1
                elif next == "M":
                    modal[rows.index(tag_table[current])] += 1
                elif next == "V":
                    verb[rows.index(tag_table[current])] += 1
                elif next == "<e>":
                    end[rows.index(tag_table[current])] += 1
                    

        df2 = pd.DataFrame({
            "":rows,
            "Noun": noun,
            "Modal": modal,
            "Verb": verb,
            "End": end
        })
        
        df1 = df2.copy()
        for column in df1.columns[1:]:
            df1[column] = df1[column].astype(str)
            df2[column] = df2[column].astype(float)
        for i in range(df1.shape[0]):
            sum = df2.iloc[i,1:].sum()
            df2.iloc[i,1:] /= sum
            df1.iloc[i,1:] = df1.iloc[i,1:] + "/" + str(sum)
        
        return df1, df2
    
    
    
    # ------------------------ tagging for x_test ------------------------
    def check_prob(self,prev_tag, current_tag, word, is_end = False):
        a = float(0)
        b = float(0)
        c = float(1)
        
        for i in range (self.ord_mat_2.shape[0]):
            if self.ord_mat_2.iloc[i][0] == prev_tag:
                a = self.ord_mat_2.iloc[i][current_tag]


        for i in range (self.prob_table_2.shape[0]):
            if self.prob_table_2.iloc[i]["Words"] == word:
                b = self.prob_table_2.iloc[i][current_tag]


        if is_end == True:
            for i in range (self.ord_mat_2.shape[0]):
                if self.ord_mat_2.iloc[i][0] == current_tag:
                    c = self.ord_mat_2.iloc[i]["End"]
            
        return a*b*c
        


    def get_tagging(self, X_test):
        sent_copy = X_test.lower().split()
        assigned_tags = []
        possible_tags = ["Noun","Modal","Verb"]
        
        for i in range (len(sent_copy)) :
            highest_prob_idx = 0
            highest_prob = 0
            word = sent_copy[i]
            
            # for starting tag
            if i == 0:
                prev_tag = "Start"
            elif i == len(sent_copy)-1:
                
                pass
            else :
                prev_tag = assigned_tags[i-1]
            for idx in range(len(possible_tags)):
                if self.check_prob(prev_tag,possible_tags[idx],word) > highest_prob:
                    highest_prob_idx = idx
            assigned_tags.append(possible_tags[highest_prob_idx])
        
        return assigned_tags
                