import pandas as pd

class PokemonDf:

    def __init__(self):
        self.exc_dict = {
            "forme": ("origin", "normal", "aria", "therian", "blade", "ordinary", "speed", "resolute", "altered", "50%", "sky", "attack", "defense", "incarnate", "shield", "land", "pirouette"),
            "mode" : ("standard", "zen"),
            "size" : ("super", "large", "average", "small"),
            "cloak": ("sandy", "trash", "plant"),
            "other": ('primal', 'mega', 'wash', 'heat', 'frost', 'fan', 'white', 'black', 'mow')
        }  

    # def format_df(self, df):
    #     df = df.transpose()
    #     df = df.reset_index(drop=True)

    #     # https://stackoverflow.com/questions/26147180/convert-row-to-column-header-for-pandas-dataframe
    #     df.columns = df.iloc[0]
    #     # df = df.iloc[pd.RangeIndex(len(df)).drop(0)]
    #     df = df.iloc[1:].reset_index(drop=True)
    #     df = df.reset_index(drop=True)

    #     df = df.rename(columns={"#": "ID"})
    #     return df


    def format_name(self, x, sep="_"):
        x = x.lower()
        # do_delete_xlast = False 
        # Flag a redecommenter pour ne pas supprimer les doublons sur nom typer RotomWash Rotom 
        try:
            x_first, x_last, *rest = x.split(sep)
            if x_last in self.exc_dict.keys(): # i.e. form, size, etc NOT mega, blabla
                x_dict_values = self.exc_dict[x_last]
            else:
                # do_delete_xlast = True
                x_dict_values = self.exc_dict["other"]
            for val in x_dict_values:
                if val in x_first:
                    x_first = x_first.replace(val, "")
                    res = x_first.capitalize() + val.capitalize() 
                    # if not do_delete_xlast :
                    #     res += sep + x_last.capitalize()
                    if rest != []: res+= sep + "".join(element.capitalize() for element in rest)
                    return res
            return x.title() # gÃ©rer les Mr. Mime, Mime Jr. et les deux trois autres bizarreries
        except ValueError: #i.e. 1 seul mot dans le nom
            return x.title()
    

    def format_columns_names(self, df, columns):
        """Apply format_name to each specified column in the DataFrame."""
        for col in columns:
            if col in df.columns:
                df[col] = df[col].astype(str).apply(self.format_name)
        return df

    def format_columns_to_float(self, df, columns):
            for col in columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype(float)
            return df
    
# --------------------------------------------------------------------------------------------

#  pour trouver les exceptions au fur et a mesure
    def mask_exc_name(self, df, sep="_"):
        mask_comp = df["name"].str.split(sep).apply(len)>1
        mask_rest = df["name"].apply(lambda x: sum(1 for car in x.split(sep)[0] if car.isupper()))==1
        return mask_comp & mask_rest
    # shows exceptions
    # display(df_pokemon[mask_exc_name(df_pokemon)])
    
    def sort_by(self, df, col_name):
        return df.sort_values(by=[col_name]).reset_index(drop=True)
    