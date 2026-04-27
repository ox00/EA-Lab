import matplotlib.pyplot as plt
import numpy as np

# Figure 1: Frequency bar chart
ids = [0, 1, 2, 3, 9, 13, 15]
freqs = [16, 431, 20, 64, 1, 2, 15]
plt.figure(figsize=(8, 4))
plt.bar(ids, freqs, edgecolor='black')
plt.xlabel("Segment ID")
plt.ylabel("Frequency")
plt.title("Segment ID Distribution from VGLC (Real Mario Levels)")
for i, v in zip(ids, freqs):
    plt.text(i, v + 3, str(v), ha='center')
plt.tight_layout()
plt.savefig("docs/results/fig_segment_frequency.png", dpi=150)
print("Saved fig_segment_frequency.png")

# Figure 2: LSTM training curve
epochs = list(range(1, 51))
train_loss = [2.6223, 1.7273, 1.1665, 1.0156, 0.8804, 0.8360, 0.7478, 0.7152, 0.6958, 0.6744,
              0.6493, 0.6150, 0.6201, 0.6288, 0.6105, 0.6046, 0.5815, 0.5940, 0.5735, 0.5840,
              0.5835, 0.5605, 0.5647, 0.5708, 0.5582, 0.5483, 0.5631, 0.5591, 0.5539, 0.5707,
              0.5600, 0.5602, 0.5411, 0.5366, 0.5481, 0.5519, 0.5353, 0.5425, 0.5423, 0.5450,
              0.5464, 0.5340, 0.5442, 0.5416, 0.5428, 0.5450, 0.5557, 0.5357, 0.5507, 0.5609]
val_loss = [2.1364, 1.1104, 0.9313, 0.7691, 0.6956, 0.6542, 0.6066, 0.5629, 0.5439, 0.5410,
            0.5492, 0.5426, 0.5330, 0.5364, 0.5375, 0.5355, 0.5268, 0.5321, 0.5256, 0.5370,
            0.5399, 0.5320, 0.5393, 0.5391, 0.5347, 0.5272, 0.5428, 0.5373, 0.5340, 0.5369,
            0.5400, 0.5332, 0.5349, 0.5389, 0.5431, 0.5418, 0.5412, 0.5390, 0.5404, 0.5409,
            0.5421, 0.5426, 0.5404, 0.5405, 0.5408, 0.5412, 0.5414, 0.5414, 0.5415, 0.5414]

plt.figure(figsize=(8, 4))
plt.plot(epochs, train_loss, label='Train Loss', color='#1f77b4')
plt.plot(epochs, val_loss, label='Val Loss', color='#ff7f0e')
plt.axhline(y=np.log(16), color='gray', linestyle='--', label='Random Baseline (ln 16 ≈ 2.77)')
plt.xlabel("Epoch")
plt.ylabel("Cross-Entropy Loss")
plt.title("LSTM Training Convergence on Mario Segment Sequences")
plt.legend()
plt.tight_layout()
plt.savefig("docs/results/fig_lstm_curve.png", dpi=150)
print("Saved fig_lstm_curve.png")