from paddleocr import PaddleOCR
from pathlib import Path

ocr = PaddleOCR(use_angle_cls=True, lang="en")

def run_ocr(file_path: str) -> str:
    print(f"DEBUG: Processing file: {file_path}")
    result = ocr.ocr(file_path)

    if not result:
        print("DEBUG: OCR returned empty result")
        return ""

    print(f"DEBUG: result type = {type(result)}, len = {len(result)}")

    all_lines = []

    # Handle the new PaddleOCR 3.0+/PaddleX dict format
    if isinstance(result, list) and result and isinstance(result[0], dict):
        print("DEBUG: Detected PaddleOCR 3.0+/PaddleX dict format")
        for page_idx, page_dict in enumerate(result):
            print(f"DEBUG: Page {page_idx} keys: {list(page_dict.keys())}")
            
            # Extract recognized texts directly from 'rec_texts'
            if 'rec_texts' in page_dict and isinstance(page_dict['rec_texts'], list):
                for text in page_dict['rec_texts']:
                    if isinstance(text, str) and text.strip():
                        all_lines.append(text)
                        # Print first few for quick verification
                        if len(all_lines) <= 5:
                            print(f"DEBUG: Extracted text line: '{text}'")
            else:
                print("DEBUG: No 'rec_texts' found on this page")
            
            # Optional: You can also use 'rec_scores' for confidence filtering
            # e.g., if 'rec_scores' in page_dict and len(page_dict['rec_scores']) == len(page_dict['rec_texts']):
            #     for text, score in zip(page_dict['rec_texts'], page_dict['rec_scores']):
            #         if score > 0.7:  # threshold
            #             all_lines.append(text)

    # Fallback for classic format (in case you downgrade later)
    elif isinstance(result, list) and result and isinstance(result[0], list):
        print("DEBUG: Detected classic list format")
        for page in result:
            for line in page:
                if isinstance(line, (list, tuple)) and len(line) >= 2:
                    text_part = line[1]
                    text = text_part[0] if isinstance(text_part, (list, tuple)) else text_part
                    if isinstance(text, str) and text.strip():
                        all_lines.append(text)

    else:
        print("DEBUG: Unknown result structure")
        print(result)

    full_text = "\n".join(all_lines)
    print(f"DEBUG: Total extracted lines: {len(all_lines)} | Text length: {len(full_text)}")
    return full_text


def detect_document_type(text: str) -> str:
    text_lower = text.lower()
    if "bank statement" in text_lower or "synthetic bank statement" in text_lower:
        return "bank_statement"
    if "dispute" in text_lower or "incorrect" in text_lower:
        return "dispute_letter"
    if "loan application" in text_lower:
        return "loan_application"
    if "income quantile" in text_lower or "age bucket" in text_lower:
        return "synthetic_bank_statement"  # optional for your test files
    return "unknown"