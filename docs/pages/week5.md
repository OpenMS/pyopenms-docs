# Woche 5

1. Änderungen:
   1. Docstrings hinzugefügt zur Erleuterung mit der help()-Funktion in python.
   2. Implementierung von Errorhandling begonnen.
   3. Im Ordner model eine tableDataFrame.py file angelegt, welche Funktionalitäten für Group, Fraction und Label beinhaltet.
   4. Design der Anwendung etwas angepasst.
   5. Save-Button entfernt und zusätzlich Import, Export, Add File, Remove File, Select All Buttons sowie ein Eingabefeld für den
      Search-Button hinzugefügt.
   4. Funktionalität für alle Buttons ausgenommen Search implementiert.
   
2. Bugs:
      - Select All selectiert zwar alles, allerdings stimmt die Darstellung nicht immer überein(mal wird nichts markiert,
         mal wird alles grau markiert, mal tatsächlich markiert oder aber auch manche markiert und andere nicht)
      - Remove File besizt derzeit noch ein seltsames Verhalten, mit Select All kann die ganze Tabelle gelöscht werden,
         ist ein einzelner Eintrag markiert so kann dieser gelöscht werden, sind allerdings mehrere Einträge markiert,
         sowerden nicht zwangsläufig die markierten gelöscht und wenn dann die markierten noch da sind und man erneut
         löscht kann es zum Crash mit einem KeyError [...] not found in axis kommen

3. TypeHinting:
    - Definition: Type von Eingabe- und Ausgabeparameter einer Funktion festlegen.
    - Dies ist nützlich da jederzeit feststeht womit eine Funktion arbeitet, was beim Debugging hilfreich ist, da wir
      uns direkt Typefehler ausgeben lassen können, und das Verstehen der Funktion für andere erleichtert.

4. Screenshots:
    ![alt text](../Screenshots/normalstart.png "Initialfenster")
    ![alt text](../Screenshots/loaded.png "gefüllte Tabelle")
    ![alt text](../Screenshots/filled.png "Bearbeitete Tabelle")
