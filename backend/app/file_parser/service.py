import os
import re

from pypdf import PdfReader


class FileParser:

    def parse(self, file_path: str) -> str:

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".txt":

            with open(file_path, "r", encoding="utf-8") as file:
                return self._clean_text(file.read())

        elif extension == ".pdf":

            reader = PdfReader(file_path)

            pages = []

            for page in reader.pages:

                page_text = page.extract_text() or ""

                pages.append(page_text)

            text = "\n\n".join(pages)

            return self._clean_text(text)

        else:

            raise ValueError("Unsupported file type")

    def _clean_text(self, text: str) -> str:

        # --------------------------------
        # 1. Normalize common PDF artifacts
        # --------------------------------

        text = text.replace("\u00a0", " ")

        # Common words that PDF extraction may split incorrectly.
        replacements = {
            "T echnology": "Technology",
            "F rameworks": "Frameworks",
            "Y ugant": "Yugant",
            "V adodara": "Vadodara",
            "E-V oting": "E-Voting",
            "T ext-to-Speech": "Text-to-Speech",
            "F unctions": "Functions",
            "T ools": "Tools",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        # --------------------------------
        # 2. Fix number + word spacing
        # --------------------------------

        # Example:
        # supporting1,038 -> supporting 1,038
        # serve48,940 -> serve 48,940
        # curated20+regional -> curated 20+regional

        text = re.sub(
            r"([A-Za-z])(\d)",
            r"\1 \2",
            text
        )

        # Example:
        # 20+regional -> 20+ regional
        # 600+DSA -> 600+ DSA

        text = re.sub(
            r"(\d\+)([A-Za-z])",
            r"\1 \2",
            text
        )

        # --------------------------------
        # 3. Fix common word boundaries
        # --------------------------------

        # Example:
        # customersand -> customers and
        # usingSupabase -> using Supabase

        text = re.sub(
            r"([a-z])([A-Z][a-z]+)",
            r"\1 \2",
            text
        )

        # --------------------------------
        # 4. Normalize repeated spaces
        # --------------------------------

        text = re.sub(r"[ \t]+", " ", text)

        # --------------------------------
        # 5. Clean individual lines
        # --------------------------------

        lines = []

        for line in text.splitlines():

            line = line.strip()

            if line:
                lines.append(line)

        return "\n".join(lines)