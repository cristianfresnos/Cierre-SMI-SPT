"""
Perfect Store SMI + SPT Q3 — Informe de Cierre Ejecutivo
MARS Petcare Colombia
"""

from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import pandas as pd

# ─── DIRECTORIO BASE Y CARGA DEL HTML EJECUTIVO ──────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
HTML_FILE = BASE_DIR / "index.html"

if HTML_FILE.exists():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        HTML_CONTENT = f.read()
else:
    HTML_CONTENT = ""

# ─── CONFIGURACIÓN DE PÁGINA STREAMLIT ───────────────────────────────────────
st.set_page_config(
    page_title="Perfect Store SMI + SPT Q3 — Informe de Cierre Ejecutivo",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── ESTILOS GLOBALES CORPORATIVOS (DARK SLATE) ──────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* ── Tarjetas KPI ── */
.kpi-card {
    background: rgba(30, 41, 59, 0.85);
    border: 1px solid rgba(51, 65, 85, 0.8);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 12px;
}
.kpi-card .label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: #94a3b8;
}
.kpi-card .value {
    font-size: 36px;
    font-weight: 800;
    color: #f8fafc;
    line-height: 1.1;
    margin: 6px 0;
}
.kpi-card .badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 6px;
}
.badge-red    { background: rgba(239,68,68,.15); color:#f87171; border:1px solid rgba(239,68,68,.3); }
.badge-green  { background: rgba(16,185,129,.15); color:#34d399; border:1px solid rgba(16,185,129,.3); }
.badge-amber  { background: rgba(245,158,11,.15); color:#fbbf24; border:1px solid rgba(245,158,11,.3); }
.badge-blue   { background: rgba(59,130,246,.15); color:#60a5fa; border:1px solid rgba(59,130,246,.3); }
.badge-indigo { background: rgba(99,102,241,.15); color:#a5b4fc; border:1px solid rgba(99,102,241,.3); }
.badge-purple { background: rgba(139,92,246,.15); color:#c4b5fd; border:1px solid rgba(139,92,246,.3); }

/* ── Cabeceras de Slide ── */
.slide-header {
    border-left: 4px solid;
    padding-left: 16px;
    margin-bottom: 20px;
}
.slide-header .eyebrow {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .1em;
}
.slide-header h2 {
    font-size: 28px;
    font-weight: 800;
    color: #f8fafc;
    margin: 4px 0 2px 0;
}
.slide-header p {
    font-size: 13px;
    color: #94a3b8;
}

/* ── Cajas de Información ── */
.info-box {
    background: rgba(30,41,59,.6);
    border: 1px solid rgba(51,65,85,.6);
    border-radius: 14px;
    padding: 18px 22px;
    font-size: 14px;
    color: #cbd5e1;
    line-height: 1.6;
    margin-bottom: 20px;
}

/* ── Tarjetas de Drivers ── */
.driver-card {
    background: rgba(15,23,42,.85);
    border-radius: 14px;
    padding: 20px;
    border: 1px solid rgba(51,65,85,.7);
    margin-bottom: 14px;
}

/* ── Tarjetas de Ejecutivos ── */
.exec-card {
    background: rgba(15,23,42,.9);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 14px;
    border: 1px solid rgba(51,65,85,.7);
}

/* ── Banner de Cierre ── */
.closing-banner {
    background: linear-gradient(135deg, #1e3a5f 0%, #1e1b4b 50%, #0f172a 100%);
    border: 2px solid rgba(99,102,241,.5);
    border-radius: 18px;
    padding: 36px;
    text-align: center;
}
.closing-banner h3 {
    font-size: 20px;
    font-weight: 800;
    color: #f8fafc;
    line-height: 1.5;
}

/* ── Ocultar elementos predeterminados de Streamlit para aspecto profesional ── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── TEMAS PLOTLY REUTILIZABLES ──────────────────────────────────────────────
PLOT_BG  = "rgba(0,0,0,0)"
PAPER_BG = "rgba(0,0,0,0)"
FONT_CLR = "#94a3b8"
GRID_CLR = "rgba(51,65,85,0.3)"
FONT_FAM = "Plus Jakarta Sans, sans-serif"

def base_layout(**kwargs) -> dict:
    return dict(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family=FONT_FAM, color=FONT_CLR, size=11),
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(font=dict(color=FONT_CLR, size=11), bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor=GRID_CLR, tickfont=dict(color=FONT_CLR)),
        yaxis=dict(gridcolor=GRID_CLR, tickfont=dict(color=FONT_CLR)),
        **kwargs,
    )

# ─── BARRA LATERAL (SIDEBAR) ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:18px;">
      <div style="width:44px;height:44px;border-radius:12px;
                  background:linear-gradient(135deg,#3b82f6,#6366f1);
                  display:flex;align-items:center;justify-content:center;
                  font-size:22px;font-weight:900;color:white;box-shadow:0 4px 12px rgba(59,130,246,0.3);">M</div>
      <div>
        <div style="font-weight:800;color:#f8fafc;font-size:15px;line-height:1.2;">MARS | Perfect Store</div>
        <div style="font-size:11px;color:#94a3b8;">Canal SMI + SPT | Q3</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="badge badge-green" style="font-size:12px;display:block;text-align:center;padding:6px;">🎯 Q3 Total: 53,2% (+0,7 pp vs Meet)</span>', unsafe_allow_html=True)
    st.markdown("---")

    modo_vista = st.radio(
        "Modo de Visualización:",
        [
            "🌐 Presentación Ejecutiva (HTML)",
            "📊 Dashboard Interactivo (Streamlit)"
        ],
        index=0
    )

    if modo_vista == "📊 Dashboard Interactivo (Streamlit)":
        st.markdown("---")
        slide = st.radio(
            "Navegación de Slides:",
            options=[
                "📊 1. Resultado General",
                "📉 2. Drivers y Pilares",
                "👤 3. Zoom Ejecutivos (10)",
                "🎯 4. Plan de Acción Q4",
            ],
        )

    st.markdown("---")
    if HTML_CONTENT:
        st.download_button(
            label="📥 Descargar Informe HTML",
            data=HTML_CONTENT,
            file_name="Informe_Perfect_Store_SMI_SPT_Q3.html",
            mime="text/html",
            use_container_width=True
        )

    st.caption("MARS Petcare Colombia\nInforme Perfect Store Q3 Canal SMI + SPT")


# ════════════════════════════════════════════════════════════════════════════
# MODO 1: PRESENTACIÓN EJECUTIVA COMPLETA (TAILWIND + CHART.JS)
# ════════════════════════════════════════════════════════════════════════════
if modo_vista == "🌐 Presentación Ejecutiva (HTML)":

    # Limpiar padding superior de Streamlit para experiencia inmersiva
    st.markdown("""
    <style>
        .block-container {
            padding-top: 0.5rem !important;
            padding-bottom: 1rem !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
            max-width: 100% !important;
        }
        iframe {
            width: 100% !important;
            border: none !important;
            min-height: 92vh !important;
            border-radius: 12px;
        }
    </style>
    """, unsafe_allow_html=True)

    if HTML_CONTENT:
        components.html(HTML_CONTENT, height=920, scrolling=True)
    else:
        st.error("No se encontró el archivo HTML index.html en la carpeta.")


# ════════════════════════════════════════════════════════════════════════════
# MODO 2: DASHBOARD INTERACTIVO NATIVO EN STREAMLIT
# ════════════════════════════════════════════════════════════════════════════
else:

    # DATOS MAESTROS DE EJECUTIVOS
    df_rank = pd.DataFrame({
        "Responsable MARS": [
            "Esteban Betancourt", "Yudy Loffsner", "Juan Giraldo", "Jefferson Mellizo",
            "Guillermo Arenas", "Gloria Figueroa", "Juan Carlos Contreras", "Luisa Chisco",
            "Marcela Enciso", "Laura Ariza", "TOTAL CANAL SMI+SPT"
        ],
        "Q2 (%)":     [56.4, 37.0, 47.1, 49.8, 47.4, 43.8, 48.8, 59.8, 52.4, 57.3, 51.5],
        "Meet (%)":   [57.4, 38.0, 48.1, 50.8, 48.4, 44.8, 49.8, 60.8, 53.4, 58.3, 52.5],
        "Exceed (%)": [58.4, 39.0, 49.1, 51.8, 49.4, 45.8, 50.8, 61.8, 54.4, 59.3, 53.5],
        "Q3 (%)":     [60.7, 40.3, 49.2, 51.8, 49.2, 44.9, 49.7, 59.8, 52.1, 56.2, 53.2],
        "Dif Q3-Q2":  ["+4,3 pp", "+3,3 pp", "+2,1 pp", "+2,0 pp", "+1,8 pp", "+1,2 pp", "+0,9 pp", "0,0 pp", "-0,3 pp", "-1,2 pp", "+1,7 pp"],
        "Vs Meet":    ["+3,3 pp", "+2,3 pp", "+1,1 pp", "+1,0 pp", "+0,8 pp", "+0,2 pp", "-0,1 pp", "-1,0 pp", "-1,3 pp", "-2,2 pp", "+0,7 pp"],
        "Vs Exceed":  ["+2,3 pp", "+1,3 pp", "+0,1 pp", "0,0 pp",  "-0,2 pp", "-0,8 pp", "-1,1 pp", "-2,0 pp", "-2,3 pp", "-3,2 pp", "-0,3 pp"],
    })

    # ────────────────────────────────────────────────────────────────────────
    # SLIDE 1 — RESULTADO GENERAL
    # ────────────────────────────────────────────────────────────────────────
    if slide == "📊 1. Resultado General":

        st.markdown("""
        <div class="slide-header" style="border-color:#3b82f6;">
          <div class="eyebrow" style="color:#60a5fa;">Slide 01 — Visión Ejecutiva del Canal</div>
          <h2>PERFECT STORE – RESULTADO SMI + SPT Q3</h2>
          <p>Evaluación de Cumplimiento Consolidado Q2 vs Q3 y Brechas vs Objetivos Meet (52,5%) y Exceed (53,5%)</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
          <strong style="color:#f1f5f9;">Resumen Ejecutivo:</strong> El canal combinado <strong>SMI + SPT</strong>
          culmina el tercer trimestre (Q3) alcanzando un cumplimiento del <strong>53,2%</strong>, lo que representa un sólido
          crecimiento de <strong>+1,7 puntos porcentuales</strong> respecto al Q2 (51,5%). Gracias a este dinamismo, el canal
          supera de manera positiva el objetivo <strong>Meet en +0,7 pp</strong> (52,5%), quedando a tan solo <strong>-0,3 pp de alcanzar la meta Exceed</strong>
          (53,5%). Este logro es impulsado por <strong>6 de los 10 ejecutivos de cuenta que se ubican por encima del target Meet</strong>.
        </div>
        """, unsafe_allow_html=True)

        # Tarjetas Métricas
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("""
            <div class="kpi-card">
              <div class="label">Cumplimiento Q3</div>
              <div class="value">53,2%</div>
              <div style="font-size:12px;color:#94a3b8;margin-bottom:8px;">vs 51,5% (Q2)</div>
              <span class="badge badge-green">🚀 Crecimiento: +1,7 pp</span>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown("""
            <div class="kpi-card">
              <div class="label">Objetivo MEET CANAL</div>
              <div class="value" style="color:#818cf8;">52,5%</div>
              <div style="font-size:12px;color:#94a3b8;margin-bottom:8px;">Umbral Base de Desempeño</div>
              <span class="badge badge-green">🎯 Estado: Superado (+0,7 pp)</span>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown("""
            <div class="kpi-card">
              <div class="label">Objetivo EXCEED CANAL</div>
              <div class="value" style="color:#c084fc;">53,5%</div>
              <div style="font-size:12px;color:#94a3b8;margin-bottom:8px;">Umbral de Excelencia</div>
              <span class="badge badge-amber">📍 Brecha Breve: -0,3 pp</span>
            </div>
            """, unsafe_allow_html=True)

        with c4:
            st.markdown("""
            <div class="kpi-card">
              <div class="label">Efectividad del Equipo</div>
              <div class="value" style="color:#34d399;font-size:32px;">60%</div>
              <div style="font-size:12px;color:#cbd5e1;line-height:1.4;">6 de 10 ejecutivos sobre la meta Meet. Foco en recuperar los 4 restantes.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        col_tbl, col_cht = st.columns([7, 5])

        with col_tbl:
            st.markdown("#### 🏅 Tabla General de Ejecutivos Mars")
            st.caption("Ordenado por Crecimiento Q3 vs Q2")

            def color_format(val):
                if isinstance(val, str):
                    if val.startswith("+"):
                        return "color: #34d399; font-weight:700"
                    elif val.startswith("-"):
                        return "color: #f87171; font-weight:700"
                return ""

            styled_df = df_rank.style.applymap(color_format, subset=["Dif Q3-Q2", "Vs Meet", "Vs Exceed"])
            st.dataframe(styled_df, use_container_width=True, hide_index=True)

            h1, h2, h3 = st.columns(3)
            with h1:
                st.markdown('<div style="background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.3);border-radius:10px;padding:10px;"><span style="font-size:11px;font-weight:700;color:#34d399;">🏆 Mayor Crecimiento</span><br><strong style="color:#f8fafc;">Esteban — +4,3 pp</strong></div>', unsafe_allow_html=True)
            with h2:
                st.markdown('<div style="background:rgba(59,130,246,.1);border:1px solid rgba(59,130,246,.3);border-radius:10px;padding:10px;"><span style="font-size:11px;font-weight:700;color:#60a5fa;">🚀 Crecimiento Clave</span><br><strong style="color:#f8fafc;">Yudy — +3,3 pp</strong></div>', unsafe_allow_html=True)
            with h3:
                st.markdown('<div style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:10px;padding:10px;"><span style="font-size:11px;font-weight:700;color:#f87171;">🚨 Brecha Más Amplia</span><br><strong style="color:#f8fafc;">Laura — -2,2 pp vs Meet</strong></div>', unsafe_allow_html=True)

        with col_cht:
            st.markdown("#### 📊 Desempeño Q3 vs Objetivos Individuales")
            st.caption("Barras: Resultado Q3 | Línea punteada: Target Meet individual")

            exec_names_10 = [
                "Esteban B.", "Yudy L.", "Juan G.", "Jefferson M.",
                "Guillermo A.", "Gloria F.", "Juan C. C.", "Luisa C.",
                "Marcela E.", "Laura A."
            ]
            q3_vals_10 = [60.7, 40.3, 49.2, 51.8, 49.2, 44.9, 49.7, 59.8, 52.1, 56.2]
            meet_vals_10 = [57.4, 38.0, 48.1, 50.8, 48.4, 44.8, 49.8, 60.8, 53.4, 58.3]
            colors_10 = [
                "#10b981", "#10b981", "#10b981", "#10b981", "#10b981", "#10b981",
                "#f59e0b", "#ef4444", "#ef4444", "#ef4444"
            ]

            hover_tooltips = [
                "<b>ESTEBAN BETANCOURT</b><br>"
                "📦 Dif. Surtido (Q3 vs Q2): <b>+0,1 %</b><br>"
                "👁️ Dif. Visibilidad (Q3 vs Q2): <b>-0,3 %</b><br>"
                "🏷️ Dif. Exhibición (Q3 vs Q2): <b>+2,6 %</b><br>"
                "🎯 Dif. Perfect Store (Q3 vs Q2): <b>+4,3 %</b><extra></extra>",

                "<b>YUDY LOFFSNER</b><br>"
                "📦 Dif. Surtido (Q3 vs Q2): <b>+2,3 %</b><br>"
                "👁️ Dif. Visibilidad (Q3 vs Q2): <b>+1,2 %</b><br>"
                "🏷️ Dif. Exhibición (Q3 vs Q2): <b>0,0 %</b><br>"
                "🎯 Dif. Perfect Store (Q3 vs Q2): <b>+3,3 %</b><extra></extra>",

                "<b>JUAN GIRALDO</b><br>"
                "📦 Dif. Surtido (Q3 vs Q2): <b>+1,5 %</b><br>"
                "👁️ Dif. Visibilidad (Q3 vs Q2): <b>+0,5 %</b><br>"
                "🏷️ Dif. Exhibición (Q3 vs Q2): <b>+0,2 %</b><br>"
                "🎯 Dif. Perfect Store (Q3 vs Q2): <b>+2,1 %</b><extra></extra>",

                "<b>JEFFERSON MELLIZO</b><br>"
                "📦 Dif. Surtido (Q3 vs Q2): <b>+1,6 %</b><br>"
                "👁️ Dif. Visibilidad (Q3 vs Q2): <b>+1,0 %</b><br>"
                "🏷️ Dif. Exhibición (Q3 vs Q2): <b>-0,4 %</b><br>"
                "🎯 Dif. Perfect Store (Q3 vs Q2): <b>+2,0 %</b><extra></extra>",

                "<b>GUILLERMO ARENAS</b><br>"
                "📦 Dif. Surtido (Q3 vs Q2): <b>+1,4 %</b><br>"
                "👁️ Dif. Visibilidad (Q3 vs Q2): <b>+0,2 %</b><br>"
                "🏷️ Dif. Exhibición (Q3 vs Q2): <b>+0,3 %</b><br>"
                "🎯 Dif. Perfect Store (Q3 vs Q2): <b>+1,8 %</b><extra></extra>",

                "<b>GLORIA FIGUEROA</b><br>"
                "📦 Dif. Surtido (Q3 vs Q2): <b>+1,7 %</b><br>"
                "👁️ Dif. Visibilidad (Q3 vs Q2): <b>+0,8 %</b><br>"
                "🏷️ Dif. Exhibición (Q3 vs Q2): <b>-0,8 %</b><br>"
                "🎯 Dif. Perfect Store (Q3 vs Q2): <b>+1,2 %</b><extra></extra>",

                "<b>JUAN CARLOS CONTRERAS</b><br>"
                "📦 Dif. Surtido (Q3 vs Q2): <b>-0,4 %</b><br>"
                "👁️ Dif. Visibilidad (Q3 vs Q2): <b>+0,5 %</b><br>"
                "🏷️ Dif. Exhibición (Q3 vs Q2): <b>+0,8 %</b><br>"
                "🎯 Dif. Perfect Store (Q3 vs Q2): <b>+0,9 %</b><extra></extra>",

                "<b>LUISA CHISCO</b><br>"
                "📦 Dif. Surtido (Q3 vs Q2): <b>+1,2 %</b><br>"
                "👁️ Dif. Visibilidad (Q3 vs Q2): <b>+0,2 %</b><br>"
                "🏷️ Dif. Exhibición (Q3 vs Q2): <b>-1,3 %</b><br>"
                "🎯 Dif. Perfect Store (Q3 vs Q2): <b>-0,0 %</b><extra></extra>",

                "<b>MARCELA ENCISO</b><br>"
                "📦 Dif. Surtido (Q3 vs Q2): <b>-1,5 %</b><br>"
                "👁️ Dif. Visibilidad (Q3 vs Q2): <b>0,0 %</b><br>"
                "🏷️ Dif. Exhibición (Q3 vs Q2): <b>+1,2 %</b><br>"
                "🎯 Dif. Perfect Store (Q3 vs Q2): <b>-0,3 %</b><extra></extra>",

                "<b>LAURA ARIZA</b><br>"
                "📦 Dif. Surtido (Q3 vs Q2): <b>-1,1 %</b><br>"
                "👁️ Dif. Visibilidad (Q3 vs Q2): <b>-0,5 %</b><br>"
                "🏷️ Dif. Exhibición (Q3 vs Q2): <b>+0,4 %</b><br>"
                "🎯 Dif. Perfect Store (Q3 vs Q2): <b>-1,2 %</b><extra></extra>",
            ]

            fig_s1 = go.Figure()
            fig_s1.add_trace(go.Bar(
                name="Resultado Q3 (%)",
                x=exec_names_10, y=q3_vals_10,
                marker_color=colors_10,
                marker_line_width=0,
                text=[f"{v:.1f}%" for v in q3_vals_10],
                textposition="outside",
                textfont=dict(color="#f8fafc", size=10, family=FONT_FAM),
                hovertemplate=hover_tooltips,
            ))
            fig_s1.add_trace(go.Scatter(
                name="Target Meet Individual",
                x=exec_names_10, y=meet_vals_10,
                mode="lines+markers",
                line=dict(color="#8b5cf6", width=2, dash="dash"),
                marker=dict(color="#8b5cf6", size=6),
                hovertemplate="🎯 Target Meet Individual: <b>%{y:.1f}%</b><extra></extra>",
            ))
            fig_s1.update_layout(
                **base_layout(yaxis=dict(range=[30, 68], gridcolor=GRID_CLR, tickfont=dict(color=FONT_CLR))),
                height=340,
            )
            st.plotly_chart(fig_s1, use_container_width=True)

            st.markdown("""
            <div style="background:rgba(15,23,42,.8);border:1px solid rgba(51,65,85,.8);border-radius:10px;
                        padding:12px;font-size:12px;color:#cbd5e1;margin-top:8px;">
              <strong style="color:#f8fafc;">Análisis de la Gráfica:</strong> Esteban (+3,3 pp vs Meet) y Yudy (+2,3 pp vs Meet)
              encabezan el sobrecumplimiento. Juan Giraldo, Jefferson, Guillermo y Gloria completan el grupo en verde.
              Laura (-2,2 pp vs Meet) y Marcela (-1,3 pp) presentan las mayores brechas por cerrar.
            </div>
            """, unsafe_allow_html=True)

    # ────────────────────────────────────────────────────────────────────────
    # SLIDE 2 — DRIVERS Y PILARES TÁCTICOS
    # ────────────────────────────────────────────────────────────────────────
    elif slide == "📉 2. Drivers y Pilares":

        st.markdown("""
        <div class="slide-header" style="border-color:#f59e0b;">
          <div class="eyebrow" style="color:#fbbf24;">Slide 02 — Diagnóstico por Indicadores</div>
          <h2>DRIVERS DEL RESULTADO SMI + SPT</h2>
          <p>Análisis táctico por KPIs: Surtido, Visibilidad y Exhibición Secundaria en canales especializados</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
          <strong style="color:#f1f5f9;">Análisis Operativo:</strong> El avance de <strong>+1,7 pp en el consolidado del canal</strong>
          es impulsado de manera equilibrada por el crecimiento del KPI de <strong>Surtido (acelerado por tecnologías Wet y C&T en Perro y Gato)</strong>
          y por la expansión en <strong>Exhibición Secundaria en Pet Shops Tradicionales y Cadenas</strong>. La Visibilidad se mantiene como un ancla de
          estabilidad, aunque con oportunidades latentes en el sub-KPI de Bloque de Marca.
        </div>
        """, unsafe_allow_html=True)

        # 3 Driver Cards
        d1, d2, d3 = st.columns(3)

        with d1:
            st.markdown("""
            <div class="driver-card" style="border:1px solid rgba(16,185,129,.4);">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <span class="badge badge-green">Motor Principal</span>
                <span style="font-size:11px;color:#94a3b8;">KPI Surtido</span>
              </div>
              <div style="display:flex;justify-content:space-between;align-items:baseline;">
                <div style="font-size:26px;font-weight:800;color:#f8fafc;">SURTIDO</div>
                <div style="font-size:20px;font-weight:900;color:#34d399;">+1,5 pp</div>
              </div>
              <hr style="border-color:rgba(51,65,85,.6);margin:14px 0;">
              <div style="font-size:12px;color:#cbd5e1;space-y:6px;">
                ✔ <strong>Juan Giraldo:</strong> Crecimiento en Gato C&T (+4,5%) y Perro C&T (+7,1%).<br><br>
                ✔ <strong>Jefferson Mellizo:</strong> Cadena crece +2,4% impulsado por Perro C&T (+8,0%).<br><br>
                ✖ <strong>Laura Ariza:</strong> Caída en Centro (-2,0%) en Makro (Gato Dry -14,6%).
              </div>
            </div>
            """, unsafe_allow_html=True)

        with d2:
            st.markdown("""
            <div class="driver-card" style="border:1px solid rgba(6,182,212,.4);">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <span class="badge badge-blue">Ancla de Estabilidad</span>
                <span style="font-size:11px;color:#94a3b8;">KPI Visibilidad</span>
              </div>
              <div style="display:flex;justify-content:space-between;align-items:baseline;">
                <div style="font-size:26px;font-weight:800;color:#f8fafc;">VISIBILIDAD</div>
                <div style="font-size:20px;font-weight:900;color:#60a5fa;">+0,2 pp</div>
              </div>
              <hr style="border-color:rgba(51,65,85,.6);margin:14px 0;">
              <div style="font-size:12px;color:#cbd5e1;space-y:6px;">
                ✔ <strong>Yudy Loffsner:</strong> Crecimiento +1,2% por mayor participación en góndola.<br><br>
                ✔ <strong>Guillermo Arenas:</strong> Crecimiento +2,2% en Pet Shop Cadena.<br><br>
                ⚠️ <strong>Juan Carlos / Esteban:</strong> Desafíos en Bloque de Marca en Centro.
              </div>
            </div>
            """, unsafe_allow_html=True)

        with d3:
            st.markdown("""
            <div class="driver-card" style="border:1px solid rgba(139,92,246,.4);">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <span class="badge badge-purple">Palanca Aceleración</span>
                <span style="font-size:11px;color:#94a3b8;">KPI Exhibición Sec.</span>
              </div>
              <div style="display:flex;justify-content:space-between;align-items:baseline;">
                <div style="font-size:24px;font-weight:800;color:#f8fafc;">EXHIBICIÓN SEC.</div>
                <div style="font-size:20px;font-weight:900;color:#c4b5fd;">+1,2 pp</div>
              </div>
              <hr style="border-color:rgba(51,65,85,.6);margin:14px 0;">
              <div style="font-size:12px;color:#cbd5e1;space-y:6px;">
                🚀 <strong>Esteban Betancourt:</strong> Crecimiento masivo +3,1% (Tradicional Centro +4,5%).<br><br>
                🚀 <strong>Marcela Enciso:</strong> Crecimiento +1,2% por bomboneras y puestos de pago.<br><br>
                ✖ <strong>Luisa / Gloria:</strong> Caídas en Tradicional por baja de wet solutions y bomboneras.
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        col_dr_cht, col_opp = st.columns([7, 5])

        with col_dr_cht:
            st.markdown("#### 📊 Crecimiento por Ejecutivo (Variación Q3 vs Q2)")
            st.caption("Variación en puntos porcentuales registrada por responsable")

            exec_labels = [
                "Esteban B.", "Yudy L.", "Juan G.", "Jefferson M.",
                "Guillermo A.", "Gloria F.", "Juan C. C.", "Luisa C.",
                "Marcela E.", "Laura A."
            ]
            diff_vals = [4.3, 3.3, 2.1, 2.0, 1.8, 1.2, 0.9, 0.0, -0.3, -1.2]
            diff_colors = ["#10b981" if v > 0 else ("#94a3b8" if v == 0 else "#ef4444") for v in diff_vals]

            fig_s2 = go.Figure()
            fig_s2.add_trace(go.Bar(
                name="Variación (pp)",
                x=exec_labels, y=diff_vals,
                marker_color=diff_colors,
                marker_line_width=0,
                text=[f"+{v:.1f} pp" if v > 0 else f"{v:.1f} pp" for v in diff_vals],
                textposition="outside",
                textfont=dict(color="#f8fafc", size=10, family=FONT_FAM),
            ))
            fig_s2.update_layout(
                **base_layout(yaxis=dict(range=[-2, 5.5], gridcolor=GRID_CLR, tickfont=dict(color=FONT_CLR))),
                height=340,
            )
            st.plotly_chart(fig_s2, use_container_width=True)

        with col_opp:
            st.markdown("""
            <div style="background:linear-gradient(135deg,rgba(30,27,75,.8),rgba(15,23,42,.9));
                        border:1px solid rgba(99,102,241,.4);border-radius:16px;padding:22px;height:100%;">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
                <span style="width:10px;height:10px;background:#818cf8;border-radius:50%;display:inline-block;"></span>
                <span style="color:#a5b4fc;font-weight:700;font-size:12px;">OPORTUNIDAD CLAVE DE CANAL</span>
              </div>
              <h4 style="font-size:20px;font-weight:800;color:#f8fafc;margin-bottom:10px;">Elementos de Exhibición al 0%</h4>
              <p style="font-size:12px;color:#cbd5e1;line-height:1.6;margin-bottom:14px;">
                A pesar de los avances, varias cuentas registran ejecuciones nulas (&lt; 2%) en elementos de alta conversión:
              </p>
              <ul style="font-size:12px;color:#cbd5e1;line-height:1.9;padding-left:16px;margin-bottom:16px;">
                <li><strong>Juan Giraldo:</strong> Balconeras, puestos de pago y lateral rejilla con &lt; 2% de presencia.</li>
                <li><strong>Laura Ariza (Homecenter Occidente):</strong> Botaderos, puntas de góndola y balconeras al 0%.</li>
                <li><strong>Guillermo Arenas:</strong> Arrumes en Pet Shop Tradicional con 0% de implementación.</li>
              </ul>
              <div style="background:rgba(99,102,241,.15);border:1px solid rgba(99,102,241,.3);border-radius:10px;
                          padding:12px;font-size:12px;color:#c4b5fd;">
                <strong>Estrategia de Captura:</strong> Desbloquear estos elementos generará el impulso requerido
                para que los 4 ejecutivos con brecha alcancen el Meet en Q4.
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ────────────────────────────────────────────────────────────────────────
    # SLIDE 3 — ZOOM DETALLADO POR EJECUTIVO
    # ────────────────────────────────────────────────────────────────────────
    elif slide == "👤 3. Zoom Ejecutivos (10)":

        st.markdown("""
        <div class="slide-header" style="border-color:#6366f1;">
          <div class="eyebrow" style="color:#a5b4fc;">Slide 03 — Zoom Operativo e Interactivo</div>
          <h2>ANÁLISIS DETALLADO POR EJECUTIVO MARS</h2>
          <p>Selecciona cualquier ejecutivo para desplegar la causa raíz, variación por cadenas, regionales y tecnologías</p>
        </div>
        """, unsafe_allow_html=True)

        exec_opciones = [
            "📊 Vista Consolidada",
            "🔴 Laura Ariza (56,2% | -2,2 pp)",
            "🔴 Marcela Enciso (52,1% | -1,3 pp)",
            "🔴 Luisa Chisco (59,8% | -1,0 pp)",
            "🟠 Juan Carlos Contreras (49,7% | -0,1 pp)",
            "🟢 Esteban Betancourt (60,7% | +3,3 pp)",
            "🟢 Yudy Loffsner (40,3% | +2,3 pp)",
            "🟢 Juan Giraldo (49,2% | +1,1 pp)",
            "🟢 Jefferson Mellizo (51,8% | +1,0 pp)",
            "🟢 Guillermo Arenas (49,2% | +0,8 pp)",
            "🟢 Gloria Figueroa (44,9% | +0,2 pp)",
        ]

        seleccion_exec = st.selectbox("Seleccione Ejecutivo para el Diagnóstico:", exec_opciones, index=0)

        # ── VISTA CONSOLIDADA ──
        if seleccion_exec == "📊 Vista Consolidada":
            st.markdown("#### 📋 Resumen Rápido por Responsable")
            cols_r1 = st.columns(3)
            with cols_r1[0]:
                st.markdown("""
                <div class="exec-card" style="border-top:4px solid #ef4444;">
                  <div style="font-weight:800;color:#f8fafc;font-size:16px;">🔴 LAURA ARIZA</div>
                  <div style="font-size:24px;font-weight:900;color:#f87171;margin:6px 0;">56,2% <span style="font-size:12px;color:#cbd5e1;">(-2,2 vs Meet)</span></div>
                  <p style="font-size:12px;color:#94a3b8;">Caída en Surtido (-1,1%), liderada por Regional Centro (-2,0%) en Makro (Gato Dry -14,6%) y Zapatoca.</p>
                </div>
                """, unsafe_allow_html=True)
            with cols_r1[1]:
                st.markdown("""
                <div class="exec-card" style="border-top:4px solid #ef4444;">
                  <div style="font-weight:800;color:#f8fafc;font-size:16px;">🔴 MARCELA ENCISO</div>
                  <div style="font-size:24px;font-weight:900;color:#f87171;margin:6px 0;">52,1% <span style="font-size:12px;color:#cbd5e1;">(-1,3 vs Meet)</span></div>
                  <p style="font-size:12px;color:#94a3b8;">Surtido cae -1,5% por Perro (-2,3%: C&T -2,6%, Wet -1,8%). Exhibición atenúa con +1,2%.</p>
                </div>
                """, unsafe_allow_html=True)
            with cols_r1[2]:
                st.markdown("""
                <div class="exec-card" style="border-top:4px solid #ef4444;">
                  <div style="font-weight:800;color:#f8fafc;font-size:16px;">🔴 LUISA CHISCO</div>
                  <div style="font-size:24px;font-weight:900;color:#f87171;margin:6px 0;">59,8% <span style="font-size:12px;color:#cbd5e1;">(-1,0 vs Meet)</span></div>
                  <p style="font-size:12px;color:#94a3b8;">Plano (0,0%). Caída en Exhibición (-1,3%) en Pet Shop Tradicional por retiro de bomboneras y puestos de pago.</p>
                </div>
                """, unsafe_allow_html=True)

            cols_r2 = st.columns(3)
            with cols_r2[0]:
                st.markdown("""
                <div class="exec-card" style="border-top:4px solid #f59e0b;">
                  <div style="font-weight:800;color:#f8fafc;font-size:16px;">🟠 JUAN CARLOS CONTRERAS</div>
                  <div style="font-size:24px;font-weight:900;color:#fbbf24;margin:6px 0;">49,7% <span style="font-size:12px;color:#cbd5e1;">(-0,1 vs Meet)</span></div>
                  <p style="font-size:12px;color:#94a3b8;">A solo 0,1 pp del Meet. Caída en Supermercados Boom y EPM por Gato Dry (-1,8%). Visibilidad suma +0,5%.</p>
                </div>
                """, unsafe_allow_html=True)
            with cols_r2[1]:
                st.markdown("""
                <div class="exec-card" style="border-top:4px solid #10b981;">
                  <div style="font-weight:800;color:#f8fafc;font-size:16px;">🟢 ESTEBAN BETANCOURT</div>
                  <div style="font-size:24px;font-weight:900;color:#34d399;margin:6px 0;">60,7% <span style="font-size:12px;color:#cbd5e1;">(+3,3 vs Meet)</span></div>
                  <p style="font-size:12px;color:#94a3b8;">Líder de crecimiento (+4,3 pp) por Exhibición Secundaria (+3,1%) en Tradicional Centro (+4,5%).</p>
                </div>
                """, unsafe_allow_html=True)
            with cols_r2[2]:
                st.markdown("""
                <div class="exec-card" style="border-top:4px solid #10b981;">
                  <div style="font-weight:800;color:#f8fafc;font-size:16px;">🟢 YUDY LOFFSNER</div>
                  <div style="font-size:24px;font-weight:900;color:#34d399;margin:6px 0;">40,3% <span style="font-size:12px;color:#cbd5e1;">(+2,3 vs Meet)</span></div>
                  <p style="font-size:12px;color:#94a3b8;">Crecimiento de +3,3 pp impulsado por Surtido en Independientes (+2,1%) y Visibilidad (+1,2%).</p>
                </div>
                """, unsafe_allow_html=True)

        # ── DETALLE LAURA ARIZA ──
        elif "Laura Ariza" in seleccion_exec:
            st.markdown("""
            <div class="exec-card" style="border:2px solid rgba(239,68,68,.5);">
              <span class="badge badge-red">🔴 FOCO PRINCIPAL DE RECUPERACIÓN</span>
              <h3 style="font-size:28px;font-weight:800;color:#f8fafc;margin:8px 0 2px;">LAURA ARIZA</h3>
              <p style="font-size:12px;color:#94a3b8;">Cadenas Especializadas SMI/SPT (Makro, Zapatoca, Homecenter, Alkosto)</p>
              <div style="display:flex;gap:20px;margin-top:10px;font-size:13px;">
                <span>Q3: <strong style="color:#f87171;font-size:18px;">56,2%</strong></span>
                <span>vs Q2: <strong style="color:#f87171;">-1,2 pp</strong></span>
                <span>vs Meet (58,3%): <strong style="color:#f87171;">-2,2 pp</strong></span>
                <span>vs Exceed (59,3%): <strong style="color:#f87171;">-3,2 pp</strong></span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            k1, k2, k3 = st.columns(3)
            with k1:
                st.markdown("""
                <div class="driver-card" style="border:1px solid rgba(239,68,68,.4);">
                  <strong style="color:#f87171;font-size:13px;">1. SURTIDO (-1,1% TOTAL)</strong>
                  <p style="font-size:12px;color:#cbd5e1;margin-top:6px;">
                    <strong>Caídas Regionales:</strong> Centro (-2,0%), Occidente (-1,7%), Oriente (-1,6%), Costa (-0,4%). Crecen Antioquia (+1,1%) y Eje Cafetero (+3,1%).
                  </p>
                  <div style="background:rgba(15,23,42,.7);padding:8px;border-radius:8px;font-size:11px;color:#cbd5e1;line-height:1.6;">
                    • Makro Centro: <strong style="color:#f87171;">-3,1%</strong><br>
                    • Zapatoca Centro: <strong style="color:#f87171;">-2,4%</strong><br>
                    • Homecenter Centro: <strong style="color:#f87171;">-1,7%</strong><br>
                    • Alkosto Centro: <strong style="color:#f87171;">-1,1%</strong>
                  </div>
                  <p style="font-size:11px;color:#fbbf24;margin-top:6px;">Makro: Gato Dry cae drásticamente -14,6%. En Perro caen las 3 tecnologías.</p>
                </div>
                """, unsafe_allow_html=True)

            with k2:
                st.markdown("""
                <div class="driver-card">
                  <strong style="color:#fbbf24;font-size:13px;">2. VISIBILIDAD (-0,5% TOTAL)</strong>
                  <p style="font-size:12px;color:#cbd5e1;margin-top:6px;">
                    Caídas moderadas &lt;0,9% en casi todas las regiones. La mayor afectación se concentra en <strong>Makro (-1,5%)</strong>.
                  </p>
                  <div style="background:rgba(15,23,42,.7);padding:8px;border-radius:8px;font-size:11px;color:#cbd5e1;line-height:1.6;">
                    • Makro Occidente: <strong style="color:#f87171;">-3,5%</strong><br>
                    • Makro Oriente: <strong style="color:#f87171;">-2,4%</strong>
                  </div>
                  <p style="font-size:11px;color:#94a3b8;margin-top:6px;">Explicado por pérdida de participación en anaquel.</p>
                </div>
                """, unsafe_allow_html=True)

            with k3:
                st.markdown("""
                <div class="driver-card">
                  <strong style="color:#c4b5fd;font-size:13px;">3. EXHIBICIÓN SEC. (+0,4% TOTAL)</strong>
                  <p style="font-size:12px;color:#cbd5e1;margin-top:6px;">
                    Aportan Antioquia (+1,9%: Homecenter +1,7%, Makro +2,3%) y Costa (+1,1%).
                  </p>
                  <div style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);padding:8px;border-radius:8px;font-size:11px;color:#fca5a5;">
                    🚨 <strong>Homecenter Occidente (-3,5%):</strong> Botaderos, puntas de góndola y balconeras tienen <strong>0% de implementación</strong>.
                  </div>
                </div>
                """, unsafe_allow_html=True)

        # ── DETALLE MARCELA ENCISO ──
        elif "Marcela Enciso" in seleccion_exec:
            st.markdown("""
            <div class="exec-card" style="border:2px solid rgba(239,68,68,.5);">
              <span class="badge badge-red">🔴 DIAGNÓSTICO DE RECUPERACIÓN</span>
              <h3 style="font-size:28px;font-weight:800;color:#f8fafc;margin:8px 0 2px;">MARCELA ENCISO</h3>
              <p style="font-size:12px;color:#94a3b8;">SMI + SPT Regional</p>
              <div style="display:flex;gap:20px;margin-top:10px;font-size:13px;">
                <span>Q3: <strong style="color:#f87171;font-size:18px;">52,1%</strong></span>
                <span>vs Q2: <strong style="color:#f87171;">-0,3 pp</strong></span>
                <span>vs Meet (53,4%): <strong style="color:#f87171;">-1,3 pp</strong></span>
                <span>vs Exceed (54,4%): <strong style="color:#f87171;">-2,3 pp</strong></span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            m1, m2 = st.columns(2)
            with m1:
                st.markdown("""
                <div class="driver-card" style="border:1px solid rgba(239,68,68,.4);">
                  <strong style="color:#f87171;font-size:13px;">1. SURTIDO (-1,5% - Causa Principal)</strong>
                  <p style="font-size:12px;color:#cbd5e1;margin-top:6px;">La contracción se concentra en la categoría <strong>Perro (-2,3%)</strong>:</p>
                  <ul style="font-size:12px;color:#cbd5e1;line-height:1.8;">
                    <li>Perro C&T: <strong style="color:#f87171;">-2,6%</strong></li>
                    <li>Perro Wet: <strong style="color:#f87171;">-1,8%</strong></li>
                    <li>Gato Wet: <strong style="color:#f87171;">-2,1%</strong></li>
                    <li>Gato C&T: <strong style="color:#34d399;">+1,4%</strong> (mitiga parcialmente)</li>
                  </ul>
                </div>
                """, unsafe_allow_html=True)

            with m2:
                st.markdown("""
                <div class="driver-card" style="border:1px solid rgba(16,185,129,.4);">
                  <strong style="color:#34d399;font-size:13px;">2. EXHIBICIÓN SECUNDARIA (+1,2%)</strong>
                  <p style="font-size:12px;color:#cbd5e1;margin-top:6px;">Excelente gestión de ejecuciones en mostrador y cajas que sostuvieron el indicador general.</p>
                  <div style="background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.3);padding:10px;border-radius:8px;font-size:12px;color:#a7f3d0;margin-top:8px;">
                    <strong>Éxito Táctico:</strong> Mayor presencia de bomboneras y puestos de pago. Reponer catálogo de Perro para alcanzar el Meet (53,4%).
                  </div>
                </div>
                """, unsafe_allow_html=True)

        # ── DETALLE ESTEBAN BETANCOURT ──
        elif "Esteban Betancourt" in seleccion_exec:
            st.markdown("""
            <div class="exec-card" style="border:2px solid rgba(16,185,129,.5);">
              <span class="badge badge-green">🏆 LÍDER DE CRECIMIENTO (+4,3 pp)</span>
              <h3 style="font-size:28px;font-weight:800;color:#f8fafc;margin:8px 0 2px;">ESTEBAN BETANCOURT</h3>
              <p style="font-size:12px;color:#94a3b8;">Regional Centro y Antioquia (Pet Shop Tradicional y Cadenas)</p>
              <div style="display:flex;gap:20px;margin-top:10px;font-size:13px;">
                <span>Q3: <strong style="color:#34d399;font-size:18px;">60,7%</strong></span>
                <span>vs Q2: <strong style="color:#34d399;">+4,3 pp</strong></span>
                <span>vs Meet (57,4%): <strong style="color:#34d399;">+3,3 pp 🎯</strong></span>
                <span>vs Exceed (58,4%): <strong style="color:#34d399;">+2,3 pp 🏆</strong></span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            e1, e2, e3 = st.columns(3)
            with e1:
                st.markdown("""
                <div class="driver-card">
                  <strong style="color:#94a3b8;font-size:13px;">1. SURTIDO (+0,1% PLANO)</strong>
                  <p style="font-size:12px;color:#cbd5e1;margin-top:6px;">
                    Resiliente. Pequeña contracción en Wet Perro tanto en Regional Centro como en Antioquia.
                  </p>
                </div>
                """, unsafe_allow_html=True)
            with e2:
                st.markdown("""
                <div class="driver-card">
                  <strong style="color:#fbbf24;font-size:13px;">2. VISIBILIDAD (-0,3%)</strong>
                  <p style="font-size:12px;color:#cbd5e1;margin-top:6px;">
                    Caída menor en Centro provocada por desalineación puntual en Bloque de Marca.
                  </p>
                </div>
                """, unsafe_allow_html=True)
            with e3:
                st.markdown("""
                <div class="driver-card" style="border:1px solid rgba(16,185,129,.4);">
                  <strong style="color:#34d399;font-size:13px;">3. EXHIBICIÓN SEC. (+3,1% GRAN MOTOR) 🚀</strong>
                  <p style="font-size:12px;color:#cbd5e1;margin-top:6px;">
                    <strong>Tradicional Centro (+4,5%):</strong> Despliegue masivo de ristras, puestos de pago y arrumes. En Cadenas también crecen ristras y cajas.
                  </p>
                  <p style="font-size:11px;color:#fbbf24;">Antioquia registra caída de -2,4%.</p>
                </div>
                """, unsafe_allow_html=True)

        # ── DETALLE GENERAL PARA OTROS EJECUTIVOS ──
        else:
            nombre = seleccion_exec.split("(")[0].strip()[2:]
            fila = df_rank[df_rank["Responsable MARS"].str.contains(nombre[:8], na=False)]

            if not fila.empty:
                f = fila.iloc[0]
                color = "#34d399" if "+" in str(f["Vs Meet"]) else "#f87171"
                badge = "badge-green" if "+" in str(f["Vs Meet"]) else "badge-red"

                st.markdown(f"""
                <div class="exec-card" style="border:2px solid {color}88;">
                  <span class="badge {badge}">FICHA DETALLADA</span>
                  <h3 style="font-size:28px;font-weight:800;color:#f8fafc;margin:8px 0 2px;">{f['Responsable MARS'].upper()}</h3>
                  <div style="display:flex;gap:20px;margin-top:10px;font-size:13px;">
                    <span>Q3: <strong style="color:{color};font-size:18px;">{f['Q3 (%)']:.1f}%</strong></span>
                    <span>vs Q2: <strong>{f['Dif Q3-Q2']}</strong></span>
                    <span>vs Meet ({f['Meet (%)']:.1f}%): <strong style="color:{color};">{f['Vs Meet']}</strong></span>
                    <span>vs Exceed ({f['Exceed (%)']:.1f}%): <strong>{f['Vs Exceed']}</strong></span>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            st.info("Para ver el análisis interactivo completo con todas las pestañas y sub-diagnósticos, cambia a la opción '🌐 Presentación Ejecutiva (HTML)' en la barra lateral.")

    # ────────────────────────────────────────────────────────────────────────
    # SLIDE 4 — PLAN DE ACCIÓN Y CIERRE Q4
    # ────────────────────────────────────────────────────────────────────────
    elif slide == "🎯 4. Plan de Acción Q4":

        st.markdown("""
        <div class="slide-header" style="border-color:#10b981;">
          <div class="eyebrow" style="color:#34d399;">Slide 04 — Estrategia de Cierre Q4</div>
          <h2>PLAN DE ACCIÓN – CANAL SMI + SPT</h2>
          <p>4 pilares estratégicos para cerrar los -0,3 pp restantes y alcanzar la meta Exceed a nivel canal</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
          <strong style="color:#f1f5f9;">Ruta Táctica para Q4:</strong> Con el canal posicionado en <strong>53,2% (+0,7 pp sobre Meet)</strong>,
          el objetivo inmediato para el cierre de año es capturar los <strong>0,3 pp requeridos para alcanzar el umbral Exceed (53,5%)</strong>.
          Esto se logrará mediante la ejecución de cuatro planes de choque directos focalizados en los ejecutivos con brechas abiertas.
        </div>
        """, unsafe_allow_html=True)

        p1, p2 = st.columns(2)

        with p1:
            st.markdown("""
            <div style="background:rgba(30,41,59,.9);border-left:4px solid #ef4444;border-radius:0 14px 14px 0;padding:22px;margin-bottom:16px;">
              <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
                <span style="width:36px;height:36px;border-radius:10px;background:rgba(239,68,68,.2);
                             display:flex;align-items:center;justify-content:center;font-weight:900;color:#f87171;">1</span>
                <div>
                  <div style="font-weight:800;color:#f8fafc;font-size:15px;">PLAN DE CHOQUE CENTRO Y MAKRO</div>
                  <div style="font-size:11px;color:#f87171;">Prioridad Absoluta: Laura Ariza</div>
                </div>
              </div>
              <ul style="font-size:12px;color:#cbd5e1;line-height:1.9;padding-left:14px;margin:0;">
                <li><strong>Reposición Inmediata:</strong> Recuperar Surtido en Makro Centro (Gato Dry -14,6%) y Zapatoca (Perro Dry/Wet).</li>
                <li><strong>Recuperar Visibilidad:</strong> Corregir participación en Makro Occidente (-3,5%) y Oriente (-2,4%).</li>
                <li><strong>Desbloqueo de Ceros:</strong> Negociar botaderos, puntas de góndola y balconeras en Homecenter Occidente (al 0%).</li>
              </ul>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background:rgba(30,41,59,.9);border-left:4px solid #3b82f6;border-radius:0 14px 14px 0;padding:22px;">
              <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
                <span style="width:36px;height:36px;border-radius:10px;background:rgba(59,130,246,.2);
                             display:flex;align-items:center;justify-content:center;font-weight:900;color:#60a5fa;">3</span>
                <div>
                  <div style="font-weight:800;color:#f8fafc;font-size:15px;">ACTIVAR MUEBLES DE PISO Y BASTIDORES</div>
                  <div style="font-size:11px;color:#60a5fa;">Despliegue de Exhibición Secundaria</div>
                </div>
              </div>
              <ul style="font-size:12px;color:#cbd5e1;line-height:1.9;padding-left:14px;margin:0;">
                <li><strong>Efecto Replicación:</strong> Extender el modelo de éxito de Esteban Betancourt (+4,5% en Tradicional Centro) a las demás zonas.</li>
                <li><strong>Captura en Juan Giraldo:</strong> Elevar presencia de balconeras y lateral rejilla (actualmente &lt; 2%).</li>
              </ul>
            </div>
            """, unsafe_allow_html=True)

        with p2:
            st.markdown("""
            <div style="background:rgba(30,41,59,.9);border-left:4px solid #f59e0b;border-radius:0 14px 14px 0;padding:22px;margin-bottom:16px;">
              <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
                <span style="width:36px;height:36px;border-radius:10px;background:rgba(245,158,11,.2);
                             display:flex;align-items:center;justify-content:center;font-weight:900;color:#fbbf24;">2</span>
                <div>
                  <div style="font-weight:800;color:#f8fafc;font-size:15px;">CIERRE DE BRECHAS CERCANAS</div>
                  <div style="font-size:11px;color:#fbbf24;">Foco: Juan Carlos Contreras y Luisa Chisco</div>
                </div>
              </div>
              <ul style="font-size:12px;color:#cbd5e1;line-height:1.9;padding-left:14px;margin:0;">
                <li><strong>Juan Carlos (-0,1 pp vs Meet):</strong> Ajustar distribución de Gato Dry/Wet en Supermercados Boom y EPM.</li>
                <li><strong>Luisa Chisco (-1,0 pp vs Meet):</strong> Reactivar bomboneras, cajas y wet solutions en Pet Shop Tradicional Eje Cafetero.</li>
                <li><strong>Marcela Enciso (-1,3 pp vs Meet):</strong> Recuperar Surtido en Perro C&T (-2,6%) y Wet (-1,8%).</li>
              </ul>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background:rgba(30,41,59,.9);border-left:4px solid #8b5cf6;border-radius:0 14px 14px 0;padding:22px;">
              <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
                <span style="width:36px;height:36px;border-radius:10px;background:rgba(139,92,246,.2);
                             display:flex;align-items:center;justify-content:center;font-weight:900;color:#c4b5fd;">4</span>
                <div>
                  <div style="font-weight:800;color:#f8fafc;font-size:15px;">ACELERACIÓN A META EXCEED</div>
                  <div style="font-size:11px;color:#c4b5fd;">Foco: Guillermo Arenas y Gloria Figueroa</div>
                </div>
              </div>
              <ul style="font-size:12px;color:#cbd5e1;line-height:1.9;padding-left:14px;margin:0;">
                <li><strong>Guillermo Arenas (-0,2 pp vs Exceed):</strong> Capturar +0,2% en visibilidad en Independientes o +0,3% en exhibición secundaria.</li>
                <li><strong>Gloria Figueroa (-0,8 pp vs Exceed):</strong> Corregir caída de -3,4% en exhibición en Tradicional reponiendo bomboneras y muebles de piso.</li>
              </ul>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("""
        <div class="closing-banner">
          <span class="badge badge-indigo" style="margin-bottom:16px;display:inline-block;">
            Compromiso de Cierre Q4
          </span>
          <h3>
            “El canal SMI + SPT superó la meta Meet alcanzando un <span style="color:#34d399;">53,2% (+0,7 pp)</span>.
            Con 6 ejecutivos en zona de éxito, enfocar la atención en el plan de choque de Laura Ariza y los cierres de brecha de
            Juan Carlos, Luisa y Marcela garantizará cruzar el umbral <span style="color:#c4b5fd;">Exceed (53,5%)</span> en Q4.”
          </h3>
        </div>
        """, unsafe_allow_html=True)
