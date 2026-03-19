# Author: modata-analytics

from pathlib import Path
import re

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Microbial Reference Library",
    page_icon="🧪",
    layout="wide"
)

DATA_DIR = Path("data")
METADATA_FILE = DATA_DIR / "metadata.csv"


DISPLAY_COLUMN_NAMES = {
    "microbe": "Microbe",
    "organism_type": "Organism Type",
    "replicate_id": "Replicate ID",
    "replicate_type": "Replicate Type",
    "strain": "Strain",
    "condition": "Condition",
    "gram_status": "Gram Status",
    "analyte_category": "Analyte Category",
    "reference_csv": "Reference CSV",
    "reference_image": "Reference Image",
    "notes": "Notes",
    "keyword_tags": "Keyword Tags",
    "n_records": "Record Count",
    "mz": "m/z",
    "intensity": "Intensity"
}


def normalize_search_text(text) -> str:
    text = str(text).lower().strip()
    text = text.replace("-", " ")
    text = text.replace("_", " ")
    text = re.sub(r"\s+", " ", text)
    return text


@st.cache_data
def load_metadata() -> pd.DataFrame:
    if not METADATA_FILE.exists():
        return pd.DataFrame()

    df = pd.read_csv(METADATA_FILE)
    df = df.fillna("")

    if "organism_type" not in df.columns:
        df["organism_type"] = "Bacterium"

    if "keyword_tags" not in df.columns:
        df["keyword_tags"] = ""

    if "organism_type" in df.columns:
        df["organism_type"] = (
            df["organism_type"]
            .astype(str)
            .str.strip()
            .replace({
                "bacterium": "Bacterium",
                "bacteria": "Bacterium",
                "Bacteria": "Bacterium",
                "Bacterium": "Bacterium",
                "yeast": "Yeast",
                "Yeasts": "Yeast",
                "Yeast": "Yeast",
                "fungus": "Fungal",
                "fungal": "Fungal",
                "Fungus": "Fungal",
                "Fungal": "Fungal"
            })
        )

    if "analyte_category" in df.columns:
        df["analyte_category"] = (
            df["analyte_category"]
            .astype(str)
            .str.strip()
            .replace({
                "lipid_A": "Lipid A",
                "lipid a": "Lipid A",
                "Lipid A": "Lipid A",
                "lipid": "Lipid A",
                "Lipid": "Lipid A",
                "los": "LOS Like",
                "LOS": "LOS Like",
                "LOS_like": "LOS Like",
                "los_like": "LOS Like",
                "los like": "LOS Like",
                "LOS Like": "LOS Like",
                "not_applicable": "Cardiolipin Profile",
                "cardio": "Cardiolipin Profile",
                "Cardio": "Cardiolipin Profile",
                "cardiolipin_profile": "Cardiolipin Profile",
                "cardiolipin profile": "Cardiolipin Profile",
                "Cardiolipin Profile": "Cardiolipin Profile",
                "sterol profile": "Sterol Profile",
                "Sterol Profile": "Sterol Profile",
                "sterol_profile": "Sterol Profile"
            })
        )

    if "gram_status" in df.columns:
        df["gram_status"] = (
            df["gram_status"]
            .astype(str)
            .str.strip()
            .replace({
                "gram-negative": "Gram-negative",
                "gram negative": "Gram-negative",
                "Gram-negative": "Gram-negative",
                "neg": "Gram-negative",
                "Neg": "Gram-negative",
                "gram-positive": "Gram-positive",
                "gram positive": "Gram-positive",
                "Gram-positive": "Gram-positive",
                "pos": "Gram-positive",
                "Pos": "Gram-positive",
                "gram-variable": "Gram-variable",
                "gram variable": "Gram-variable",
                "Gram-variable": "Gram-variable",
                "na": "Not Applicable",
                "N/A": "Not Applicable",
                "n/a": "Not Applicable",
                "not applicable": "Not Applicable",
                "Not Applicable": "Not Applicable"
            })
        )

    if "replicate_type" in df.columns:
        df["replicate_type"] = (
            df["replicate_type"]
            .astype(str)
            .str.strip()
            .replace({
                "technical": "Technical",
                "Technical": "Technical",
                "tech": "Technical",
                "Tech": "Technical",
                "biological": "Biological",
                "Biological": "Biological",
                "bio": "Biological",
                "Bio": "Biological"
            })
        )

    return df


