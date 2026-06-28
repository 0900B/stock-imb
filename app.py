import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Stock Explorer", page_icon="📈", layout="wide")

THEMES = {
    "🌙 Dark": dict(bg="#0E1117", secondary_bg="#1C2128", text="#E6EDF3", primary="#00C896", dark=True),
    "☀️ Light": dict(bg="#FFFFFF", secondary_bg="#F0F2F6", text="#262730", primary="#FF4B4B", dark=False),
    "🌊 Ocean": dict(bg="#0B1E2D", secondary_bg="#13344A", text="#E0F2FE", primary="#38BDF8", dark=True),
    "🌅 Sunset": dict(bg="#1A1025", secondary_bg="#2D1B3D", text="#FDE8D8", primary="#FB923C", dark=True),
}

with st.sidebar.expander("🎨 Appearance", expanded=False):
    theme_name = st.selectbox("Theme", list(THEMES.keys()))
    accent = st.color_picker("Accent color", THEMES[theme_name]["primary"])

theme = {**THEMES[theme_name], "primary": accent}
plotly_template = "plotly_dark" if theme["dark"] else "plotly_white"

st.markdown(
    f"""
    <style>
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: {theme['bg']} !important;
        color: {theme['text']} !important;
    }}
    [data-testid="stSidebar"] {{
        background-color: {theme['secondary_bg']} !important;
    }}
    .stApp p, .stApp span, .stApp label, .stApp h1, .stApp h2, .stApp h3,
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {{
        color: {theme['text']} !important;
    }}
    [data-testid="stMultiSelect"] span[data-baseweb="tag"] {{
        background-color: {theme['primary']} !important;
    }}
    div[role="slider"] {{
        background-color: {theme['primary']} !important;
        border-color: {theme['primary']} !important;
    }}
    button[role="tab"][aria-selected="true"] {{
        color: {theme['primary']} !important;
        border-bottom-color: {theme['primary']} !important;
    }}
    [role="tablist"] > div[role="presentation"] {{
        background-color: {theme['primary']} !important;
    }}
    button[kind="primary"], button[kind="secondary"] {{
        border-color: {theme['primary']} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📈 Stock Price Explorer")
st.caption("Comparing growth of major tech stocks since January 2018.")


@st.cache_data
def load_data():
    # This stock dataset is built into plotly — no file to download or push!
    df = px.data.stocks()  # columns: date + 6 big tech stocks
    df["date"] = pd.to_datetime(df["date"])
    return df


df = load_data()
tickers = [c for c in df.columns if c != "date"]

st.sidebar.header("Controls")
chosen = st.sidebar.multiselect("Choose stocks", tickers, default=["AAPL", "MSFT", "GOOG"])

min_date, max_date = df["date"].min().date(), df["date"].max().date()
date_range = st.sidebar.slider(
    "Date range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
)

investment = st.sidebar.number_input(
    "Hypothetical investment ($)", min_value=100, max_value=1_000_000, value=1000, step=100
)

st.sidebar.info(
    "📰 Did you know? In 2000, Netflix offered to sell itself to Blockbuster for "
    "just $50 million — Blockbuster turned it down, then went bankrupt a decade "
    "later while Netflix grew into a streaming giant."
)

if not chosen:
    st.warning("Pick at least one stock from the sidebar.")
    st.stop()

mask = (df["date"].dt.date >= date_range[0]) & (df["date"].dt.date <= date_range[1])
view = df.loc[mask].reset_index(drop=True)

if view.empty or len(view) < 2:
    st.warning("Selected date range is too short — pick a wider range.")
    st.stop()

st.caption(
    "Prices are indexed to 1.00 at the start of the data, so each line shows "
    "growth relative to that starting point."
)

# Growth for each chosen stock over the selected date range, rebased to the
# start of that range so the metrics and chart agree with each other.
rebased = view.copy()
for t in chosen:
    rebased[t] = rebased[t] / rebased[t].iloc[0]

growths = {t: (rebased[t].iloc[-1] - 1) * 100 for t in chosen}
volatility = {t: view[t].pct_change().dropna().std() * 100 for t in chosen}
best = max(growths, key=growths.get)
most_volatile = max(volatility, key=volatility.get)

cols = st.columns(len(chosen) + 2)
for col, t in zip(cols, chosen):
    label = t
    if t == best and len(chosen) > 1:
        label = f"🏆 {label}"
    if t == most_volatile and len(chosen) > 1:
        label = f"🌪️ {label}"
    col.metric(label, f"{rebased[t].iloc[-1]:.2f}x", f"{growths[t]:+.1f}%")

with cols[-2]:
    st.metric("🏆 Best performer", best, f"{growths[best]:+.1f}%")
    st.caption(f"${investment:,.0f} invested in {best} would now be worth "
               f"${investment * rebased[best].iloc[-1]:,.0f}.")

with cols[-1]:
    st.metric("🌪️ Most volatile", most_volatile, f"{volatility[most_volatile]:.2f}% daily swing")
    st.caption("Standard deviation of daily % price changes — higher means bumpier.")

tab1, tab2, tab3 = st.tabs(["📈 Growth over time", "📊 Total growth", "🌪️ Volatility"])

chart_style = dict(
    template=plotly_template,
    paper_bgcolor=theme["bg"],
    plot_bgcolor=theme["bg"],
    font_color=theme["text"],
)

with tab1:
    fig = px.line(rebased, x="date", y=chosen, title="Normalized price over time")
    fig.update_layout(yaxis_title="Growth multiple", legend_title="Stock", **chart_style)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    bar_df = pd.DataFrame({"stock": list(growths.keys()), "growth_%": list(growths.values())})
    bar_fig = px.bar(
        bar_df.sort_values("growth_%", ascending=False),
        x="stock",
        y="growth_%",
        color="stock",
        title="Total growth by stock over selected range",
        text_auto=".1f",
    )
    bar_fig.update_layout(yaxis_title="Growth (%)", showlegend=False, **chart_style)
    st.plotly_chart(bar_fig, use_container_width=True)

with tab3:
    vol_df = pd.DataFrame({"stock": list(volatility.keys()), "volatility_%": list(volatility.values())})
    vol_fig = px.bar(
        vol_df.sort_values("volatility_%", ascending=False),
        x="stock",
        y="volatility_%",
        color="stock",
        title="Daily price volatility by stock (std dev of daily % change)",
        text_auto=".2f",
    )
    vol_fig.update_layout(yaxis_title="Volatility (% daily std dev)", showlegend=False, **chart_style)
    st.plotly_chart(vol_fig, use_container_width=True)

st.divider()
st.subheader("💸 What if I had invested?")
invest_cols = st.columns(len(chosen))
for col, t in zip(invest_cols, chosen):
    final_value = investment * rebased[t].iloc[-1]
    col.metric(f"{t}: ${investment:,.0f} → ", f"${final_value:,.0f}", f"{growths[t]:+.1f}%")
