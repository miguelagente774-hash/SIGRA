import subprocess
import shutil
import os
from pathlib import Path


def pptx_to_pdf(pptx_path: str, pdf_path: str) -> None:
    """Convierte un archivo PPTX a PDF.

    Intenta en orden:
      1) PowerPoint vía pywin32 (Windows)
      2) LibreOffice (`soffice`) en PATH

    Lanza RuntimeError con información útil si falla.
    """
    pptx_path = os.path.abspath(str(pptx_path))
    pdf_path = os.path.abspath(str(pdf_path))
    outdir = str(Path(pdf_path).parent)

    if not os.path.exists(pptx_path):
        raise FileNotFoundError(f"PPTX no encontrado: {pptx_path}")

    errores = []

    # 1) PowerPoint via COM (Windows)
    if os.name == 'nt':
        try:
            from win32com import client as win32_client
            powerpoint = win32_client.Dispatch("PowerPoint.Application")
            powerpoint.Visible = 1
            # Asegurarse de usar ruta absoluta
            presentation = powerpoint.Presentations.Open(pptx_path, WithWindow=False)
            presentation.SaveAs(pdf_path, 32)  # 32 == ppSaveAsPDF
            presentation.Close()
            powerpoint.Quit()
            return
        except Exception as e:
            errores.append(f"pywin32/PowerPoint: {e}")
            # Intentar usar comtypes como alternativa a pywin32
            try:
                import comtypes.client as com_client
                ppt = com_client.CreateObject("PowerPoint.Application")
                presentation = ppt.Presentations.Open(pptx_path, WithWindow=False)
                presentation.SaveAs(pdf_path, 32)
                presentation.Close()
                ppt.Quit()
                return
            except Exception as e2:
                errores.append(f"comtypes/PowerPoint: {e2}")

    # 2) LibreOffice (soffice)
    soffice_exe = shutil.which('soffice') or shutil.which('soffice.exe')
    if soffice_exe:
        try:
            cmd = [soffice_exe, "--headless", "--convert-to", "pdf", "--outdir", outdir, pptx_path]
            subprocess.run(cmd, check=True)

            generated_name = Path(pptx_path).stem + ".pdf"
            generated_path = Path(outdir) / generated_name
            if generated_path.exists():
                shutil.move(str(generated_path), pdf_path)
                return
            else:
                errores.append("LibreOffice no generó el PDF esperado")
        except Exception as e:
            errores.append(f"soffice: {e}")
    else:
        errores.append("soffice no encontrado en PATH")

    detalle = " | ".join(errores)
    raise RuntimeError(f"No se pudo convertir PPTX a PDF. Detalles: {detalle}\nInstala LibreOffice (soffice) o pywin32 en Windows.")