@st.cache_data
def load_spectrum(csv_path: str) -> pd.DataFrame:
    if not csv_path:
        return pd.DataFrame()

    path = Path(csv_path)
    if not path.exists():
        return pd.DataFrame()

    df = pd.read_csv(path)
    expected_cols = {"mz", "intensity"}

    if not expected_cols.issubset(df.columns):
        return pd.DataFrame()

    df = df.sort_values("mz").reset_index(drop=True)
    return df


def plot_spectrum(df: pd.DataFrame, title: str):
    fig = px.line(
        df,
        x="mz",
        y="intensity",
        title=title,
        labels={"mz": "m/z", "intensity": "Intensity"}
    )
    fig.update_traces(mode="lines")
    fig.update_layout(
        xaxis_title="m/z",
        yaxis_title="Intensity",
        template="plotly_white",
        height=500
    )
    return fig


def build_search_mask(df: pd.DataFrame, search_term: str) -> pd.Series:
    search_cols = [
        "microbe",
        "organism_type",
        "strain",
        "notes",
        "condition",
        "analyte_category",
        "gram_status",
        "keyword_tags"
    ]
    valid_cols = [col for col in search_cols if col in df.columns]

    normalized_term = normalize_search_text(search_term)
    search_tokens = normalized_term.split()

    def row_matches(row):
        combined_text = " ".join(
            normalize_search_text(row[col]) for col in valid_cols
        )
        return all(token in combined_text for token in search_tokens)

    return df.apply(row_matches, axis=1)


def prettify_dataframe_columns(df: pd.DataFrame) -> pd.DataFrame:
    renamed_columns = {
        col: DISPLAY_COLUMN_NAMES.get(col, col.replace("_", " ").title())
        for col in df.columns
    }
    return df.rename(columns=renamed_columns)


