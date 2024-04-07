import os
import sys
import art
from prompt_toolkit.shortcuts import prompt,yes_no_dialog
from prompt_toolkit.styles import style_from_pygments_cls, Style
from prompt_toolkit import HTML, PromptSession
from prompt_toolkit import print_formatted_text as print
from pygments.lexers import Python3Lexer
from prompt_toolkit.lexers import PygmentsLexer
from pygments.styles import get_style_by_name
import sqlite3
from natsort import natsorted


def cleanshows(season, extension, showname, directory):
    
    files = natsorted(os.listdir(r"{}".format(directory)))
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS Log(OldName TEXT, NewName TEXT)")

    for i in  range(len(files)):
            
        filename = files[i]
        
        if i < 10:
            i = "0" + str(i+1)
        else:
            i = str(i+1)
        
        new = f"{showname} S{season}E{i}{extension}"
        
        os.rename(os.path.join(directory, filename), 
                os.path.join(directory, new))
        cur.execute(f"INSERT INTO Log VALUES(?,?)",(filename,new))
        
        print(HTML(f"<ansired>Renamed</ansired><skyblue> {filename}</skyblue><ansired> to</ansired><seagreen> {new}</seagreen>"))
            

        
    con.commit()
    return con
    






def main():

    style = style_from_pygments_cls(get_style_by_name('inkpot'))

    ascii_art = art.text2art("SNEN", font="broadway")

    # Print the ASCII art
    print(HTML(f"\n\n<violet>{ascii_art}</violet>\n\n"))
    
    print(HTML("<ansired>Type [q]uit to exit.\n</ansired>"))
    session = PromptSession(lexer=PygmentsLexer(Python3Lexer),style=style,include_default_pygments_style=False
    )
    while True:
        directory = session.prompt("Enter the absolute filepath: ", 
                            )
        
        if directory == "q" or directory == "quit":
            sys.exit()

        season = session.prompt("Enter the season number: ",
                        )

        if season == "q" or directory == "quit":
            sys.exit()
        
        assert len(season) > 1, "Season must be in the format: 0[season] if season < 10. Eg. 01,02,10,21"
        
        extension = session.prompt("Enter the extension of the file: ",
                            )
        if extension == "q" or directory == "quit":
            sys.exit()
        
        assert extension in [".mkv",".mp4"], "Please enter a valid file extension."
        
        showname = session.prompt("Enter the name of the show: ", 
                        )
        if showname == "q" or directory == "quit":
            sys.exit()
        con = cleanshows(season, extension, showname, directory)

        result = session.prompt("Would you like to Undo? [y]es,[n]o: ")
        assert result in ["y","yes","n","no"], "Please enter a valid response."
        
        if result == "y" or result == "yes":
    
            cur = con.cursor()
            for row in cur.execute(f"SELECT OldName, NewName FROM Log"):

                os.rename(os.path.join(directory, row[1]), 
                    os.path.join(directory, row[0]))
            con.close()
        print(HTML("<seagreen>Complete!</seagreen>"))
        con.close()
        sys.exit()

if __name__ == "__main__":
    main()