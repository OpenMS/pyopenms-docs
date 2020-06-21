# Woche 7

1. Arbeitet euch in Profiling mit trace und timeit ein
     - trace gibt einfach in der Konsole aus was genau gemacht wird, mit der option --trace
       z.Bsp. wird jeder funktionsaufruf bis ins detail angezeigt
     - timeit stellt verschiedene Möglichkeiten zur Verfügung um runtime zu testen 
        (bei uns wird über einen boolean bestimmt ob die runtimes der ausgeführten funktionen im
         Terminal angezeigt werden sollen, wobei timeit nur die Zeit zu Beginn der Funktion nimmt
         und dann die Zeit von der aktuellen abzieht um eine aktuelle runtime auszurechnen)
     ![alt text](../Screenshots/timeit.png )
2. Bugfix Remove Button:
    - Programm kann jetzt ohne Probleme mehrere Male hintereinander Files aus der Tabelle
    löschen ohne abzustürzen
3. To Do:
    - Arbeitet euch in Debugging mit Hilfe von pdb ein.
    
4. Erstellt ein Widget um Konfigurationsdateien wie z.B.:
    https://github.com/OpenMS/OpenMS/blob/develop/src/tests/topp/OpenPepXLLF_
    input2.ini zu visualisieren und vom Benutzer editierbar zu machen.
    - Erstes grobe Fenster ist erstellt -> Layout muss bearbeitet werden
      ![alt text](../Screenshots/ConfigView.png )
