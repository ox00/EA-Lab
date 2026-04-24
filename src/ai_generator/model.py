"""LSTM-based language model for segment ID sequences."""

import torch
import torch.nn as nn


class SegmentLSTM(nn.Module):
    """LSTM model for next-segment prediction."""

    def __init__(
        self,
        vocab_size: int,
        embedding_dim: int = 64,
        hidden_dim: int = 128,
        num_layers: int = 2,
        dropout: float = 0.3,
    ):
        super().__init__()
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers

        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(
            embedding_dim,
            hidden_dim,
            num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x, hidden=None):
        emb = self.embedding(x)
        lstm_out, hidden = self.lstm(emb, hidden)
        lstm_out = self.dropout(lstm_out)
        logits = self.fc(lstm_out)
        return logits, hidden

    def generate(
        self,
        start_ids: list[int],
        max_length: int,
        temperature: float = 1.0,
        device: torch.device = torch.device("cpu"),
    ) -> list[int]:
        self.eval()
        with torch.no_grad():
            input_ids = torch.tensor([start_ids], device=device)
            hidden = None
            generated = list(start_ids)

            for _ in range(max_length - len(start_ids)):
                logits, hidden = self.forward(input_ids, hidden)
                last_logits = logits[0, -1, :] / temperature
                probs = torch.softmax(last_logits, dim=-1)
                next_id = torch.multinomial(probs, num_samples=1).item()
                generated.append(next_id)
                input_ids = torch.cat(
                    [input_ids, torch.tensor([[next_id]], device=device)], dim=1
                )
            return generated