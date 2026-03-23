from pathlib import Path
import csv
import re


SPECTRA_DIR = Path("data/spectra")
OUTPUT_FILE = Path("data/metadata_generated.csv")


REFERENCE_LOOKUP = {
    "Achromobacter xylosoxidans": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-negative",
        "analyte_category": "Lipid A",
        "keyword_tags": "achromobacter gram negative non fermenter rod",
        "notes": "Reference mzXML",
    },
    "Acetobacter cerevisiae": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-negative",
        "analyte_category": "Lipid A",
        "keyword_tags": "acetobacter acetic acid bacterium gram negative",
        "notes": "Reference mzXML",
    },
    "Acinetobacter baumannii": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-negative",
        "analyte_category": "Lipid A",
        "keyword_tags": "acinetobacter baumannii gram negative coccobacillus opportunistic",
        "notes": "Reference mzXML",
    },
    "Aerococcus loyolae": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-positive",
        "analyte_category": "Cardiolipin Profile",
        "keyword_tags": "aerococcus loyolae gram positive cocci",
        "notes": "Reference mzXML",
    },
    "Aerococcus urinae": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-positive",
        "analyte_category": "Cardiolipin Profile",
        "keyword_tags": "aerococcus urinae gram positive cocci urine",
        "notes": "Reference mzXML",
    },
    "Candida albicans": {
        "organism_type": "Yeast",
        "gram_status": "Not Applicable",
        "analyte_category": "Sterol Profile",
        "keyword_tags": "candida albicans yeast fungal",
        "notes": "Reference mzXML",
    },
    "Candida dubliniensis": {
        "organism_type": "Yeast",
        "gram_status": "Not Applicable",
        "analyte_category": "Sterol Profile",
        "keyword_tags": "candida dubliniensis yeast fungal",
        "notes": "Reference mzXML",
    },
    "Candida duobushaemulonii": {
        "organism_type": "Yeast",
        "gram_status": "Not Applicable",
        "analyte_category": "Sterol Profile",
        "keyword_tags": "candida duobushaemulonii yeast fungal",
        "notes": "Reference mzXML",
    },
    "Candida glabrata": {
        "organism_type": "Yeast",
        "gram_status": "Not Applicable",
        "analyte_category": "Sterol Profile",
        "keyword_tags": "candida glabrata yeast fungal",
        "notes": "Reference mzXML",
    },
    "Candida haemulonii": {
        "organism_type": "Yeast",
        "gram_status": "Not Applicable",
        "analyte_category": "Sterol Profile",
        "keyword_tags": "candida haemulonii yeast fungal",
        "notes": "Reference mzXML",
    },
    "Candida krusei": {
        "organism_type": "Yeast",
        "gram_status": "Not Applicable",
        "analyte_category": "Sterol Profile",
        "keyword_tags": "candida krusei yeast fungal",
        "notes": "Reference mzXML",
    },
    "Candida lusitaniae": {
        "organism_type": "Yeast",
        "gram_status": "Not Applicable",
        "analyte_category": "Sterol Profile",
        "keyword_tags": "candida lusitaniae yeast fungal",
        "notes": "Reference mzXML",
    },
    "Candida parapsilosis": {
        "organism_type": "Yeast",
        "gram_status": "Not Applicable",
        "analyte_category": "Sterol Profile",
        "keyword_tags": "candida parapsilosis yeast fungal",
        "notes": "Reference mzXML",
    },
    "Chlamydia trachomatis": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-negative",
        "analyte_category": "LOS Like",
        "keyword_tags": "chlamydia intracellular gram negative std",
        "notes": "Reference mzXML",
    },
    "Citrobacter portucalensis": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-negative",
        "analyte_category": "Lipid A",
        "keyword_tags": "citrobacter portucalensis gram negative rod enteric",
        "notes": "Reference mzXML",
    },
    "Citrobacter xylosoxidans": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-negative",
        "analyte_category": "Lipid A",
        "keyword_tags": "citrobacter gram negative rod",
        "notes": "Reference mzXML",
    },
    "Corynebacterium tuscaniense": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-positive",
        "analyte_category": "Cardiolipin Profile",
        "keyword_tags": "corynebacterium gram positive rod",
        "notes": "Reference mzXML",
    },
    "Cryptococcus neoformans": {
        "organism_type": "Fungal",
        "gram_status": "Not Applicable",
        "analyte_category": "Sterol Profile",
        "keyword_tags": "cryptococcus neoformans yeast fungus fungal encapsulated cryptococcal",
        "notes": "Reference mzXML",
    },
    "Enterococci spp": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-positive",
        "analyte_category": "Cardiolipin Profile",
        "keyword_tags": "enterococci spp enterococcus gram positive cocci",
        "notes": "Reference mzXML",
    },
    "Enterococcus faecalis": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-positive",
        "analyte_category": "Cardiolipin Profile",
        "keyword_tags": "enterococcus faecalis entero gram positive cocci",
        "notes": "Reference mzXML",
    },
    "Enterococcus faecium": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-positive",
        "analyte_category": "Cardiolipin Profile",
        "keyword_tags": "enterococcus faecium entero gram positive cocci",
        "notes": "Reference mzXML",
    },
    "Escherichia coli": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-negative",
        "analyte_category": "Lipid A",
        "keyword_tags": "e coli ecoli enteric gram negative rod",
        "notes": "Reference mzXML",
    },
    "Gardnerella pickettii": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-variable",
        "analyte_category": "Cardiolipin Profile",
        "keyword_tags": "gardnerella gram variable vaginal",
        "notes": "Reference mzXML",
    },
    "Gardnerella vaginalis": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-variable",
        "analyte_category": "Cardiolipin Profile",
        "keyword_tags": "gardnerella vaginalis vaginal gram variable coccobacillus",
        "notes": "Reference mzXML",
    },
    "Helicobacter pylori": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-negative",
        "analyte_category": "Lipid A",
        "keyword_tags": "helicobacter h pylori curved rod gastric gram negative",
        "notes": "Reference mzXML",
    },
    "Klebsiella aerogenes": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-negative",
        "analyte_category": "Lipid A",
        "keyword_tags": "klebsiella aerogenes enterobacter aerogenes gram negative rod",
        "notes": "Reference mzXML",
    },
    "Klebsiella oxytoca": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-negative",
        "analyte_category": "Lipid A",
        "keyword_tags": "klebsiella oxytoca gram negative rod enteric",
        "notes": "Reference mzXML",
    },
    "Klebsiella pneumoniae": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-negative",
        "analyte_category": "Lipid A",
        "keyword_tags": "klebsiella encapsulated gram negative rod pneumonia",
        "notes": "Reference mzXML",
    },
    "Kodamaea ohmeri": {
        "organism_type": "Yeast",
        "gram_status": "Not Applicable",
        "analyte_category": "Sterol Profile",
        "keyword_tags": "kodamaea ohmeri yeast fungal",
        "notes": "Reference mzXML",
    },
    "Lactobacillus crispatus": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-positive",
        "analyte_category": "Cardiolipin Profile",
        "keyword_tags": "lactobacillus crispatus lacto gram positive rod vaginal",
        "notes": "Reference mzXML",
    },
    "Lactobacillus iners": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-positive",
        "analyte_category": "Cardiolipin Profile",
        "keyword_tags": "lactobacillus iners lacto gram positive rod vaginal",
        "notes": "Reference mzXML",
    },
    "Lactobacillus paragasseri": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-positive",
        "analyte_category": "Cardiolipin Profile",
        "keyword_tags": "lactobacillus gram positive rod",
        "notes": "Reference mzXML",
    },
    "Neisseria spp": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-negative",
        "analyte_category": "LOS Like",
        "keyword_tags": "neisseria spp neisseria species gram negative diplococci los",
        "notes": "Reference mzXML",
    },
    "Porphyromonas gingivalis": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-negative",
        "analyte_category": "Lipid A",
        "keyword_tags": "porphyromonas gingivalis anaerobe oral gram negative",
        "notes": "Reference mzXML",
    },
    "Pseudomonas aeruginosa": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-negative",
        "analyte_category": "Lipid A",
        "keyword_tags": "pseudomonas non fermenter gram negative rod opportunistic",
        "notes": "Reference mzXML",
    },
    "Saccharomyces cerevisiae": {
        "organism_type": "Yeast",
        "gram_status": "Not Applicable",
        "analyte_category": "Sterol Profile",
        "keyword_tags": "saccharomyces cerevisiae baker yeast budding yeast fungal",
        "notes": "Reference mzXML",
    },
    "Salmonella spp": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-negative",
        "analyte_category": "Lipid A",
        "keyword_tags": "salmonella spp gram negative rod enteric",
        "notes": "Reference mzXML",
    },
    "Serratia spp": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-negative",
        "analyte_category": "Lipid A",
        "keyword_tags": "serratia spp gram negative rod opportunistic",
        "notes": "Reference mzXML",
    },
    "Staphylococcus aureus": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-positive",
        "analyte_category": "Cardiolipin Profile",
        "keyword_tags": "staph staphylococcus aureus gram positive cocci skin",
        "notes": "Reference mzXML",
    },
    "Staphylococcus capitis": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-positive",
        "analyte_category": "Cardiolipin Profile",
        "keyword_tags": "staphylococcus capitis gram positive cocci",
        "notes": "Reference mzXML",
    },
    "Staphylococcus epidermidis": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-positive",
        "analyte_category": "Cardiolipin Profile",
        "keyword_tags": "staphylococcus epidermidis gram positive cocci",
        "notes": "Reference mzXML",
    },
    "Staphylococcus haemolyticus": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-positive",
        "analyte_category": "Cardiolipin Profile",
        "keyword_tags": "staphylococcus haemolyticus gram positive cocci",
        "notes": "Reference mzXML",
    },
    "Staphylococcus lugdunensis": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-positive",
        "analyte_category": "Cardiolipin Profile",
        "keyword_tags": "staphylococcus lugdunensis gram positive cocci",
        "notes": "Reference mzXML",
    },
    "Streptococcus pneumoniae": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-positive",
        "analyte_category": "Cardiolipin Profile",
        "keyword_tags": "strep streptococcus pneumoniae gram positive cocci respiratory",
        "notes": "Reference mzXML",
    },
    "Streptococcus pyogenes": {
        "organism_type": "Bacterium",
        "gram_status": "Gram-positive",
        "analyte_category": "Cardiolipin Profile",
        "keyword_tags": "strep streptococcus pyogenes group a strep gram positive cocci",
        "notes": "Reference mzXML",
    },
}


