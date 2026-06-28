import os

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Stock Explorer", page_icon="📈", layout="wide")

FUN_FACTS = [
    "In 2000, Netflix offered to sell itself to Blockbuster for just $50 million — Blockbuster turned it down, then went bankrupt a decade later while Netflix grew into a streaming giant.",
    "Apple's 1980 IPO priced at $22 a share and made over 40 of its roughly 1,000 employees instant millionaires.",
    "Steve Jobs ended the day of Apple's 1980 IPO with a net worth of about $217 million — at age 25.",
    "Apple's stock rose almost 32% on its first day of trading in 1980, the biggest tech IPO since Ford Motor Company went public in 1956.",
    "Microsoft went public in 1985 selling only microprocessors and software — hence the name 'Micro-Soft.'",
    "Microsoft briefly overtook Apple as the most valuable U.S. public company in October 2021.",
    "Amazon's 1997 IPO priced at $18 a share, back when the company only sold books.",
    "AWS, a side project Amazon launched in 2006, now generates more than half of the company's operating income.",
    "Google's 2004 IPO used an unusual public auction so everyday investors could bid alongside Wall Street pros.",
    "Google's IPO instantly created 7 billionaires and about 900 millionaires among its early stockholders.",
    "Netflix's 2002 IPO priced at $15 a share — back then it mailed DVDs to 600,000 subscribers in red envelopes.",
    "Since its 2002 IPO, Netflix stock has returned roughly 15,000%, making it one of the best-performing stocks of its era.",
    "The NYSE traces back to the 'Buttonwood Agreement,' signed by 24 stockbrokers under a buttonwood tree in 1792.",
    "Ticker tape parades got their name from literal stock ticker tape thrown out of windows to celebrate the Statue of Liberty's 1886 dedication.",
    "AT&T fought for decades to get the single-letter ticker 'T,' finally winning it on the NYSE in 1930.",
    "Only 26 single-letter ticker symbols exist on the NYSE, and almost all of them are already claimed by major companies.",
    "Ford Motor Company still trades under the simple ticker 'F,' a symbol it's held since the stock began trading.",
    "Berkshire Hathaway's Class A shares have never split, and a single share has traded for well over $500,000.",
    "Coca-Cola listed on the NYSE in 1919; a single share back then, with dividends reinvested, would be worth many millions today.",
    "The 1929 stock market crash wiped out about 90% of the Dow Jones Industrial Average's value over the following three years.",
    "'Black Monday' in October 1987 saw the Dow fall almost 23% in a single day — still the largest one-day percentage drop in its history.",
    "The word 'ticker' comes from the actual ticking sound made by the stock ticker machines invented in 1867.",
    "Nasdaq, founded in 1971, was the world's first electronic stock exchange — no physical trading floor required.",
    "The S&P 500 index was created in 1957, expanding an earlier index that tracked just 90 companies.",
    "Tesla stock split five-for-one in 2020 and three-for-one in 2022 to make shares more accessible to retail investors.",
    "Amazon founder Jeff Bezos started the company in his garage in 1994, originally naming it 'Cadabra' before switching to Amazon.",
    "Walmart went public in 1970 at $16.50 a share; a single original share, after splits, has multiplied into thousands of shares today.",
    "McDonald's stock has split a dozen times since its 1965 IPO, turning one original share into hundreds of shares.",
    "Warren Buffett bought his first stock at age 11 — three shares of Cities Service Preferred — and later said he wished he'd started even sooner.",
    "Disney's stock ticker is simply 'DIS,' chosen to be instantly recognizable to everyday investors.",
    "The first NYSE-listed company to reach a $1 trillion market valuation was Apple, in August 2018.",
    "Apple became the first U.S. company to reach a $3 trillion market cap, briefly touching that milestone in January 2022.",
    "Saudi Aramco's 2019 IPO raised $25.6 billion, making it the largest IPO in history at the time.",
    "The Dutch East India Company is widely considered the first company to issue stock to the public, back in 1602.",
    "Amsterdam's stock exchange, founded in the early 1600s, is generally regarded as the world's oldest.",
    "Facebook's 2012 IPO was plagued by Nasdaq's technical glitches, delaying trading and confusing investor orders for hours.",
    "Meta Platforms (formerly Facebook) changed its corporate name in 2021 but kept trading under its original ticker, 'META.'",
    "Enron's stock collapsed from about $90 a share to under $1 in 2001 after one of the largest accounting scandals in history.",
    "The 'Dogs of the Dow' is an investing strategy of buying the ten highest-dividend-yielding stocks in the Dow each year.",
    "GameStop's stock surged over 1,500% in January 2021, driven largely by retail traders coordinating on Reddit.",
    "The Dow Jones Industrial Average started in 1896 with just 12 companies — General Electric was the only one still on it a century later (until 2018).",
    "Lehman Brothers' 2008 bankruptcy remains the largest in U.S. history, with over $600 billion in assets.",
    "Cisco Systems briefly became the world's most valuable company in 2000, right at the peak of the dot-com bubble.",
    "During the dot-com crash, Amazon's stock fell more than 90% from its peak before recovering over the following decade.",
    "Costco's stock has historically tracked closely with its membership renewal rate, one of the highest in retail at over 90%.",
    "Nike's famous 'swoosh' logo was designed by a graphic design student in 1971 for just $35.",
    "Starbucks went public in 1992 at $17 a share; after several splits, an original share has multiplied many times over.",
    "Visa's 2008 IPO raised $17.9 billion at the time, making it one of the largest IPOs in U.S. history.",
    "Alibaba's 2014 IPO on the NYSE raised $25 billion, setting a record that stood for years.",
    "The term 'blue chip stock' comes from poker, where blue chips traditionally carry the highest value.",
    "'Bull' and 'bear' markets are thought to be named after how each animal attacks — bulls thrust horns upward, bears swipe paws downward.",
    "Intel co-founder Gordon Moore predicted in 1965 that computing power would double roughly every two years — a forecast now called 'Moore's Law.'",
    "Tesla briefly became the most valuable carmaker in the world in 2020, surpassing Toyota despite producing far fewer vehicles.",
    "Nvidia's stock surged dramatically starting in 2023, fueled by explosive demand for AI computing chips.",
    "Berkshire Hathaway started as a struggling New England textile manufacturer before Warren Buffett transformed it into a holding company.",
    "The phrase 'Wall Street' comes from an actual wall built by Dutch settlers in 1653 to defend the southern tip of Manhattan.",
    "Procter & Gamble's stock is one of only a handful to have paid uninterrupted dividends for more than 130 consecutive years.",
]

FACT_COUNTER_PATH = os.path.join(os.path.dirname(__file__), ".fact_counter.txt")


def next_fact():
    try:
        with open(FACT_COUNTER_PATH) as f:
            index = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        index = 0
    try:
        with open(FACT_COUNTER_PATH, "w") as f:
            f.write(str((index + 1) % len(FUN_FACTS)))
    except OSError:
        pass
    return FUN_FACTS[index % len(FUN_FACTS)]

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

if "fun_fact" not in st.session_state:
    st.session_state.fun_fact = next_fact()

st.sidebar.info(f"📰 Did you know? {st.session_state.fun_fact}")

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
