pub mod geometric_reward_model;
pub use geometric_reward_model::*;

pub struct CudaRewardModel {}
pub struct CudaEvaluation {
    pub correct: bool,
    pub cuda_speedup_compile: f32,
}
impl CudaRewardModel {
    pub async fn evaluate(&self, _reference: &str, _kernel: &str) -> Result<CudaEvaluation, String> {
        Ok(CudaEvaluation { correct: true, cuda_speedup_compile: 1.5 })
    }
}
