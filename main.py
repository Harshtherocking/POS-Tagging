from table import Harsh
if __name__ == "__main__":

    X_train = [
        "Mary Jane can see Will",
        "Spot will see Mary",
        "Will Jane spot Mary",
        "Mary will pat Spot"
        ]

    y_train = [
        "N N M V N",
        "N M V N",
        "M N V N",
        "N M V N"
        ]

    table = Harsh(X_train,y_train)
    print(table.prob_table_1)
    print("\n")
    print(table.ord_mat_1)


    X_test = input("Enter the sentence from the word corpus : " )

    taggings = table.get_tagging(X_test)

    print("The taggings are as followed : \n")
    print(taggings)