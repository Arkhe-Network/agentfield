use ndarray::Array1;

pub trait EmbeddingModel: Send + Sync {
    fn embed(&self, text: &str) -> Array1<f32>;
}

pub struct EmbeddingBridge {}

pub struct SimpleEmbedder {
    dim: usize,
}

impl SimpleEmbedder {
    pub fn new(dim: usize) -> Self {
        Self { dim }
    }
}

impl EmbeddingModel for SimpleEmbedder {
    fn embed(&self, _text: &str) -> Array1<f32> {
        Array1::zeros(self.dim)
    }
}
