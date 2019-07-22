def decode(s:str) -> str:
    """ 
    Implementation of the bencoding format
    <BE>    ::= <DICT> | <LIST> | <INT> | <STR>
    <DICT>  ::= "d" 1 * (<STR> <BE>) "e"
    <LIST>  ::= "l" 1 * <BE>         "e"
    <INT>   ::= "i"     <SNUM>       "e"
    <STR>   ::= <NUM> ":" n * <CHAR>; where n equals the <NUM>

    <SNUM>  ::= "-" <NUM> / <NUM>
    <NUM>   ::= 1 * <DIGIT>
    <CHAR>  ::= %
    <DIGIT> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
    """
    def decode_str(s:str) -> str:
        ret = ""
        len_s = 0
        i = 0
        print(s)
        while i < len(s):
            print(s[i])
            if s[i].isdigit():
                len_s = len_s*10+int(s[i])
                i += 1
            else:
                break
        print("Length is", len_s)
        if len(s) != len_s+2:
            raise ValueError("Incorrectl length for string!")
        return s[i:-1]
    
    return decode_str(b'12:Middle Earth')

if __name__ == "__main__":
    decode("")
