import re
import json
from typing import List, Dict
from difflib import SequenceMatcher
from jiwer import wer as compute_wer

def parse_asr_output(file_path: str) -> Dict[str, str]:
    """
    Parse the ASR output file to extract the ID and transcription.
    The file format is:
    <file_path> <transcription>
    """
    asr_data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Split the line into file path and transcription
            parts = line.strip().split(' ', 1)
            if len(parts) != 2:
                print(f"Invalid line: {line.strip()}")
                continue
            file_path, transcription = parts
            # Extract the ID from the file path
            file_id = re.search(r'/([^/]+)\.wav$', file_path)
            if file_id:
                asr_data[file_id.group(1)] = transcription
    return asr_data

def load_jsonl(file_path: str) -> List[dict]:
    """
    Load a JSONL file and return a list of dictionaries.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return [json.loads(line.strip()) for line in file]

def extract_entities(data: dict) -> List[str]:
    """
    Extract important entities (filler words) from the reference data.
    """
    return [entity["filler"] for entity in data.get("entities", [])]

# def compute_wer(reference: str, hypothesis: str) -> float:
#     """
#     Compute Word Error Rate (WER) between reference and hypothesis.
#     """
#     ref_words = reference.split()
#     hyp_words = hypothesis.split()

#     # Levenshtein distance table
#     len_ref, len_hyp = len(ref_words), len(hyp_words)
#     dp = [[0 for _ in range(len_hyp + 1)] for _ in range(len_ref + 1)]

#     # Initialization
#     for i in range(len_ref + 1):
#         dp[i][0] = i
#     for j in range(len_hyp + 1):
#         dp[0][j] = j

#     # Fill the DP table
#     for i in range(1, len_ref + 1):
#         for j in range(1, len_hyp + 1):
#             if ref_words[i - 1] == hyp_words[j - 1]:
#                 dp[i][j] = dp[i - 1][j - 1]  # No error
#             else:
#                 dp[i][j] = min(
#                     dp[i - 1][j - 1] + 1,  # Substitution
#                     dp[i - 1][j] + 1,      # Deletion
#                     dp[i][j - 1] + 1       # Insertion
#                 )

#     # WER = (Substitutions + Deletions + Insertions) / Total Reference Words
#     wer = dp[len_ref][len_hyp] / max(len_ref, 1)
#     return round(wer, 3)

def get_similarity_score(a: str, b: str) -> float:
    """
    Compute similarity score between two strings using SequenceMatcher.
    """
    return SequenceMatcher(None, a, b).ratio()

def extract_hypothesis_entities(hypothesis: str, reference_entities: List[str], similarity_threshold: float = 0.8) -> str:
    """
    Extract only the entities from the ASR hypothesis that match the entities in the reference,
    using a similarity threshold to allow for minor differences.
    """
    matched_entities = []
    hyp_words = hypothesis.split()

    # Check for each reference entity
    for ref_entity in reference_entities:
        best_match = ""
        best_score = 0
        for i in range(len(hyp_words) - len(ref_entity.split()) + 1):
            # Compare the reference entity with a phrase of the same length from the hypothesis
            hyp_phrase = " ".join(hyp_words[i:i + len(ref_entity.split())])
            similarity = get_similarity_score(ref_entity, hyp_phrase)
            if similarity > best_score:
                best_match = hyp_phrase
                best_score = similarity

        # If the best match exceeds the threshold, consider it matched
        if best_score >= similarity_threshold:
            matched_entities.append(best_match)

    return " ".join(matched_entities)


def evaluate_entity_wer(reference_file: str, asr_output_file: str, output_file: str):
    """
    Compute WER based only on important entities for sentences in a JSONL reference file
    and a plain-text ASR output file.
    """
    # Load data
    reference_data = load_jsonl(reference_file)
    print(f"Loaded {len(reference_data)} reference items")
    asr_data = parse_asr_output(asr_output_file)
    print(f"Loaded {len(asr_data)} ASR outputs")

    # Compute WER for each matching ID
    with open(output_file, 'w', encoding='utf-8') as out_file:
        total_wer = 0
        count = 0
        for ref_item in reference_data:
            ref_id = ref_item["id"]
            ref_entities = extract_entities(ref_item)
            if ref_id in asr_data:
                hyp_sentence = asr_data[ref_id]
                
                # Extract important words (entities) from the reference
                ref_sentence = " ".join(ref_entities)
                
                # Extract only the words from the hypothesis that are in the reference entities
                hyp_entities = extract_hypothesis_entities(hyp_sentence, ref_entities)
                
                out_file.write(f"{ref_id}: {hyp_entities}\n")
                # Compute WER on these important words (entities)
                if ref_sentence and hyp_entities:
                    wer = compute_wer(ref_sentence, hyp_entities)
                    total_wer += wer
                    count += 1
                    if (wer > 0):
                        print(f"ID: {ref_id} | Ref: {ref_sentence} | Hyp: {hyp_entities} | Entity-WER: {wer}")
                else:
                    wer = 1.0
                    total_wer += wer
                    count += 1
                    print(f"Empty reference or hypothesis for ID: {ref_id}")
            
            else:
                print(f"ASR output not found for ID: {ref_id}")
                
        print(f"\nTotal Entity-WER: {total_wer} for {count} sentences")
        # Average WER
        avg_wer = total_wer / max(count, 1)
        print(f"\nAverage Entity-WER: {round(avg_wer, 8)}")


# Example usage
reference_file = "/home/fithaui/workspace/BKAI-Vietnamese-SLU/slu_data/processed_output/test.jsonl"  # Path to your reference JSONL file
asr_file = "/home/fithaui/workspace/BKAI-Vietnamese-SLU/SLU-ASR/process_trans_file_ema_esc50.txt"       # Path to your ASR JSONL file
output_file = "/home/fithaui/workspace/BKAI-Vietnamese-SLU/hyp_entities.txt"  
evaluate_entity_wer(reference_file, asr_file, output_file)