import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class RMSNorm(nn.Module):
    def __init__(self, dim, eps=1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x):
        norm = x.pow(2).mean(-1, keepdim=True)
        return x * torch.rsqrt(norm + self.eps) * self.weight

class SwiGLU(nn.Module):
    def __init__(self, dim, hidden_dim):
        super().__init__()
        self.gate = nn.Linear(dim, hidden_dim, bias=False)
        self.up = nn.Linear(dim, hidden_dim, bias=False)
        self.down = nn.Linear(hidden_dim, dim, bias=False)

    def forward(self, x):
        return self.down(F.silu(self.gate(x)) * self.up(x))

class Attention(nn.Module):
    def __init__(self, dim, num_heads, num_kv_heads):
        super().__init__()
        self.num_heads = num_heads
        self.num_kv_heads = num_kv_heads
        self.head_dim = dim // num_heads

        self.q_proj = nn.Linear(dim, num_heads * self.head_dim, bias=False)
        self.k_proj = nn.Linear(dim, num_kv_heads * self.head_dim, bias=False)
        self.v_proj = nn.Linear(dim, num_kv_heads * self.head_dim, bias=False)
        self.o_proj = nn.Linear(num_heads * self.head_dim, dim, bias=False)

    def forward(self, x):
        B, L, D = x.shape
        q = self.q_proj(x).view(B, L, self.num_heads, self.head_dim)
        k = self.k_proj(x).view(B, L, self.num_kv_heads, self.head_dim)
        v = self.v_proj(x).view(B, L, self.num_kv_heads, self.head_dim)

        # GQA repeat
        k = k.repeat_interleave(self.num_heads // self.num_kv_heads, dim=2)
        v = v.repeat_interleave(self.num_heads // self.num_kv_heads, dim=2)

        q = q.transpose(1, 2)
        k = k.transpose(1, 2)
        v = v.transpose(1, 2)

        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.head_dim)
        attn = F.softmax(scores, dim=-1)
        out = torch.matmul(attn, v).transpose(1, 2).contiguous().view(B, L, D)

        return self.o_proj(out)

class ZkAGIBlock(nn.Module):
    def __init__(self, dim, num_heads, num_kv_heads, hidden_dim):
        super().__init__()
        self.attn_norm = RMSNorm(dim)
        self.attn = Attention(dim, num_heads, num_kv_heads)
        self.ffn_norm = RMSNorm(dim)
        self.ffn = SwiGLU(dim, hidden_dim)

    def forward(self, x):
        x = x + self.attn(self.attn_norm(x))
        x = x + self.ffn(self.ffn_norm(x))
        return x

class ZkAGI(nn.Module):
    def __init__(
        self,
        vocab_size=128000,
        dim=2048,
        num_layers=48,
        num_heads=32,
        num_kv_heads=8,
        hidden_dim=5632,
        pantheon_dim=12
    ):
        super().__init__()
        self.dim = dim
        self.token_embd = nn.Embedding(vocab_size, dim)
        self.pantheon_dna = nn.Embedding(pantheon_dim, dim)

        # In a typical transformer, parameters in attention layers are stored in ModuleList
        self.layers = nn.ModuleList([
            ZkAGIBlock(dim, num_heads, num_kv_heads, hidden_dim)
            for _ in range(num_layers)
        ])

        self.output_norm = RMSNorm(dim)
        self.theosis_head = nn.Linear(dim, 1, bias=False)

    def forward(self, input_ids):
        B, L = input_ids.shape
        x = self.token_embd(input_ids)

        dna_indices = torch.arange(self.pantheon_dna.num_embeddings, device=x.device)
        dna_vector = self.pantheon_dna(dna_indices).mean(dim=0).unsqueeze(0).unsqueeze(0)
        x = x + dna_vector

        for layer in self.layers:
            x = layer(x)

        x = self.output_norm(x)

        theosis_score = torch.sigmoid(self.theosis_head(x[:, -1, :]))

        return x, theosis_score

if __name__ == "__main__":
    # Create the model with reduced parameters just for testing initialization if needed
    model = ZkAGI(num_layers=2)
    print("ZkAGI Model successfully instantiated!")