def main():
    st.title("Microbial Reference Library")
    st.caption("Pilot Streamlit app for curated microbial reference spectra")
    st.caption("Developed by modata-analytics")

    metadata = load_metadata()

    if metadata.empty:
        st.error("metadata.csv was not found or is empty.")
        st.stop()

    with st.sidebar:
        st.header("Filters")

        search_term = st.text_input(
            "Search Microbe / Strain / Notes / Keywords",
            value="",
            placeholder="Type keyword..."
        )

        microbe_options = [""] + sorted(
            [x for x in metadata["microbe"].dropna().unique() if str(x).strip()]
        )
        selected_microbe = st.selectbox(
            "Select Microbe",
            options=microbe_options,
            index=0,
            format_func=lambda x: "All" if x == "" else x
        )

        organism_options = [""] + sorted(
            [x for x in metadata["organism_type"].dropna().unique() if str(x).strip()]
        )
        selected_organism_type = st.selectbox(
            "Organism Type",
            options=organism_options,
            index=0,
            format_func=lambda x: "All" if x == "" else x
        )

        gram_options = [""] + sorted(
            [x for x in metadata["gram_status"].dropna().unique() if str(x).strip()]
        )
        selected_gram = st.selectbox(
            "Gram Status",
            options=gram_options,
            index=0,
            format_func=lambda x: "All" if x == "" else x
        )

        analyte_options = [""] + sorted(
            [x for x in metadata["analyte_category"].dropna().unique() if str(x).strip()]
        )
        selected_analyte = st.selectbox(
            "Analyte Category",
            options=analyte_options,
            index=0,
            format_func=lambda x: "All" if x == "" else x
        )

        replicate_options = [""] + sorted(
            [x for x in metadata["replicate_type"].dropna().unique() if str(x).strip()]
        )
        selected_replicate_type = st.selectbox(
            "Replicate Type",
            options=replicate_options,
            index=0,
            format_func=lambda x: "All" if x == "" else x
        )

    filtered = metadata.copy()

    if search_term.strip():
        filtered = filtered[build_search_mask(filtered, search_term)]

    if selected_microbe != "":
        filtered = filtered[filtered["microbe"] == selected_microbe]

    if selected_organism_type != "":
        filtered = filtered[filtered["organism_type"] == selected_organism_type]

    if selected_gram != "":
        filtered = filtered[filtered["gram_status"] == selected_gram]

    if selected_analyte != "":
        filtered = filtered[filtered["analyte_category"] == selected_analyte]

    if selected_replicate_type != "":
        filtered = filtered[filtered["replicate_type"] == selected_replicate_type]

    if filtered.empty:
        st.error("No matching records were found. Check the search term or selected filters.")
        st.stop()

    filtered = filtered.reset_index(drop=True)
    filtered["display_label"] = filtered.apply(
        lambda row: f"{row['microbe']} | {row['replicate_id']} | {row['replicate_type']}",
        axis=1
    )

    if selected_microbe:
        st.subheader(selected_microbe)
    else:
        st.subheader("Filtered Library Results")

    top_row = filtered.iloc[0]

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Metadata")
        st.write(f"Organism Type: {top_row['organism_type']}")
        st.write(f"Gram Status: {top_row['gram_status']}")
        st.write(f"Analyte Category: {top_row['analyte_category']}")
        st.write(f"Strain: {top_row['strain'] or 'Not provided'}")
        st.write(f"Condition: {top_row['condition'] or 'Not provided'}")
        st.write(f"Notes: {top_row['notes'] or 'None'}")
        st.write(f"Keyword Tags: {top_row['keyword_tags'] or 'None'}")

        if top_row["analyte_category"] == "Cardiolipin Profile":
            st.info(
                "This organism does not have a Lipid A profile, but it can still be "
                "distinguished within the library using its cardiolipin profile."
            )
        elif top_row["analyte_category"] == "Sterol Profile":
            st.info(
                "This organism is represented through a sterol-associated profile rather than "
                "a Lipid A profile."
            )

    with col2:
        st.markdown("### Matching Entries")
        display_cols = [
            "microbe",
            "organism_type",
            "replicate_id",
            "replicate_type",
            "strain",
            "condition",
            "gram_status",
            "analyte_category",
            "keyword_tags",
            "reference_csv",
            "reference_image"
        ]
        matching_entries_df = filtered[display_cols].copy()
        matching_entries_df = prettify_dataframe_columns(matching_entries_df)
        st.dataframe(matching_entries_df, use_container_width=True)

    st.markdown("---")
    st.markdown("### Reference Spectrum")

    selected_label = st.selectbox(
        "Select Entry",
        filtered["display_label"].tolist()
    )

    selected_row = filtered[filtered["display_label"] == selected_label].iloc[0]
    spectrum_df = load_spectrum(selected_row["reference_csv"])

    left, right = st.columns([2, 1])

    with left:
        if spectrum_df.empty:
            st.warning("No spectrum CSV found for this entry.")
        else:
            fig = plot_spectrum(
                spectrum_df,
                f"{selected_row['microbe']} | {selected_row['replicate_id']} | {selected_row['replicate_type']}"
            )
            st.plotly_chart(fig, use_container_width=True)

            with st.expander("Show Peak Table"):
                peak_table_df = prettify_dataframe_columns(spectrum_df.copy())
                st.dataframe(peak_table_df, use_container_width=True)

    with right:
        image_path = selected_row["reference_image"]
        if image_path and Path(image_path).exists():
            st.image(image_path, caption=f"{selected_row['microbe']} spectrum image")
        else:
            st.info("No spectrum image found for this entry.")

    st.markdown("---")
    st.markdown("### Optional Overlay View")

    available_overlay = filtered[filtered["reference_csv"] != ""].copy()
    overlay_options = available_overlay["display_label"].tolist()
    default_overlay = overlay_options[:1] if overlay_options else []

    overlay_labels = st.multiselect(
        "Choose Entries to Overlay",
        options=overlay_options,
        default=default_overlay
    )

    if overlay_labels:
        overlay_frames = []

        for label in overlay_labels:
            row = available_overlay[available_overlay["display_label"] == label].iloc[0]
            rep_df = load_spectrum(row["reference_csv"])

            if not rep_df.empty:
                rep_df = rep_df.copy()
                rep_df["entry_label"] = label
                overlay_frames.append(rep_df)

        if overlay_frames:
            overlay_df = pd.concat(overlay_frames, ignore_index=True)

            overlay_fig = px.line(
                overlay_df,
                x="mz",
                y="intensity",
                color="entry_label",
                labels={
                    "mz": "m/z",
                    "intensity": "Intensity",
                    "entry_label": "Entry"
                },
                title="Overlay Plot"
            )
            overlay_fig.update_layout(
                template="plotly_white",
                height=500
            )
            st.plotly_chart(overlay_fig, use_container_width=True)
        else:
            st.info("No valid CSV files available for overlay.")

    st.markdown("---")
    st.markdown("### Library Summary")

    summary = (
        metadata.groupby(["microbe", "organism_type", "gram_status", "analyte_category"])
        .size()
        .reset_index(name="n_records")
        .sort_values(["microbe", "analyte_category"])
    )
    summary = prettify_dataframe_columns(summary)
    st.dataframe(summary, use_container_width=True)

    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; padding: 10px; font-size: 13px; color: #9aa0a6;'>
            Developed by <b>modata-analytics</b> |
            <a href="https://github.com/modata-analytics" target="_blank" style="color: #58a6ff;">
                View GitHub
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()