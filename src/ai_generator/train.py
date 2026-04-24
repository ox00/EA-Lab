"""Train an LSTM language model on VGLC chromosome sequences."""

import json
import argparse
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai_generator.model import SegmentLSTM


class ChromosomeDataset(Dataset):
    def __init__(self, sequences: list[list[int]], seq_length: int = 16):
        self.seq_length = seq_length
        self.samples = []
        for chrom in sequences:
            if len(chrom) < seq_length + 1:
                continue
            for i in range(len(chrom) - seq_length):
                input_seq = chrom[i : i + seq_length]
                target_seq = chrom[i + 1 : i + seq_length + 1]
                self.samples.append((input_seq, target_seq))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        input_seq, target_seq = self.samples[idx]
        return torch.tensor(input_seq, dtype=torch.long), torch.tensor(
            target_seq, dtype=torch.long
        )


def load_chromosomes(data_path: Path) -> list[list[int]]:
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)["data"]
    return [entry["chromosome"] for entry in data if entry["chromosome"]]


def train_epoch(model, dataloader, optimizer, criterion, device, clip_grad: float = 1.0):
    model.train()
    total_loss = 0.0
    for inputs, targets in dataloader:
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad()
        logits, _ = model(inputs)
        loss = criterion(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), clip_grad)
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(dataloader)


def validate(model, dataloader, criterion, device):
    model.eval()
    total_loss = 0.0
    with torch.no_grad():
        for inputs, targets in dataloader:
            inputs, targets = inputs.to(device), targets.to(device)
            logits, _ = model(inputs)
            loss = criterion(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))
            total_loss += loss.item()
    return total_loss / len(dataloader)


def main():
    parser = argparse.ArgumentParser(description="Train Segment LSTM")
    parser.add_argument("--data", type=str, default="data/processed/vglc_chromosomes_approx.json")
    parser.add_argument("--output_dir", type=str, default="models")
    parser.add_argument("--embed_dim", type=int, default=64)
    parser.add_argument("--hidden_dim", type=int, default=128)
    parser.add_argument("--num_layers", type=int, default=2)
    parser.add_argument("--dropout", type=float, default=0.3)
    parser.add_argument("--seq_length", type=int, default=8)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--device", type=str, default="auto")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.device == "auto":
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(args.device)
    print(f"Using device: {device}")

    torch.manual_seed(args.seed)

    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    chromosomes = load_chromosomes(data_path)
    print(f"Loaded {len(chromosomes)} chromosome sequences")

    all_ids = set()
    for chrom in chromosomes:
        all_ids.update(chrom)
    vocab_size = max(all_ids) + 1
    print(f"Vocabulary size: {vocab_size} (max ID = {max(all_ids)})")

    split_idx = int(0.8 * len(chromosomes))
    train_chroms = chromosomes[:split_idx]
    val_chroms = chromosomes[split_idx:]

    train_dataset = ChromosomeDataset(train_chroms, seq_length=args.seq_length)
    val_dataset = ChromosomeDataset(val_chroms, seq_length=args.seq_length)
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, drop_last=True)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False, drop_last=False)
    print(f"Train samples: {len(train_dataset)}, Val samples: {len(val_dataset)}")

    model = SegmentLSTM(
        vocab_size=vocab_size,
        embedding_dim=args.embed_dim,
        hidden_dim=args.hidden_dim,
        num_layers=args.num_layers,
        dropout=args.dropout,
    ).to(device)
    print(f"Model parameters: {sum(p.numel() for p in model.parameters())}")

    criterion = nn.CrossEntropyLoss()
    optimizer = AdamW(model.parameters(), lr=args.lr)
    scheduler = CosineAnnealingLR(optimizer, T_max=args.epochs)

    best_val_loss = float("inf")
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for epoch in range(1, args.epochs + 1):
        train_loss = train_epoch(model, train_loader, optimizer, criterion, device, clip_grad=1.0)
        val_loss = validate(model, val_loader, criterion, device)
        scheduler.step()

        print(f"Epoch {epoch:3d}/{args.epochs} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(
                {
                    "model_state_dict": model.state_dict(),
                    "vocab_size": vocab_size,
                    "embed_dim": args.embed_dim,
                    "hidden_dim": args.hidden_dim,
                    "num_layers": args.num_layers,
                    "dropout": args.dropout,
                },
                output_dir / "lstm_generator.pt",
            )
            print(f"  -> Saved best model (val_loss={val_loss:.4f})")

    print(f"\nTraining complete. Best val loss: {best_val_loss:.4f}")
    print(f"Model saved to: {output_dir / 'lstm_generator.pt'}")


if __name__ == "__main__":
    main()