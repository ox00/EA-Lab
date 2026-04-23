# scripts/analyze_chromosomes.py
import json
from pathlib import Path
from collections import Counter

def main():
    data_file = Path("data/processed/vglc_chromosomes_approx.json")
    with open(data_file) as f:
        chromosomes = json.load(f)["data"]
    
    all_ids = []
    transitions = Counter()
    for entry in chromosomes:
        chrom = entry["chromosome"]
        all_ids.extend(chrom)
        for i in range(len(chrom)-1):
            transitions[(chrom[i], chrom[i+1])] += 1
    
    freq = Counter(all_ids)
    total = len(all_ids)
    print("Segment ID Frequency:")
    for sid in sorted(freq):
        print(f"  {sid:2d}: {freq[sid]:5d} ({freq[sid]/total:.2%})")
    
    print("\nTop 10 Transitions:")
    for (a, b), c in transitions.most_common(10):
        print(f"  {a} -> {b}: {c}")

if __name__ == "__main__":
    main()