import os
import sys
import subprocess
import shutil

# ==========================================
#              CONFIGURATION
# ==========================================
# Hier den Namen deiner ONNX-Datei eintragen:
# Enter the name of your ONNX file here:
#
YOUR_ONNX_FILE = "ecko.onnx"
#
# ==========================================

def convert_onnx_to_tflite(onnx_path, tflite_path):
    """
    Konvertiert ein ONNX Modell zu TFLite unter Verwendung des modernen 'onnx2tf' Tools.

    Args:
        onnx_path (str): Pfad zur .onnx Datei
        tflite_path (str): Gewünschter Pfad zur .tflite Datei
    """

    # 1. Prüfungen
    if not os.path.exists(onnx_path):
        print("--- Achtung ---")
        print("")
        print(f"Fehler: Eingabedatei '{onnx_path}' nicht gefunden!")
        print(f"Info: Lade die Datei '{onnx_path}' in den Projektordner!")
        print("")
        print("---------------")
        return

    # onnx2tf erstellt einen Ordner, keine einzelne Datei. Wir definieren diesen Ordner:
    output_folder = "saved_model_temp"

    print(f"--- Starte Konvertierung mit onnx2tf ---")
    print(f"Input File: {onnx_path}")

    # 2. Befehl für onnx2tf zusammenbauen
    # Wir rufen es als Subprozess auf, das ist stabiler als der direkte Import bei diesem Tool
    # Flags: -i (input), -o (output folder), -tfl (generate tflite directly)
    cmd = [
        sys.executable, "-m", "onnx2tf",
        "-i", onnx_path,
        "-o", output_folder
    ]

    try:
        print("Führe Konvertierung durch (das kann einen Moment dauern)...")
        # Subprozess starten
        result = subprocess.run(cmd, check=True, text=True, capture_output=True)

        # 3. Datei verschieben und aufräumen
        # onnx2tf speichert die Datei im output_folder oft als 'model_float32.tflite' oder ähnlich
        # Wir suchen die erstellte .tflite Datei
        found_tflite = None
        for file in os.listdir(output_folder):
            if file.endswith(".tflite"):
                found_tflite = os.path.join(output_folder, file)
                break

        if found_tflite:
            # Verschieben an den gewünschten Ort
            if os.path.exists(tflite_path):
                os.remove(tflite_path) # Alte Datei löschen falls vorhanden
            shutil.move(found_tflite, tflite_path)
            print(f"\n--- SUCCESS - ERFOLG! ---")
            print("")
            print(f"Deine Datei ist fertig zum Download im Projektordner bereit.")
            print(f"Dateiname: {tflite_path}")
            print("")
            print("----------------------------")
        else:
            print("Fehler: Konvertierung lief durch, aber keine .tflite Datei gefunden.")

    except subprocess.CalledProcessError as e:
        print(f"\nFehler beim Ausführen von onnx2tf. Exit code: {e.returncode}")
        print("")
        print("--- onnx2tf STDOUT ---")
        print(e.stdout)
        print("--- onnx2tf STDERR ---")
        print(e.stderr)
        print("Tipp: Hast du 'pip install onnx2tf tensorflow onnx sng4onnx ai_edge_litert' ausgeführt?")
        print("Tipp: Es müssen alle hier aufgeführten Bibilotheken installiert sein.")
        print("Tipp: Du hast nicht --  ▷ Alle ausführen -- ausgewählt.")
        print("")
        print("----------------------")
    except Exception as e:
        print(f"Unerwarteter Fehler: {e}")
    finally:
        # Aufräumen des temporären Ordners
        if os.path.exists(output_folder):
            try:
                shutil.rmtree(output_folder)
            except:
                pass

# Abrufen der Dateinamen zum setzen des Outputs
if __name__ == "__main__":
    INPUT_FILE = YOUR_ONNX_FILE
    OUTPUT_FILE = os.path.splitext(INPUT_FILE)[0] + ".tflite"

    convert_onnx_to_tflite(INPUT_FILE, OUTPUT_FILE)
