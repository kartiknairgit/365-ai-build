"""Local-only Streamlit interface for the ScamSense educational prototype."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# Community Cloud launches subdirectory entrypoints from the repository root.
sys.path.insert(0, str(Path(__file__).parent / "src"))

from scamsense.analysis import analyse_message
from scamsense.guidance import CYBER_RECOVERY_URL, SCAMWATCH_REPORT_URL
from scamsense.sample_messages import SAMPLE_MESSAGES

st.set_page_config(
    page_title="ScamSense",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      .block-container {max-width: 920px; padding-top: 2rem;}
      .hero {padding: 1.6rem; border: 1px solid #d7dedb; border-radius: 18px;
             background: linear-gradient(135deg, #f5fbf8, #fffaf0); margin-bottom: 1rem;}
      .hero h1 {margin: 0 0 .45rem; color: #153c35;}
      .result {padding: 1.25rem; border: 2px solid #315f56; border-radius: 16px;
               background: #f7faf8; margin: 1rem 0;}
      .risk-label {font-size: 1.35rem; font-weight: 750; color: #173b34;}
      .muted {color: #50645e;}
      div[data-testid="stButton"] button {border-radius: 999px; min-height: 2.8rem;}
      div[data-testid="stTextArea"] textarea {min-height: 190px;}
      @media (max-width: 640px) {.block-container {padding: 1rem;} .hero {padding: 1rem;}}
    </style>
    """,
    unsafe_allow_html=True,
)


def load_sample() -> None:
    selected = st.session_state.get("sample_selector", "Choose a fictional example")
    if selected in SAMPLE_MESSAGES:
        st.session_state.message_input = SAMPLE_MESSAGES[selected]
        st.session_state.analysis_result = None


def clear_message() -> None:
    st.session_state.message_input = ""
    st.session_state.sample_selector = "Choose a fictional example"
    st.session_state.analysis_result = None


if "message_input" not in st.session_state:
    st.session_state.message_input = ""
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

st.markdown(
    """
    <section class="hero">
      <h1>🛡️ ScamSense</h1>
      <p>Pause before you click, share or pay. Check a message for explainable scam-risk
      indicators—privately, with no account or external analysis service.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.subheader("Check a message")
st.caption("Paste text only. ScamSense analyses it in memory and does not save a message history.")
st.selectbox(
    "Try a fictional example",
    ["Choose a fictional example", *SAMPLE_MESSAGES],
    key="sample_selector",
    on_change=load_sample,
)
st.text_area(
    "Message text",
    key="message_input",
    placeholder="Paste the suspicious SMS, email or chat message here…",
    max_chars=20_000,
)

analyse_column, clear_column = st.columns([2, 1])
with analyse_column:
    analyse_clicked = st.button("Analyse message", type="primary", use_container_width=True)
with clear_column:
    st.button("Clear", on_click=clear_message, use_container_width=True)

if analyse_clicked:
    if not st.session_state.message_input.strip():
        st.session_state.analysis_result = None
        st.warning("Add a message or choose a fictional example before analysing.")
    else:
        st.session_state.analysis_result = analyse_message(st.session_state.message_input)

result = st.session_state.analysis_result
if result:
    level_text = result.risk.level.value.title()
    category_text = result.category.category.value.title()
    st.markdown(
        f"""
        <section class="result" aria-label="ScamSense analysis result">
          <div class="risk-label">Risk assessment: {level_text} risk</div>
          <div class="muted">Score {result.risk.score}/100 · likely context:
          {category_text} · category confidence: {result.category.confidence.value}</div>
          <p>{result.explanation}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if result.detected_signals:
        st.subheader(f"Indicators detected ({len(result.detected_signals)})")
        for signal in result.detected_signals:
            with st.expander(f"{signal.category} — {signal.severity.value}"):
                st.write(signal.description)
                st.write(f"Why it matters: {signal.why_it_matters}")
                st.caption(f"Matched clue: “{signal.evidence}”")
    else:
        st.info("No obvious indicators detected. Limited text or new scam patterns can be missed.")

    st.subheader("Safest next step")
    st.success(result.safest_next_step)
    st.markdown("**Avoid for now**")
    for action in result.unsafe_actions:
        st.markdown(f"- {action}")

    with st.expander("A calm explanation to share"):
        st.write(result.parent_friendly_explanation)

    st.subheader("If money, details or an account may be affected")
    st.markdown(
        f"""
        - Contact your bank or provider immediately using its official number or app.
        - Use the Australian Government’s [Scamwatch reporting form]({SCAMWATCH_REPORT_URL}).
        - For cybercrime or account recovery steps, use
          [cyber.gov.au report and recover]({CYBER_RECOVERY_URL}).

        Scamwatch reports are not official police reports. Follow the reporting service’s
        guidance for your circumstances.
        """
    )
    st.warning(result.disclaimer)
else:
    st.markdown("---")
    st.markdown(
        "**What this check can do:** highlight documented warning signs and suggest a safer "
        "next step. It does not inspect links, contact senders or determine whether a message "
        "is definitely a scam or safe."
    )
