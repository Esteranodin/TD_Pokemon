import re, unicodedata
import pandas as pd

class PandasImport:

    def __init__(self):
        pass

    def __str__(self):
        # pass
        return f"{self.__class__.__name__}()"
    def __repr__(self):
        # pass
        return f"{self.__class__.__name__}()"

    def lower_text(self, text:str, keep=[]) -> str:
        """ 
        Sets uppercases to lowercases, except for strings put in keep:
            - text: string to be lower
            - keep: list of exceptions in text not to change, each element must be a string
        Returns lowercased text with unchanged exceptions
        Found and adapted from https://stackoverflow.com/questions/54250594/python-replace-all-words-in-a-string-except-some
        """
        return re.sub(r'\b\w+\b', lambda w: w.group() if w.group() in keep else w.group().lower(), text)

    def capitalize_text(self, text:str, keep=[]) -> str:
        """ 
        Sets first letter of text in uppercase, the rest in lowercase, except if first word in keep, in which case first letter is unchanged:
            - text: string to be lower
            - keep: list of exceptions in text not to change, each element must be a string
        Returns capitalized text with unchanged exceptions
        Found and adapted from https://stackoverflow.com/questions/54250594/python-replace-all-words-in-a-string-except-some
        """
        for exc in keep:
            if text.find(exc) == 0:
                return re.sub(r'\b\w+\b', lambda w: w.group() if w.group() in keep else w.group().lower(), text)
        temp = re.sub(r'\b\w+\b', lambda w: w.group() if w.group() in keep else w.group().lower(), text)
        return temp[0].upper() + temp[1:]

    def remove_accents(self, text:str) -> str:
        """ 
        Removes accents from text:
            - text: string where accents have to be removed
        Returns text without accents
        Found and adapted by Marion
        Unicodedata categories : https://www.unicode.org/reports/tr44/tr44-34.html#General_Category_Values
        """
        return ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) not in ['Mn', 'Sk']
        )

    def remove_punctuations(self, text:str, keep=[]) -> str:
        """ 
        Removes punctuation (all that is not an alphanumerical caracter or a space) from text, except for the symbols in keep:
            - text: string where punctuation should be removed
            - keep: list of punctuation in text not to remove, each element must be a string
        Returns text without punctuation.
        Found and adapted from 
        TO LOOOK: https://www.youtube.com/watch?v=7DG3kCDx53c&feature=youtu.be
        """
        # return re.sub(r'\b^\w+\b', lambda w: "" if w.group() in keep else w.group().lower(), text)
        # return re.sub(r"[^a-zA-Z0-9\s:]", lambda w: "" if w.group() in keep else w.group().lower(), text)
        return re.sub(r'[^\w\s]', lambda w: w.group() if w.group() in keep else '', text)

    def clean_spaces(self, text:str, sep="_") -> str:
        """ 
        Changes spaces to given separator sep:
            - text: string where spaces have to be replaced by given separator sep
            - sep: symbol replacing the spaces. Default is '_'
        Returns text with spaces replaced by separator sep
        """

        # return text.replace(" ", sep) # pour un seul espace
        return re.sub(r'\s+', sep, text.strip())
    
   

# --------------------------------------------------------------------------------------------

    def final_clean(self, text:str, 
                    do_lower:bool=True, keep_lower=[], 
                    do_capitalize:bool=False, keep_capitalize=[], 
                    del_accent:bool=True, 
                    del_punctuation:bool=True, keep_punctuation=[], 
                    spaces_to_sep:bool=True, sep:str="_",
                    ) -> str:
        """ 
        Cleans given input text as following:
            - text: text to clean.
            - Lowering text:
                * do_lower: Applies PandasImport.lower_text. Default=True.
                * keep_lower: words that will not be changed by the function. Default=[].
            - Capitalizing text:
                * do_capitalize: Applies PandasImport.capitalize_text. Default=False.
                * keep_capitalize: words that will not be changed by the function. Default=[].
            - Delete accents:
                * del_accent: Applies PandasImport.remove_accent. Default=True.
            - Delete punctuation:
                * del_punctuation: Applies PandasImport.remove_punctuation. Default=True.
                * keep_punctuation: punctuation which will not be removed by the function. Default=[].
            - Replace spaces by other symbol:
                * spaces_to_sep: Applies PandasImport.clean_spaces. Default=True
                * sep: separator used to replace spaces. Default='_'.
        Returns string of text where every operations have been performed.
        """
        text = text.strip()
        if do_lower:
            text = self.lower_text(text, keep=keep_lower)
        elif do_capitalize:
            text = self.capitalize_text(text, keep=keep_capitalize)
        else:
            pass
        if del_accent:
            text = self.remove_accents(text)
        if del_punctuation:
            text = self.remove_punctuations(text, keep=keep_punctuation)
            # text = self.test_remove_punctuations(text, keep=keep_punctuation)
        if spaces_to_sep:
            text = self.clean_spaces(text, sep=sep)
        return text
    

# --------------------------------------------------------------------------------------------

    def replace_one_term(self, text:str, in_word="", out_word="") -> str:
        """ 
        Replaces in_word by out_word in text:
            - text: text where terms have to be replaced
            - in_word: word to be replaced. Default="".
            - out_word: replacing word. Default="".
        Returns string of text where in_word has been replace by out_word, if in_word in text.
        """
        return text.replace(in_word, out_word)
    
       
    def format_float_cols(self, df, labels_col) :
        # ATTENTION: une série a beau être typée string via .dtype == str, parcourue élément par élément via .apply, les Nan sont considérés comme des floats !
        # d'où la double vérification .dtype et type(x) both strings
        for lab in labels_col:
            if df[lab].dtype=='str': 
                df[lab] = df[lab].apply(lambda x: re.sub(r'\.+', '.', re.sub(r'[^0-9.]+', '', x)) if type(x)==str else x)
        return df

    def convert_to_float(self, series):
        return pd.to_numeric(series, errors='coerce')