FIELDNAMES = [
    "microbe",
    "organism_type",
    "gram_status",
    "analyte_category",
    "replicate_type",
    "replicate_id",
    "strain",
    "condition",
    "reference_csv",
    "reference_image",
    "reference_mzxml",
    "notes",
    "keyword_tags",
]


def clean_filename_to_microbe_name(filename: str) -> str:
    stem = Path(filename).stem

    # remove common replicate / extra labels
    stem = re.sub(r"\b[Pp]ure\b", "", stem)
    stem = re.sub(r"\brep\d+\b", "", stem, flags=re.IGNORECASE)
    stem = re.sub(r"\s+", " ", stem).strip()

    # normalize spaces and punctuation
    stem = stem.replace("_", " ")
    stem = re.sub(r"\s+", " ", stem).strip()

    return stem


def infer_replicate_id(filename: str) -> str:
    match = re.search(r"(rep\d+)", filename, flags=re.IGNORECASE)
    if match:
        return match.group(1).lower()
    return "rep1"


def build_row_for_file(file_path: Path) -> dict:
    microbe = clean_filename_to_microbe_name(file_path.name)
    lookup = REFERENCE_LOOKUP.get(microbe, None)

    if lookup is None:
        return {
            "microbe": microbe,
            "organism_type": "Unknown",
            "gram_status": "Unknown",
            "analyte_category": "Unknown",
            "replicate_type": "Technical",
            "replicate_id": infer_replicate_id(file_path.name),
            "strain": "Unknown",
            "condition": "standard",
            "reference_csv": "",
            "reference_image": "",
            "reference_mzxml": str(file_path).replace("\\", "/"),
            "notes": "Review classification",
            "keyword_tags": normalize_keywords(microbe),
        }

    return {
        "microbe": microbe,
        "organism_type": lookup["organism_type"],
        "gram_status": lookup["gram_status"],
        "analyte_category": lookup["analyte_category"],
        "replicate_type": "Technical",
        "replicate_id": infer_replicate_id(file_path.name),
        "strain": "Unknown",
        "condition": "standard",
        "reference_csv": "",
        "reference_image": "",
        "reference_mzxml": str(file_path).replace("\\", "/"),
        "notes": lookup["notes"],
        "keyword_tags": lookup["keyword_tags"],
    }


def normalize_keywords(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def main():
    mzxml_files = sorted(
        list(SPECTRA_DIR.glob("*.mzXML")) + list(SPECTRA_DIR.glob("*.mzxml"))
    )

    rows = [build_row_for_file(path) for path in mzxml_files]

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows in {OUTPUT_FILE}")


if __name__ == "__main__":
    main()