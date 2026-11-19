"""Figura da diferença estimada de F1 macro e seu IC bilateral."""

from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas


def gerar_figura(resultado, destino):
    estimativa = 100 * resultado["diferenca_f1_macro"]
    inferior, superior = [100 * x for x in resultado["ic95_diferenca"]]
    c = canvas.Canvas(str(destino), pagesize=(238, 80))
    c.setTitle("Diferença estimada de F1 macro")

    def x(valor):
        return 16 + valor * 3.45

    c.setStrokeColor(HexColor("#606773"))
    c.line(x(0), 29, x(60), 29)
    c.setFont("Helvetica", 8)
    for marca in range(0, 61, 10):
        c.line(x(marca), 26, x(marca), 32)
        c.drawCentredString(x(marca), 15, str(marca))
    c.drawCentredString(119, 2, "Diferença de F1 macro (p.p.)")
    c.setStrokeColor(HexColor("#174967"))
    c.setFillColor(HexColor("#174967"))
    c.setLineWidth(1.5)
    c.line(x(inferior), 49, x(superior), 49)
    for extremo in (inferior, superior):
        c.line(x(extremo), 45, x(extremo), 53)
    c.circle(x(estimativa), 49, 3.5, stroke=0, fill=1)
    c.drawCentredString(x(estimativa), 65, f"{estimativa:.1f} p.p.".replace(".", ","))
    c.save()
